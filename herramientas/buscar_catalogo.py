#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
buscar_catalogo.py - Buscador rápido en el catálogo de artículos Factusol.

Uso:
  python herramientas/buscar_catalogo.py "termino"
  python herramientas/buscar_catalogo.py "tubo 40x40" --familia MET
  python herramientas/buscar_catalogo.py "tornillo" --familia TOR --con-precio
  python herramientas/buscar_catalogo.py "oxiron" --json
"""

import sys
import json
import argparse
import unicodedata
from pathlib import Path

DEFAULT_CATALOG_PATH = Path("C:/Users/grupo/outputs/catalogo-20260917/prepared.json")

def norm(text):
    if not text:
        return ""
    return "".join(
        c for c in unicodedata.normalize("NFD", str(text).upper())
        if unicodedata.category(c) != "Mn"
    )

def load_catalog(path=None):
    catalog_path = Path(path) if path else DEFAULT_CATALOG_PATH
    if not catalog_path.exists():
        alt_path = Path(__file__).resolve().parent.parent / "datos-privados" / "prepared.json"
        if alt_path.exists():
            catalog_path = alt_path
        else:
            print(f"Error: No se encuentra el archivo de catalogo en {catalog_path}", file=sys.stderr)
            sys.exit(1)

    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def search_articles(catalog_data, query="", familia=None, tipo=None, con_stock=False, con_precio=False, limit=25):
    catalog = catalog_data.get("catalog", [])
    query_tokens = [norm(t) for t in query.split() if norm(t)]
    
    results = []
    for item in catalog:
        item_id = item[0]
        short_code = item[1] or ""
        desc = item[2] or ""
        item_tipo = item[3] or ""
        fam_code = item[4] or ""
        stock = item[8] or 0
        costo = item[16] or 0
        pvp = item[17] or 0
        
        if familia and fam_code.upper() != familia.upper():
            continue
            
        if tipo:
            tipo_norm = norm(tipo)
            if tipo_norm in ("FISICO", "MATERIAL", "MATERIAL FISICO") and "FISICO" not in norm(item_tipo):
                continue
            elif tipo_norm in ("SERVICIO", "TRABAJO") and "SERVICIO" not in norm(item_tipo):
                continue
                
        if con_stock and (not isinstance(stock, (int, float)) or stock <= 0):
            continue
            
        if con_precio and (not isinstance(costo, (int, float)) or costo <= 0):
            continue
            
        if query_tokens:
            haystack = norm(f"{short_code} {desc} {item[12] or ''} {item[13] or ''} {fam_code}")
            if not all(t in haystack for t in query_tokens):
                continue
                
        results.append(item)
        if len(results) >= limit:
            break
            
    return results

def format_table(items):
    if not items:
        return "No se encontraron articulos que coincidan con la busqueda."
        
    headers = ["ID", "FAM", "CODIGO CORTO", "DESCRIPCION", "COSTE (EUR)", "PVP (EUR)", "STOCK"]
    rows = []
    for it in items:
        coste_str = f"{it[16]:.2f} EUR" if isinstance(it[16], (int, float)) and it[16] > 0 else "-"
        pvp_str = f"{it[17]:.2f} EUR" if isinstance(it[17], (int, float)) and it[17] > 0 else "-"
        stock_str = f"{it[8]:g}" if isinstance(it[8], (int, float)) else "0"
        desc = it[2][:45] + "..." if len(it[2]) > 45 else it[2]
        short = it[1][:22] if it[1] else ""
        rows.append([it[0], it[4], short, desc, coste_str, pvp_str, stock_str])
        
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
            
    sep = "| " + " | ".join("-" * w for w in col_widths) + " |"
    header_row = "| " + " | ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " |"
    
    out = [header_row, sep]
    for row in rows:
        out.append("| " + " | ".join(str(v).ljust(w) for v, w in zip(row, col_widths)) + " |")
        
    return "\n".join(out)

def main():
    parser = argparse.ArgumentParser(description="Buscador en el catalogo de articulos de Factusol")
    parser.add_argument("query", nargs="*", help="Terminos de busqueda (ej. 'tubo 40x40', 'tornillo din 933')")
    parser.add_argument("-f", "--familia", help="Filtrar por codigo de familia (MET, TOR, PIN, ELE, FON, CER, etc.)")
    parser.add_argument("-t", "--tipo", help="Filtrar por tipo (fisico, servicio)")
    parser.add_argument("-s", "--con-stock", action="store_true", help="Solo articulos con stock mayor a cero")
    parser.add_argument("-p", "--con-precio", action="store_true", help="Solo articulos con coste mayor a cero")
    parser.add_argument("-n", "--limite", type=int, default=20, help="Limite de resultados a mostrar (default: 20)")
    parser.add_argument("--json", action="store_true", help="Devolver resultados en formato JSON")
    parser.add_argument("--stats", action="store_true", help="Mostrar estadisticas globales del catalogo")
    parser.add_argument("--catalogo", help="Ruta alternativa a prepared.json")

    args = parser.parse_args()
    data = load_catalog(args.catalogo)
    
    if args.stats:
        stats = data.get("stats", {})
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        return

    query_str = " ".join(args.query).strip()
    if not query_str and not args.familia and not args.tipo:
        print("Indica al menos un termino de busqueda o un filtro de familia (--familia).")
        parser.print_help()
        return

    items = search_articles(
        data,
        query=query_str,
        familia=args.familia,
        tipo=args.tipo,
        con_stock=args.con_stock,
        con_precio=args.con_precio,
        limit=args.limite
    )

    if args.json:
        out_list = []
        for it in items:
            out_list.append({
                "id": it[0],
                "codigo_corto": it[1],
                "descripcion": it[2],
                "tipo": it[3],
                "familia": it[4],
                "familia_nombre": it[5],
                "stock": it[8],
                "costo": it[16],
                "pvp": it[17],
                "codigo_factusol": it[12],
                "ref_proveedor": it[13],
                "proveedor": it[15]
            })
        print(json.dumps(out_list, indent=2, ensure_ascii=False))
    else:
        print(f"\nResultados para '{query_str}' (mostrando hasta {args.limite}):\n")
        print(format_table(items))
        print(f"\nTotal listados: {len(items)}\n")

if __name__ == "__main__":
    main()
