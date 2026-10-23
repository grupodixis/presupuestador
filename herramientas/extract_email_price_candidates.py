from __future__ import annotations

import csv
import hashlib
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from pathlib import Path


PRICE_KEYWORDS = {
    "presupuesto": 4,
    "presupuestos": 4,
    "oferta": 4,
    "tarifa": 5,
    "tarifas": 5,
    "precio": 5,
    "precios": 5,
    "factura": 2,
    "albaran": 3,
    "albarán": 3,
    "pedido": 2,
    "catalogo": 3,
    "catálogo": 3,
    "material": 3,
    "materiales": 3,
    "proveedor": 3,
    "cotizacion": 4,
    "cotización": 4,
    "proforma": 4,
    "netos": 4,
}

DOMAIN_KEYWORDS = {
    "aluminio": 3,
    "mallorquina": 4,
    "menorquina": 4,
    "persiana": 4,
    "pergola": 3,
    "pérgola": 3,
    "barandilla": 3,
    "reja": 2,
    "puerta": 2,
    "inox": 3,
    "acero": 3,
    "hierro": 3,
    "metalica": 3,
    "metálica": 3,
    "chapa": 3,
    "estructura": 3,
    "cerramiento": 3,
    "clima": 2,
    "fontaneria": 2,
    "fontanería": 2,
    "electricidad": 2,
    "iluminacion": 2,
    "iluminación": 2,
}

NEGATIVE_KEYWORDS = {
    "nomina": -8,
    "nómina": -8,
    "vacaciones": -6,
    "seguridad": -4,
    "contraseña": -6,
    "password": -6,
    "newsletter": -4,
    "marketing": -4,
    "air europa": -5,
    "steam": -5,
    "revolut": -6,
    "xtb": -6,
    "kids&us": -5,
}

ATTACHMENT_EXTENSIONS = {
    ".pdf",
    ".xlsx",
    ".xls",
    ".csv",
    ".doc",
    ".docx",
    ".bc3",
    ".zip",
}


@dataclass
class ParsedEmail:
    path: Path
    subject: str
    sender: str
    recipients: str
    email_date: str
    year: str
    attachment_names: list[str]
    score: int
    reasons: list[str]
    has_relevant_attachment: bool


def clean_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def safe_filename(value: str, limit: int = 120) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    value = re.sub(r"\s+", " ", value).strip().strip(".")
    if not value:
        return "sin-nombre"
    if len(value) <= limit:
        return value
    digest = hashlib.sha1(value.encode("utf-8", errors="ignore")).hexdigest()[:8]
    return f"{value[: max(10, limit - 9)]}-{digest}"


def parse_date(value: object, fallback_path: Path) -> tuple[str, str]:
    if value:
        try:
            dt = parsedate_to_datetime(str(value))
            if dt:
                return dt.date().isoformat(), str(dt.year)
        except Exception:
            pass
    match = re.search(r"(20\d{2})[-_ ](\d{2})[-_ ](\d{2})", fallback_path.name)
    if match:
        y, m, d = match.groups()
        return f"{y}-{m}-{d}", y
    return "", ""


def get_plain_body(msg) -> str:
    try:
        body = msg.get_body(preferencelist=("plain", "html"))
        if body:
            content = body.get_content()
            return clean_text(content)[:10000]
    except Exception:
        return ""
    return ""


def score_text(subject: str, sender: str, body: str, attachment_names: list[str]) -> tuple[int, list[str]]:
    haystack = " ".join([subject, sender, " ".join(attachment_names), body[:3000]]).lower()
    score = 0
    reasons: list[str] = []

    for keyword, weight in PRICE_KEYWORDS.items():
        if keyword in haystack:
            score += weight
            reasons.append(keyword)

    for keyword, weight in DOMAIN_KEYWORDS.items():
        if keyword in haystack:
            score += weight
            reasons.append(keyword)

    for keyword, weight in NEGATIVE_KEYWORDS.items():
        if keyword in haystack:
            score += weight
            reasons.append(f"neg:{keyword}")

    relevant_attachments = [
        name for name in attachment_names if Path(name).suffix.lower() in ATTACHMENT_EXTENSIONS
    ]
    if relevant_attachments:
        score += 2
        reasons.append("adjunto")

    return score, sorted(set(reasons))


