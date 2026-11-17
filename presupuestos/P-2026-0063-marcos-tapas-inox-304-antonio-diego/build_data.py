import os
import json
import subprocess
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# 1. Definición de datos maestros
DATA = {
    "codigo": "P-2026-0063",
    "referencia": "PRE-2026-1117-TAPAS-ESTANCAS-INOX-60X60",
    "estado_presupuesto": "DEFINITIVO — Fabricación en taller con soldadura TIG, juntas estancas EPDM y entrega en POIMA",
    "fecha": "17 de noviembre de 2026",
    "validez_dias": 30,
    "calidad_inox": "Acero Inoxidable AISI 304 (EN 1.4301) / Tornillería Inox A2",
    "proceso_soldadura": "Soldadura TIG en taller bajo protección de argón puro, decapado y pasivado químico de cordones",
    "cliente": {
        "nombre": "ANTONIO Y DIEGO, S.A.",
        "cif": "A07116122",
        "domicilio": "Carrer des Cap Negre, 3 (Pol. Ind. POIMA), 07714 Mahón (Menorca)",
        "contacto": "Guillermo Casanova Rosa / Dpto. Obras y Compras",
        "obra": "Marcos y tapas estancas de arqueta / registro 60x60 cm",
        "ubicacion": "Mahón / Menorca (Illes Balears)",
        "telefono": "+34 971 36 05 05",
        "email": "guillermo@antonioydiego.com / info@antonioydiego.com"
    },
    "emisor": {
        "razon_social": "Dixis Recursos y Soluciones S.L.",
        "cif": "B57825432",
        "nombre_comercial": "HAM Estructuras Metálicas Menorca",
        "domicilio": "Av. Circunval·lació, 11, Polígono de Sant Lluís, 07710 Sant Lluís, Menorca",
        "telefono": "+34 971 35 20 18",
        "movil": "+34 669 769 541",
        "email": "info@hamenorca.com",
        "web": "https://www.hamenorca.com"
    },
    "proyecto": {
        "titulo": "Fabricación en Taller de 4 Marcos Angulares y Tapas Estancas en Acero Inoxidable AISI 304 (60x60 cm)",
        "medidas_utiles": "600 x 600 mm (luz libre de paso)",
        "descripcion": "Suministro de materiales, fabricación en taller mediante soldadura TIG y ensamblaje de 4 conjuntos completos de marco angular perimetral y tapa estanca practicable de medidas útiles interiores 600 x 600 mm en acero inoxidable AISI 304. Cada conjunto está compuesto por tapa de chapa plegada con rigidizadores y tirador escamoteable enrasado, marco perimetral en perfil angular L 40x40x4 mm provisto de garras de anclaje para empotrar en obra civil, junta celular perimetral estanca de EPDM resistente a intemperie y sistema de apriete estanco perimetral mediante 4 tornillos con junta elástica. Incluye decapado y pasivado químico de soldaduras y entrega en instalaciones/obra del cliente en Mahón."
    },
    "tarifas_mo": {
        "oficial_taller_tig": 35.00,
        "oficial_taller_base": 30.00
    },
    "desglose_costes_unitario": {
        "tapa_chapa_plegada": {
            "concepto": "Tapa de chapa plegada en acero inoxidable AISI 304 (e=3 mm) con pestañas a 90° y rigidizadores",
            "coste": 200.00,
            "origen": "Indicación de coste directo del cliente / proveedor externo"
        },
        "marco_angular_inox": {
            "concepto": "Perfil angular L 40x40x4 mm en acero inoxidable AISI 304 (2,60 m x 2,42 kg/m = 6,29 kg @ 7,00 €/kg)",
            "coste": 44.20,
            "origen": "Tarifa material perfiles inox comercial"
        },
        "garras_anclaje_inox": {
            "concepto": "4 garras de fijación perimetrales en pletina inox AISI 304 soldadas al marco para empotrar en obra",
            "coste": 10.00,
            "origen": "Material taller pletina inox"
        },
        "junta_estanqueidad_epdm": {
            "concepto": "Junta perimetral estanca de caucho EPDM celular de alta recuperación elástica (2,40 m)",
            "coste": 15.00,
            "origen": "Suministro junta técnica de estanqueidad"
        },
        "apriete_estanco_tirador": {
            "concepto": "Sistema de 4 tornillos inox A2 de apriete estanco con casquillos/juntas + tirador escamoteable inox",
            "coste": 30.00,
            "origen": "Herrajes y tornillería inox A2"
        },
        "consumibles_taller": {
            "concepto": "Argón puro soldadura TIG, varilla inox 304L, discos corte/desbaste fino y gel decapante/pasivante",
            "coste": 18.00,
            "origen": "Consumibles directos taller HAM"
        },
        "mo_taller_tig": {
            "concepto": "Mano de obra taller: corte ingletes, armado, soldadura TIG, roscado M8, ajuste y pasivado (2,75 h @ 35 €/h)",
            "horas": 2.75,
            "tarifa_hora": 35.00,
            "coste": 96.25,
            "origen": "Oficial 1ª Taller Soldador TIG"
        },
        "transporte_entrega": {
            "concepto": "Embalaje protector y transporte/entrega en nave de Antonio y Diego SA (POIMA, Mahón)",
            "coste": 10.00,
            "origen": "Logística local Menorca"
        }
    },
    "partida": {
        "id": "1.01",
        "concepto": "Marco angular y tapa estanca en acero inoxidable AISI 304 de 600 x 600 mm",
        "descripcion": "Fabricación a medida y suministro de conjunto estanco de arqueta/registro de medidas interiores útiles 600 x 600 mm, ejecutado íntegramente en acero inoxidable AISI 304 (EN 1.4301). Compuesto por tapa en chapa plegada con rigidizadores perimetrales y tirador escamoteable enrasado de acero inoxidable; marco perimetral exterior en perfil angular L 40x40x4 mm cortado a inglete a 45° y soldado a TIG, dotado de garras de fijación para empotrar en fábrica de albañilería u hormigón; junta perimetral estanca de caucho celular EPDM de alta elasticidad resistente a intemperie; y 4 puntos perimetrales de apriete estanco mediante tornillos de acero inoxidable A2 con arandela de sellado elástico. Tratamiento de acabado superficial mediante desbarbado, decapado y pasivado químico de todos los cordones de soldadura. Totalmente terminado y listo para su colocación.",
        "unidad": "ud",
        "cantidad": 4,
        "coste_unitario": 423.45,
        "precio_unitario": 590.00,
        "subtotal": 2360.00
    },
    "totales": {
        "coste_directo_total": 1693.80,
        "base_imponible": 2360.00,
        "iva_porcentaje": 21,
        "iva_importe": 495.60,
        "total_con_iva": 2855.60,
        "beneficio_bruto": 666.20,
        "margen_sobre_venta_pct": 28.23,
        "margen_sobre_coste_pct": 39.33
    }
}

# Guardar datos.json
with open(os.path.join(BASE_DIR, "datos.json"), "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=2)

print("datos.json creado correctamente.")