def parse_email(path: Path) -> tuple[ParsedEmail | None, object | None]:
    try:
        with path.open("rb") as fh:
            msg = BytesParser(policy=policy.default).parse(fh)
    except Exception as exc:
        print(f"WARN parse failed: {path} -> {exc}", file=sys.stderr)
        return None, None

    subject = clean_text(msg.get("subject"))
    sender = clean_text(msg.get("from"))
    recipients = clean_text(msg.get("to"))
    email_date, year = parse_date(msg.get("date"), path)

    attachment_names: list[str] = []
    for part in msg.iter_attachments():
        filename = part.get_filename()
        if filename:
            attachment_names.append(clean_text(filename))

    body = get_plain_body(msg)
    score, reasons = score_text(subject, sender, body, attachment_names)
    has_relevant_attachment = any(
        Path(name).suffix.lower() in ATTACHMENT_EXTENSIONS for name in attachment_names
    )

    parsed = ParsedEmail(
        path=path,
        subject=subject,
        sender=sender,
        recipients=recipients,
        email_date=email_date,
        year=year,
        attachment_names=attachment_names,
        score=score,
        reasons=reasons,
        has_relevant_attachment=has_relevant_attachment,
    )
    return parsed, msg


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def extract_relevant_attachments(msg, parsed: ParsedEmail, out_dir: Path) -> list[str]:
    saved: list[str] = []
    if parsed.score < 6 or not parsed.has_relevant_attachment:
        return saved

    email_key = safe_filename(f"{parsed.email_date or 'sin-fecha'} {parsed.subject}", 72)
    target_dir = out_dir / email_key
    target_dir.mkdir(parents=True, exist_ok=True)

    for part in msg.iter_attachments():
        filename = part.get_filename()
        if not filename:
            continue
        suffix = Path(filename).suffix.lower()
        if suffix not in ATTACHMENT_EXTENSIONS:
            continue
        target = target_dir / safe_filename(filename, 80)
        payload = part.get_payload(decode=True)
        if payload is None:
            continue
        try:
            target.write_bytes(payload)
            saved.append(str(target))
        except OSError as exc:
            print(f"WARN attachment skipped: {target} -> {exc}", file=sys.stderr)
    return saved


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("correos")
    root = root.resolve()
    out_dir = root / "_procesado"
    attachments_dir = out_dir / "adjuntos-candidatos"
    out_dir.mkdir(parents=True, exist_ok=True)
    attachments_dir.mkdir(parents=True, exist_ok=True)

    emails = sorted(root.rglob("*.eml"))
    parsed_rows: list[ParsedEmail] = []
    messages: dict[Path, object] = {}

    for path in emails:
        if "_procesado" in path.parts:
            continue
        parsed, msg = parse_email(path)
        if parsed is None:
            continue
        parsed_rows.append(parsed)
        if msg is not None:
            messages[path] = msg

    index_rows = []
    candidate_rows = []
    for item in sorted(parsed_rows, key=lambda row: (row.score, row.email_date), reverse=True):
        row = {
            "score": item.score,
            "email_date": item.email_date,
            "year": item.year,
            "from": item.sender,
            "to": item.recipients,
            "subject": item.subject,
            "attachments": " | ".join(item.attachment_names),
            "reasons": " | ".join(item.reasons),
            "path": str(item.path),
        }
        index_rows.append(row)
        if item.score >= 6 and item.has_relevant_attachment:
            msg = messages.get(item.path)
            saved = extract_relevant_attachments(msg, item, attachments_dir) if msg else []
            candidate = dict(row)
            candidate["saved_attachments"] = " | ".join(saved)
            candidate_rows.append(candidate)

    fieldnames = [
        "score",
        "email_date",
        "year",
        "from",
        "to",
        "subject",
        "attachments",
        "reasons",
        "path",
    ]
    write_csv(out_dir / "indice-eml.csv", index_rows, fieldnames)
    write_csv(out_dir / "candidatos-precios.csv", candidate_rows, fieldnames + ["saved_attachments"])

    md_lines = [
        "# Candidatos de correos para precios y catalogos",
        "",
        f"- Carpeta: `{root}`",
        f"- Emails procesados: {len(parsed_rows)}",
        f"- Candidatos: {len(candidate_rows)}",
        f"- Generado: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Candidatos principales",
        "",
    ]
    for row in candidate_rows[:80]:
        md_lines.extend(
            [
                f"### {row['email_date'] or 'sin fecha'} - {row['subject'] or 'sin asunto'}",
                "",
                f"- Score: {row['score']}",
                f"- De: {row['from']}",
                f"- Adjuntos: {row['attachments'] or 'sin adjuntos'}",
                f"- Motivos: {row['reasons']}",
                f"- Archivo EML: `{row['path']}`",
                f"- Adjuntos extraidos: {row['saved_attachments'] or 'ninguno'}",
                "",
            ]
        )
    (out_dir / "candidatos-precios.md").write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Emails procesados: {len(parsed_rows)}")
    print(f"Candidatos: {len(candidate_rows)}")
    print(f"Indice: {out_dir / 'indice-eml.csv'}")
    print(f"Candidatos CSV: {out_dir / 'candidatos-precios.csv'}")
    print(f"Candidatos MD: {out_dir / 'candidatos-precios.md'}")
    print(f"Adjuntos: {attachments_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
