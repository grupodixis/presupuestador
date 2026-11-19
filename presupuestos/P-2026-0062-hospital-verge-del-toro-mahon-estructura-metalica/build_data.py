import os
import json
import subprocess
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def build_data():
    raw_data = {
        "codigo": "P-2026-0062",
        "referencia": "PRE-2026-1116-HOSPITAL-MAHON-ESTRUCTURA",
        "version": "1.0",
        "fecha": "16 de noviembre de 2026",
        "fecha_iso": "2026-11-16",
        "validez_dias": 30,
        "forma_pago": "Certificaciones mensuales según avance de obra ejecutada y aprobada por la D.F. / Facturación a 30 días",
        "plazo_ejecucion_estimado": "Coordinado con el Plan General de Reforma del Hospital (fabricación secuencial en taller y montaje escalonado por fases)",
        "cliente": {
            "empresa": "Cobra Edificación Singular (Cobra Singular Building / Grupo Cobra)",
            "contacto": "Fernando Sánchez Sánchez",
            "cargo": "Arquitecto Técnico · Departamento de Estudios",
            "telefono": "(34) 914 569 500 / (34) 611 820 961",
            "direccion": "C/ Cardenal Marcelo Spínola 14",
            "codigo_postal": "28016",
            "poblacion": "Madrid",
            "provincia": "Madrid",
            "pais": "España",
            "web": "https://grupocobra.com/"
        },
        "proyecto": {
            "titulo": "Projecte Bàsic i d'Execució 2 de Reforma Interior i Ordenació de la Parcel·la del Nou Hospital Verge del Toro, Maó, Menorca",
            "promotor": "IB-SALUT (Govern de les Illes Balears - Servei de Salut)",
            "obra": "Nou Hospital Verge del Toro",
            "emplazamiento": "Carrer de Barcelona / Verge del Toro, 07701 Maó, Menorca (Illes Balears)",
            "capitulo_codigo": "H06",
            "capitulo_nombre": "ESTRUCTURA METALICA",
            "planos_referencia": "ES.01.01 a ES.04.09 (Plantas generales, refuerzos y fosos) y ER.01.01 a ER.05.07 (Cuadros de pilares, plantas de derribo y obra nueva, escaleras y detalles constructivos)",
            "normativa_aplicable": "Código Estructural (Real Decreto 470/2021), UNE-EN 1090-2 (Clase de Ejecución EXC3 / EXC2), UNE-EN 10025-2 (Acero S275JR), Marcado CE y CTE DB-SE / DB-SI",
            "criterio_pintura_ham": "Tratamiento anticorrosión mediante preparación superficial, imprimación de adherencia antioxidante en taller y esmalte de poliuretano bicomponente para acabado (C1 interior / C4 cimentación). Conforme al estándar de HAM Menorca, en ningún caso se utiliza pintura al horno o termolacado.",
            "uniones_y_retacado": "Fijaciones mecánicas y químicas con varillas roscadas B500S M16/M20 e inyección continua de resina epoxi de dos componentes de baja viscosidad. Retacado y relleno continuo con mortero sin retracción de alta resistencia."
        },
        "emisor": {
            "razon_social": "Dixis Recursos y Soluciones S.L.",
            "cif": "B57825432",
            "nombre_comercial": "HAM Estructuras Metálicas Menorca / HAMenorca",
            "domicilio": "Av. Circunval·lació, 11, Polígono Industrial de Sant Lluís, 07710 Sant Lluís, Menorca (Illes Balears)",
            "telefono": "+34 971 35 20 18",
            "movil": "+34 669 769 541",
            "email": "pablo@dixis.es / administracion@dixis.es",
            "web": "https://www.hamenorca.com",
            "representante": "Pablo Sebastián Sánchez Arnoletto"
        },
        "subcapitulos": [
            {
                "codigo": "06.01",
                "nombre": "REHABILITACION",
                "partidas": [
                    {
                        "codigo": "PM.01.05.01.01.02",
                        "padre_capitulo": "PM.01.05.01.01 Elementos de anclaje",
                        "resumen": "PLACA DE ANCLAJE INTERIOR ACERO S275JR - PLANCHA, TRABAJADO EN TALLER",
                        "unidad": "kg",
                        "cantidad": 131.88,
                        "coste_unitario": 4.75,
                        "precio_venta_unitario": 6.80,
                        "descripcion": "Placa de anclaje con acero S275JR según UNE-EN 10025-2, para elementos de anclaje formados por pieza simple, en perfiles laminados en caliente serie L, LD, T, redondo, cuadrado, rectangular y plancha, trabajado en taller, colocado en obra con soldadura y/o tornillos. Los elementos llegarán a obra con el tratamiento de durabilidad C1. Clase de ejecución EXC3 según Código Estructural. Incluye p.p. de rigidizadores, cartelas y pletinas, mortero sin retracción, varillas con resina epoxi de dos componentes y medios auxiliares.",
                        "mediciones": [
                            {"comentario": "CIM", "n": 2, "longitud": 0.12, "anchura": 157.0, "altura": 0.0, "cantidad": 37.68},
                            {"comentario": "CIM", "n": 2, "longitud": 0.10, "anchura": 157.0, "altura": 0.0, "cantidad": 31.40},
                            {"comentario": "TPB", "n": 4, "longitud": 0.09, "anchura": 157.0, "altura": 0.0, "cantidad": 56.52},
                            {"comentario": "AJUSTE", "n": 6.28, "longitud": 0.0, "anchura": 0.0, "altura": 0.0, "cantidad": 6.28}
                        ]
                    },
                    {
                        "codigo": "PM.01.05.01.01.01",
                        "padre_capitulo": "PM.01.05.01.02 Pilares metálicos",
                        "resumen": "ESTRUCTURA VERTICAL INTERIOR ACERO S275JR - PERFILES IP,HE,UP, TRABAJADOS EN TALLER",
                        "unidad": "kg",
                        "cantidad": 3826.12,
                        "coste_unitario": 3.55,
                        "precio_venta_unitario": 4.95,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para pilares formados por pieza simple y compuesta en perfiles laminados en caliente HEB y pletinas soldadas, trabajado en taller, colocado en obra con soldadura y/o tornillos. Elementos de interior C1 con imprimación antioxidante de taller y pintura de acabado en obra. Clase de ejecución EXC3 según Código Estructural. Incluye medios auxiliares, izado y apuntalamiento.",
                        "mediciones": [
                            {"comentario": "P1 - HEB-180", "n": 2, "longitud": 3.6, "anchura": 51.2, "altura": 0.0, "cantidad": 368.64},
                            {"comentario": "P1 - HEB-220+PL.15", "n": 2, "longitud": 3.6, "anchura": 97.4, "altura": 0.0, "cantidad": 701.28},
                            {"comentario": "P2 - HEB-160", "n": 2, "longitud": 3.6, "anchura": 42.6, "altura": 0.0, "cantidad": 306.72},
                            {"comentario": "P2 - HEB-200+PL.15", "n": 2, "longitud": 3.6, "anchura": 84.9, "altura": 0.0, "cantidad": 611.28},
                            {"comentario": "P3 - HEB-160", "n": 2, "longitud": 3.6, "anchura": 42.6, "altura": 0.0, "cantidad": 306.72},
                            {"comentario": "P3 - HEB-180+PL.15", "n": 2, "longitud": 3.6, "anchura": 72.4, "altura": 0.0, "cantidad": 521.28},
                            {"comentario": "P4 - HEB-160", "n": 2, "longitud": 3.6, "anchura": 42.6, "altura": 0.0, "cantidad": 306.72},
                            {"comentario": "P4 - HEB-180+PL.15", "n": 2, "longitud": 3.6, "anchura": 72.4, "altura": 0.0, "cantidad": 521.28},
                            {"comentario": "AJUSTE", "n": 182.20, "longitud": 0.0, "anchura": 0.0, "altura": 0.0, "cantidad": 182.20}
                        ]
                    },
                    {
                        "codigo": "P442-BA21PM",
                        "padre_capitulo": "PM.01.05.01.03 Vigas metálicas",
                        "resumen": "ESTRUCTURA HORIZONTAL INTERIOR ACERO S275JR - PERFILES IP,HE,UP, TRABAJADOS EN TALLER",
                        "unidad": "kg",
                        "cantidad": 30922.65,
                        "coste_unitario": 3.45,
                        "precio_venta_unitario": 4.80,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para vigas, viguetas y zancas de escalera formadas por pieza simple, en perfiles laminados en caliente serie IPE, HEB y UPN, trabajado en taller, colocado en obra con soldadura y tornillos de alta resistencia. Elementos de interior C1 con imprimación anticorrosiva en taller y pintura de acabado. Clase de ejecución EXC2 según Código Estructural. Incluye vigas de plantas TPSS a TP4 y zancas de Escalera 1 y Escalera 2.",
                        "mediciones": [
                            {"comentario": "TPSS - IPE-300", "n": 1, "longitud": 3.6, "anchura": 42.2, "altura": 0.0, "cantidad": 151.92},
                            {"comentario": "TPSS - IPE-360", "n": 1, "longitud": 5.1, "anchura": 57.1, "altura": 0.0, "cantidad": 291.21},
                            {"comentario": "TPSS - IPE-240", "n": 1, "longitud": 5.8, "anchura": 30.7, "altura": 0.0, "cantidad": 178.06},
                            {"comentario": "TPSS - IPE-140", "n": 1, "longitud": 9.0, "anchura": 12.9, "altura": 0.0, "cantidad": 116.10},
                            {"comentario": "TPSS - IPE-200", "n": 1, "longitud": 3.2, "anchura": 22.4, "altura": 0.0, "cantidad": 71.68},
                            {"comentario": "TPSS - UPN-220", "n": 1, "longitud": 3.6, "anchura": 29.4, "altura": 0.0, "cantidad": 105.84},
                            {"comentario": "TPSS - UPN-300", "n": 1, "longitud": 15.0, "anchura": 46.2, "altura": 0.0, "cantidad": 693.00},
                            {"comentario": "TPSS - HEB-200", "n": 1, "longitud": 18.0, "anchura": 61.3, "altura": 0.0, "cantidad": 1103.40},
                            {"comentario": "TPB - IPE-300", "n": 1, "longitud": 7.2, "anchura": 42.2, "altura": 0.0, "cantidad": 303.84},
                            {"comentario": "TPB - IPE-360", "n": 1, "longitud": 5.1, "anchura": 57.1, "altura": 0.0, "cantidad": 291.21},
                            {"comentario": "TPB - IPE-240", "n": 1, "longitud": 5.8, "anchura": 30.7, "altura": 0.0, "cantidad": 178.06},
                            {"comentario": "TPB - IPE-140", "n": 1, "longitud": 10.3, "anchura": 12.9, "altura": 0.0, "cantidad": 132.87},
                            {"comentario": "TPB - IPE-200", "n": 1, "longitud": 3.2, "anchura": 22.4, "altura": 0.0, "cantidad": 71.68},
                            {"comentario": "TPB - UPN-220", "n": 1, "longitud": 3.6, "anchura": 29.4, "altura": 0.0, "cantidad": 105.84},
                            {"comentario": "TPB - UPN-300", "n": 1, "longitud": 15.0, "anchura": 46.2, "altura": 0.0, "cantidad": 693.00},
                            {"comentario": "TPB - HEB-200", "n": 1, "longitud": 18.0, "anchura": 61.3, "altura": 0.0, "cantidad": 1103.40},
                            {"comentario": "TP1-TP2-TP3 - IPE-300", "n": 3, "longitud": 32.0, "anchura": 42.2, "altura": 0.0, "cantidad": 4051.20},
                            {"comentario": "TP1-TP2-TP3 - IPE-360", "n": 3, "longitud": 5.1, "anchura": 57.1, "altura": 0.0, "cantidad": 873.63},
                            {"comentario": "TP1-TP2-TP3 - IPE-240", "n": 3, "longitud": 5.9, "anchura": 30.7, "altura": 0.0, "cantidad": 543.39},
                            {"comentario": "TP1-TP2-TP3 - IPE-140", "n": 3, "longitud": 10.3, "anchura": 12.9, "altura": 0.0, "cantidad": 398.61},
                            {"comentario": "TP1-TP2-TP3 - IPE-200", "n": 3, "longitud": 3.2, "anchura": 22.4, "altura": 0.0, "cantidad": 215.04},
                            {"comentario": "TP1-TP2-TP3 - UPN-220", "n": 3, "longitud": 8.9, "anchura": 29.4, "altura": 0.0, "cantidad": 784.98},
                            {"comentario": "TP1-TP2-TP3 - UPN-300", "n": 3, "longitud": 11.0, "anchura": 46.2, "altura": 0.0, "cantidad": 1524.60},
                            {"comentario": "TP4 - IPE-240", "n": 1, "longitud": 42.0, "anchura": 30.7, "altura": 0.0, "cantidad": 1289.40},
                            {"comentario": "TP4 - IPE-140", "n": 1, "longitud": 17.0, "anchura": 12.9, "altura": 0.0, "cantidad": 219.30},
                            {"comentario": "TP4 - IPE-270", "n": 1, "longitud": 42.0, "anchura": 36.1, "altura": 0.0, "cantidad": 1516.20},
                            {"comentario": "ESC. 2 - PS/PB - UPN-260", "n": 2, "longitud": 10.7, "anchura": 37.9, "altura": 0.0, "cantidad": 811.06},
                            {"comentario": "ESC. 2 - PS/PB - IPE-140", "n": 5, "longitud": 1.4, "anchura": 12.9, "altura": 0.0, "cantidad": 90.30},
                            {"comentario": "ESC. 2 - PS/PB - IPE-300", "n": 1, "longitud": 5.1, "anchura": 42.2, "altura": 0.0, "cantidad": 215.22},
                            {"comentario": "ESC. 2 - PB/P1 - UPN-260", "n": 2, "longitud": 12.8, "anchura": 37.9, "altura": 0.0, "cantidad": 970.24},
                            {"comentario": "ESC. 2 - PB/P1 - IPE-140", "n": 5, "longitud": 1.4, "anchura": 12.9, "altura": 0.0, "cantidad": 90.30},
                            {"comentario": "ESC. 2 - PB/P1 - IPE-300", "n": 1, "longitud": 5.2, "anchura": 42.2, "altura": 0.0, "cantidad": 219.44},
                            {"comentario": "ESC. 2 - P1/P2 - UPN-260", "n": 2, "longitud": 12.8, "anchura": 37.9, "altura": 0.0, "cantidad": 970.24},
                            {"comentario": "ESC. 2 - P1/P2 - IPE-140", "n": 6, "longitud": 1.4, "anchura": 12.9, "altura": 0.0, "cantidad": 108.36},
                            {"comentario": "ESC. 2 - P1/P2 - IPE-300", "n": 1, "longitud": 5.2, "anchura": 42.2, "altura": 0.0, "cantidad": 219.44},
                            {"comentario": "ESC. 2 - P2/P3 - UPN-260", "n": 2, "longitud": 12.8, "anchura": 37.9, "altura": 0.0, "cantidad": 970.24},
                            {"comentario": "ESC. 2 - P2/P3 - IPE-140", "n": 6, "longitud": 1.4, "anchura": 12.9, "altura": 0.0, "cantidad": 108.36},
                            {"comentario": "ESC. 2 - P2/P3 - IPE-300", "n": 1, "longitud": 5.2, "anchura": 42.2, "altura": 0.0, "cantidad": 219.44},
                            {"comentario": "ESC. 2 - P3/P4 - UPN-260", "n": 2, "longitud": 12.8, "anchura": 37.9, "altura": 0.0, "cantidad": 970.24},
                            {"comentario": "ESC. 2 - P3/P4 - IPE-140", "n": 6, "longitud": 1.4, "anchura": 12.9, "altura": 0.0, "cantidad": 108.36},
                            {"comentario": "ESC. 2 - P3/P4 - IPE-300", "n": 1, "longitud": 5.2, "anchura": 42.2, "altura": 0.0, "cantidad": 219.44},
                            {"comentario": "ESC. 1 - PS/PB - UPN-300", "n": 2, "longitud": 11.0, "anchura": 46.2, "altura": 0.0, "cantidad": 1016.40},
                            {"comentario": "ESC. 1 - PS/PB - IPE-140", "n": 5, "longitud": 1.6, "anchura": 12.9, "altura": 0.0, "cantidad": 103.20},
                            {"comentario": "ESC. 1 - PS/PB - IPE-300", "n": 1, "longitud": 3.6, "anchura": 42.2, "altura": 0.0, "cantidad": 151.92},
                            {"comentario": "ESC. 1 - PB/P1 - UPN-300", "n": 2, "longitud": 6.7, "anchura": 46.2, "altura": 0.0, "cantidad": 619.08},
                            {"comentario": "ESC. 1 - PB/P1 - UPN-220", "n": 2, "longitud": 5.5, "anchura": 29.4, "altura": 0.0, "cantidad": 323.40},
                            {"comentario": "ESC. 1 - PB/P1 - IPE-140", "n": 4, "longitud": 1.6, "anchura": 12.9, "altura": 0.0, "cantidad": 82.56},
                            {"comentario": "ESC. 1 - PB/P1 - IPE-300", "n": 1, "longitud": 3.7, "anchura": 42.2, "altura": 0.0, "cantidad": 156.14},
                            {"comentario": "ESC. 1 - P1/P2 - UPN-220", "n": 2, "longitud": 11.0, "anchura": 29.4, "altura": 0.0, "cantidad": 646.80},
                            {"comentario": "ESC. 1 - P1/P2 - IPE-140", "n": 4, "longitud": 1.6, "anchura": 12.9, "altura": 0.0, "cantidad": 82.56},
                            {"comentario": "ESC. 1 - P1/P2 - IPE-300", "n": 1, "longitud": 3.7, "anchura": 42.2, "altura": 0.0, "cantidad": 156.14},
                            {"comentario": "ESC. 1 - P2/P3 - UPN-220", "n": 2, "longitud": 11.0, "anchura": 29.4, "altura": 0.0, "cantidad": 646.80},
                            {"comentario": "ESC. 1 - P2/P3 - IPE-140", "n": 4, "longitud": 1.6, "anchura": 12.9, "altura": 0.0, "cantidad": 82.56},
                            {"comentario": "ESC. 1 - P2/P3 - IPE-300", "n": 1, "longitud": 3.7, "anchura": 42.2, "altura": 0.0, "cantidad": 156.14},
                            {"comentario": "ESC. 1 - P3/P4 - UPN-220", "n": 2, "longitud": 11.0, "anchura": 29.4, "altura": 0.0, "cantidad": 646.80},
                            {"comentario": "ESC. 1 - P3/P4 - IPE-140", "n": 4, "longitud": 1.6, "anchura": 12.9, "altura": 0.0, "cantidad": 82.56},
                            {"comentario": "ESC. 1 - P3/P4 - IPE-300", "n": 1, "longitud": 3.7, "anchura": 42.2, "altura": 0.0, "cantidad": 156.14},
                            {"comentario": "TPSS - IPE-160", "n": 1, "longitud": 11.0, "anchura": 15.8, "altura": 0.0, "cantidad": 173.80},
                            {"comentario": "TPB - IPE-160", "n": 1, "longitud": 11.0, "anchura": 15.8, "altura": 0.0, "cantidad": 173.80},
                            {"comentario": "TP1 - IPE-160", "n": 1, "longitud": 11.0, "anchura": 15.8, "altura": 0.0, "cantidad": 173.80},
                            {"comentario": "TP2 - IPE-160", "n": 1, "longitud": 11.0, "anchura": 15.8, "altura": 0.0, "cantidad": 173.80},
                            {"comentario": "TP3 - IPE-160", "n": 1, "longitud": 11.0, "anchura": 15.8, "altura": 0.0, "cantidad": 173.80},
                            {"comentario": "TP4 - IPE-160", "n": 1, "longitud": 11.0, "anchura": 15.8, "altura": 0.0, "cantidad": 173.80},
                            {"comentario": "AJUSTE", "n": 1472.51, "longitud": 0.0, "anchura": 0.0, "altura": 0.0, "cantidad": 1472.51}
                        ]
                    },
                    {
                        "codigo": "PM.01.05.01.04.01",
                        "padre_capitulo": "PM.01.05.01.04 Forjados colaborantes",
                        "resumen": "FORJADO COLABORANTE, E=16cm (6+10), HA-25/B/20/XC3, BAJO RASANTE",
                        "unidad": "m²",
                        "cantidad": 66.01,
                        "coste_unitario": 76.00,
                        "precio_venta_unitario": 106.00,
                        "descripcion": "Formación de forjado 16 cm de grueso total, con planchas colaborantes de acero galvanizado S320GD de espesor 1 mm. Incluye hormigón HA-25/B/20/XC3 fluido vertido con bomba, armadura AP500 S en barras B500S, mallazo electrosoldado AP500 T B500S, anclajes químicos con resinas epoxi sin disolventes y conectores tipo Nelson soldados a los perfiles metálicos.",
                        "mediciones": [
                            {"comentario": "TPSS", "n": 1, "longitud": 15.0, "anchura": 0.0, "altura": 0.0, "cantidad": 15.00},
                            {"comentario": "ESC. 1", "n": 1, "longitud": 8.64, "anchura": 0.0, "altura": 0.0, "cantidad": 8.64},
                            {"comentario": "ESC. 2", "n": 1, "longitud": 10.80, "anchura": 0.0, "altura": 0.0, "cantidad": 10.80},
                            {"comentario": "ESCALERA 1/2 PS - ESC. 1", "n": 1, "longitud": 15.37, "anchura": 0.0, "altura": 0.0, "cantidad": 15.37},
                            {"comentario": "ESCALERA 1/2 PS - ESC. 2", "n": 1, "longitud": 16.20, "anchura": 0.0, "altura": 0.0, "cantidad": 16.20}
                        ]
                    },
                    {
                        "codigo": "PM.01.05.01.04.02",
                        "padre_capitulo": "PM.01.05.01.04 Forjados colaborantes",
                        "resumen": "FORJADO COLABORANTE, E=16cm (6+10), HA-25/B/20/XC1, SOBRE RASANTE",
                        "unidad": "m²",
                        "cantidad": 337.16,
                        "coste_unitario": 71.50,
                        "precio_venta_unitario": 99.50,
                        "descripcion": "Formación de forjado 16 cm de grueso total, con planchas colaborantes de acero galvanizado S320GD de espesor 1 mm. Incluye hormigón HA-25/B/20/XC1 fluido vertido con bomba, armadura en barras corrugadas B500S, mallazo electrosoldado B500S, anclajes con resina epoxi y conectores tipo Nelson soldados a perfiles. Medición sobre rasante en plantas TPB, TP1, TP2, TP3, TP4 y mesetas de escaleras.",
                        "mediciones": [
                            {"comentario": "TPB", "n": 1, "longitud": 15.0, "anchura": 0.0, "altura": 0.0, "cantidad": 15.00},
                            {"comentario": "TPB - ESC. 1", "n": 1, "longitud": 8.21, "anchura": 0.0, "altura": 0.0, "cantidad": 8.21},
                            {"comentario": "TPB - ESC. 2", "n": 1, "longitud": 10.80, "anchura": 0.0, "altura": 0.0, "cantidad": 10.80},
                            {"comentario": "TP1", "n": 1, "longitud": 15.0, "anchura": 0.0, "altura": 0.0, "cantidad": 15.00},
                            {"comentario": "TP1 - ESC. 1", "n": 1, "longitud": 8.21, "anchura": 0.0, "altura": 0.0, "cantidad": 8.21},
                            {"comentario": "TP1 - ESC. 2", "n": 1, "longitud": 10.80, "anchura": 0.0, "altura": 0.0, "cantidad": 10.80},
                            {"comentario": "TP2", "n": 1, "longitud": 15.0, "anchura": 0.0, "altura": 0.0, "cantidad": 15.00},
                            {"comentario": "TP2 - ESC. 1", "n": 1, "longitud": 8.21, "anchura": 0.0, "altura": 0.0, "cantidad": 8.21},
                            {"comentario": "TP2 - ESC. 2", "n": 1, "longitud": 10.80, "anchura": 0.0, "altura": 0.0, "cantidad": 10.80},
                            {"comentario": "TP3", "n": 1, "longitud": 15.0, "anchura": 0.0, "altura": 0.0, "cantidad": 15.00},
                            {"comentario": "TP3 - ESC. 1", "n": 1, "longitud": 8.21, "anchura": 0.0, "altura": 0.0, "cantidad": 8.21},
                            {"comentario": "TP3 - ESC. 2", "n": 1, "longitud": 10.80, "anchura": 0.0, "altura": 0.0, "cantidad": 10.80},
                            {"comentario": "TP4 - ESC. 1", "n": 1, "longitud": 27.41, "anchura": 0.0, "altura": 0.0, "cantidad": 27.41},
                            {"comentario": "TP4 - ESC. 2", "n": 1, "longitud": 35.81, "anchura": 0.0, "altura": 0.0, "cantidad": 35.81},
                            {"comentario": "ESCALERA 1/2 PB - ESC. 1", "n": 1, "longitud": 12.60, "anchura": 0.0, "altura": 0.0, "cantidad": 12.60},
                            {"comentario": "ESCALERA 1/2 PB - ESC. 2", "n": 1, "longitud": 19.40, "anchura": 0.0, "altura": 0.0, "cantidad": 19.40},
                            {"comentario": "ESCALERA 1/2 P1 - ESC. 1", "n": 1, "longitud": 10.30, "anchura": 0.0, "altura": 0.0, "cantidad": 10.30},
                            {"comentario": "ESCALERA 1/2 P1 - ESC. 2", "n": 1, "longitud": 25.00, "anchura": 0.0, "altura": 0.0, "cantidad": 25.00},
                            {"comentario": "ESCALERA 1/2 P2 - ESC. 1", "n": 1, "longitud": 10.30, "anchura": 0.0, "altura": 0.0, "cantidad": 10.30},
                            {"comentario": "ESCALERA 1/2 P2 - ESC. 2", "n": 1, "longitud": 25.00, "anchura": 0.0, "altura": 0.0, "cantidad": 25.00},
                            {"comentario": "ESCALERA 1/2 P3 - ESC. 1", "n": 1, "longitud": 10.30, "anchura": 0.0, "altura": 0.0, "cantidad": 10.30},
                            {"comentario": "ESCALERA 1/2 P3 - ESC. 2", "n": 1, "longitud": 25.00, "anchura": 0.0, "altura": 0.0, "cantidad": 25.00}
                        ]
                    }
                ]
            },
            {
                "codigo": "06.02",
                "nombre": "OBRA NUEVA",
                "partidas": [
                    {
                        "codigo": "EESA.1baaaaa.ST0",
                        "padre_capitulo": "06.02 OBRA NUEVA",
                        "resumen": "Suministro y montaje acero S 275 JR soldado e/soportes, vigas",
                        "unidad": "kg",
                        "cantidad": 1068.96,
                        "coste_unitario": 3.80,
                        "precio_venta_unitario": 5.35,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para perfiles formados por pieza simple en caliente serie UPN, L y T, trabajado en taller y con imprimación de taller + pintura de acabado en obra. Incluye placas de anclaje, conectores, retacado a estructura existente mediante mortero sin retracción y medios auxiliares. Aplicado en Cubierta P6 y Pasarela de acceso al ascensor.",
                        "mediciones": [
                            {"comentario": "Cubierta P6", "n": 1, "longitud": 26.6, "anchura": 0.0, "altura": 16.7, "cantidad": 444.22},
                            {"comentario": "Pasarela ascensor - L80.80.8", "n": 1, "longitud": 8.8, "anchura": 9.63, "altura": 0.0, "cantidad": 84.74},
                            {"comentario": "Pasarela ascensor - T80.9", "n": 5, "longitud": 2.0, "anchura": 10.7, "altura": 0.0, "cantidad": 107.00},
                            {"comentario": "Pasarela ascensor - T80.9", "n": 1, "longitud": 5.0, "anchura": 10.7, "altura": 0.0, "cantidad": 53.50},
                            {"comentario": "Pasarela ascensor - UPN200", "n": 1, "longitud": 15.0, "anchura": 25.3, "altura": 0.0, "cantidad": 379.50}
                        ]
                    }
                ]
            },
            {
                "codigo": "06.03",
                "nombre": "REFUERZOS ESTRUCTURALES",
                "partidas": [
                    {
                        "codigo": "P442-BR01",
                        "padre_capitulo": "06.03 REFUERZOS ESTRUCTURALES",
                        "resumen": "SUSTITUCIÓN FUNCIONAL JÁCENAS HA MEDIANTE VIGAS DE ACERO S275JR CONECTADAS",
                        "unidad": "kg",
                        "cantidad": 99219.23,
                        "coste_unitario": 3.30,
                        "precio_venta_unitario": 4.60,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para vigas formadas por pieza simple, en perfiles UPN laminados en caliente y planchas, trabajado en taller, colocado en obra bajo jácena existente con soldadura y/o tornillos. Conexión a la jácena mediante conectores definidos en proyecto y retacado continuo con mortero sin retracción en toda su longitud. Protección C1 con imprimación y pintura de acabado. EXC3 según Código Estructural.",
                        "mediciones": [
                            {"comentario": "TPSS - UPN-200", "n": 1, "longitud": 351.0, "anchura": 25.3, "altura": 0.0, "cantidad": 8880.30},
                            {"comentario": "TPSS - UPN-260", "n": 1, "longitud": 176.0, "anchura": 37.9, "altura": 0.0, "cantidad": 6670.40},
                            {"comentario": "TPSS - UPN-300", "n": 1, "longitud": 35.0, "anchura": 46.2, "altura": 0.0, "cantidad": 1617.00},
                            {"comentario": "TPB - UPN-200", "n": 1, "longitud": 441.0, "anchura": 25.3, "altura": 0.0, "cantidad": 11157.30},
                            {"comentario": "TPB - UPN-260", "n": 1, "longitud": 213.0, "anchura": 37.9, "altura": 0.0, "cantidad": 8072.70},
                            {"comentario": "TPB - UPN-300", "n": 1, "longitud": 10.0, "anchura": 46.2, "altura": 0.0, "cantidad": 462.00},
                            {"comentario": "TP1 - UPN-200", "n": 1, "longitud": 264.0, "anchura": 25.3, "altura": 0.0, "cantidad": 6679.20},
                            {"comentario": "TP1 - UPN-260", "n": 1, "longitud": 133.0, "anchura": 37.9, "altura": 0.0, "cantidad": 5040.70},
                            {"comentario": "TP1 - UPN-300", "n": 1, "longitud": 11.0, "anchura": 46.2, "altura": 0.0, "cantidad": 508.20},
                            {"comentario": "TP2 - UPN-200", "n": 1, "longitud": 261.0, "anchura": 25.3, "altura": 0.0, "cantidad": 6603.30},
                            {"comentario": "TP2 - UPN-260", "n": 1, "longitud": 134.0, "anchura": 37.9, "altura": 0.0, "cantidad": 5078.60},
                            {"comentario": "TP2 - UPN-300", "n": 1, "longitud": 11.0, "anchura": 46.2, "altura": 0.0, "cantidad": 508.20},
                            {"comentario": "TP3 - UPN-200", "n": 1, "longitud": 263.0, "anchura": 25.3, "altura": 0.0, "cantidad": 6653.90},
                            {"comentario": "TP3 - UPN-260", "n": 1, "longitud": 135.0, "anchura": 37.9, "altura": 0.0, "cantidad": 5116.50},
                            {"comentario": "TP3 - UPN-300", "n": 1, "longitud": 11.0, "anchura": 46.2, "altura": 0.0, "cantidad": 508.20},
                            {"comentario": "TP4 - UPN-200", "n": 1, "longitud": 309.0, "anchura": 25.3, "altura": 0.0, "cantidad": 7817.70},
                            {"comentario": "TP4 - UPN-260", "n": 1, "longitud": 91.0, "anchura": 37.9, "altura": 0.0, "cantidad": 3448.90},
                            {"comentario": "TP4 - UPN-300", "n": 1, "longitud": 11.0, "anchura": 46.2, "altura": 0.0, "cantidad": 508.20},
                            {"comentario": "TP5 - UPN-200", "n": 1, "longitud": 262.0, "anchura": 25.3, "altura": 0.0, "cantidad": 6628.60},
                            {"comentario": "TP5 - UPN-260", "n": 1, "longitud": 62.0, "anchura": 37.9, "altura": 0.0, "cantidad": 2349.80},
                            {"comentario": "TP5 - UPN-300", "n": 1, "longitud": 4.0, "anchura": 46.2, "altura": 0.0, "cantidad": 184.80},
                            {"comentario": "AJUSTE", "n": 1, "longitud": 4724.72, "anchura": 0.0, "altura": 0.0, "cantidad": 4724.72},
                            {"comentario": "AJUSTE FINO", "n": 1, "longitud": 0.01, "anchura": 0.0, "altura": 0.0, "cantidad": 0.01}
                        ]
                    },
                    {
                        "codigo": "P442-BA61",
                        "padre_capitulo": "06.03 REFUERZOS ESTRUCTURALES",
                        "resumen": "ESTRUCTURA HORIZONTAL INTERIOR SOPORTE PARTELUCES ACERO S275JR - PERFILES IP,HE,UP",
                        "unidad": "kg",
                        "cantidad": 56621.25,
                        "coste_unitario": 3.25,
                        "precio_venta_unitario": 4.50,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para vigas soporte de parteluces en plantas TPB a TP5, en perfiles IPE-200, 240, 270, 300 y HEB-220, trabajado en taller, colocado en obra con soldadura y tornillos. Tratamiento C1 de taller + acabado en obra. EXC3 según Código Estructural.",
                        "mediciones": [
                            {"comentario": "TPB - IPE-300", "n": 1, "longitud": 131.0, "anchura": 42.2, "altura": 0.0, "cantidad": 5528.20},
                            {"comentario": "TPB - IPE-200", "n": 1, "longitud": 20.0, "anchura": 22.4, "altura": 0.0, "cantidad": 448.00},
                            {"comentario": "TPB - IPE-270", "n": 1, "longitud": 102.0, "anchura": 36.1, "altura": 0.0, "cantidad": 3682.20},
                            {"comentario": "TPB - IPE-240", "n": 1, "longitud": 10.0, "anchura": 30.7, "altura": 0.0, "cantidad": 307.00},
                            {"comentario": "TP1 - IPE-300", "n": 1, "longitud": 82.0, "anchura": 42.2, "altura": 0.0, "cantidad": 3460.40},
                            {"comentario": "TP1 - IPE-200", "n": 1, "longitud": 20.0, "anchura": 22.4, "altura": 0.0, "cantidad": 448.00},
                            {"comentario": "TP1 - IPE-270", "n": 1, "longitud": 34.0, "anchura": 36.1, "altura": 0.0, "cantidad": 1227.40},
                            {"comentario": "TP1 - IPE-240", "n": 1, "longitud": 10.0, "anchura": 30.7, "altura": 0.0, "cantidad": 307.00},
                            {"comentario": "TP1 - HEB-220", "n": 1, "longitud": 54.0, "anchura": 71.5, "altura": 0.0, "cantidad": 3861.00},
                            {"comentario": "TP2 - IPE-300", "n": 1, "longitud": 82.0, "anchura": 42.2, "altura": 0.0, "cantidad": 3460.40},
                            {"comentario": "TP2 - IPE-200", "n": 1, "longitud": 20.0, "anchura": 22.4, "altura": 0.0, "cantidad": 448.00},
                            {"comentario": "TP2 - IPE-270", "n": 1, "longitud": 38.0, "anchura": 36.1, "altura": 0.0, "cantidad": 1371.80},
                            {"comentario": "TP2 - IPE-240", "n": 1, "longitud": 10.0, "anchura": 30.7, "altura": 0.0, "cantidad": 307.00},
                            {"comentario": "TP2 - HEB-220", "n": 1, "longitud": 54.0, "anchura": 71.5, "altura": 0.0, "cantidad": 3861.00},
                            {"comentario": "TP3 - IPE-300", "n": 1, "longitud": 82.0, "anchura": 42.2, "altura": 0.0, "cantidad": 3460.40},
                            {"comentario": "TP3 - IPE-200", "n": 1, "longitud": 20.0, "anchura": 22.4, "altura": 0.0, "cantidad": 448.00},
                            {"comentario": "TP3 - IPE-270", "n": 1, "longitud": 38.0, "anchura": 36.1, "altura": 0.0, "cantidad": 1371.80},
                            {"comentario": "TP3 - IPE-240", "n": 1, "longitud": 10.0, "anchura": 30.7, "altura": 0.0, "cantidad": 307.00},
                            {"comentario": "TP3 - HEB-220", "n": 1, "longitud": 54.0, "anchura": 71.5, "altura": 0.0, "cantidad": 3861.00},
                            {"comentario": "TP4 - IPE-300", "n": 1, "longitud": 82.0, "anchura": 42.2, "altura": 0.0, "cantidad": 3460.40},
                            {"comentario": "TP4 - IPE-200", "n": 1, "longitud": 20.0, "anchura": 22.4, "altura": 0.0, "cantidad": 448.00},
                            {"comentario": "TP4 - IPE-270", "n": 1, "longitud": 38.0, "anchura": 36.1, "altura": 0.0, "cantidad": 1371.80},
                            {"comentario": "TP4 - IPE-240", "n": 1, "longitud": 10.0, "anchura": 30.7, "altura": 0.0, "cantidad": 307.00},
                            {"comentario": "TP4 - HEB-220", "n": 1, "longitud": 54.0, "anchura": 71.5, "altura": 0.0, "cantidad": 3861.00},
                            {"comentario": "TP5 - IPE-300", "n": 1, "longitud": 39.0, "anchura": 42.2, "altura": 0.0, "cantidad": 1645.80},
                            {"comentario": "TP5 - IPE-200", "n": 1, "longitud": 20.0, "anchura": 22.4, "altura": 0.0, "cantidad": 448.00},
                            {"comentario": "TP5 - IPE-270", "n": 1, "longitud": 39.0, "anchura": 36.1, "altura": 0.0, "cantidad": 1407.90},
                            {"comentario": "TP5 - IPE-240", "n": 1, "longitud": 10.0, "anchura": 30.7, "altura": 0.0, "cantidad": 307.00},
                            {"comentario": "TP5 - HEB-220", "n": 1, "longitud": 35.0, "anchura": 71.5, "altura": 0.0, "cantidad": 2502.50},
                            {"comentario": "AJUSTE", "n": 2696.25, "longitud": 0.0, "anchura": 0.0, "altura": 0.0, "cantidad": 2696.25}
                        ]
                    },
                    {
                        "codigo": "P442-BR51",
                        "padre_capitulo": "06.03 REFUERZOS ESTRUCTURALES",
                        "resumen": "REFUERZO PARTELUCES ESTRUCTURA HORIZONTAL INTERIOR FORJ. UNIDIRECC. MEDIANTE VIGAS DE ACERO S275JR",
                        "unidad": "kg",
                        "cantidad": 21097.44,
                        "coste_unitario": 3.35,
                        "precio_venta_unitario": 4.65,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para vigas de refuerzo de parteluces en forjado unidireccional en perfiles IPE-200, colocado con soldadura/tornillos y retacado con mortero sin retracción en los apoyos de las viguetas existentes en plantas TPB a TP5. Clase EXC3.",
                        "mediciones": [
                            {"comentario": "TPB - IPE-200", "n": 1, "longitud": 228.0, "anchura": 22.4, "altura": 0.0, "cantidad": 5107.20},
                            {"comentario": "TP1 - IPE-200", "n": 1, "longitud": 140.0, "anchura": 22.4, "altura": 0.0, "cantidad": 3136.00},
                            {"comentario": "TP2 - IPE-200", "n": 1, "longitud": 140.0, "anchura": 22.4, "altura": 0.0, "cantidad": 3136.00},
                            {"comentario": "TP3 - IPE-200", "n": 1, "longitud": 140.0, "anchura": 22.4, "altura": 0.0, "cantidad": 3136.00},
                            {"comentario": "TP4 - IPE-200", "n": 1, "longitud": 140.0, "anchura": 22.4, "altura": 0.0, "cantidad": 3136.00},
                            {"comentario": "TP5 - IPE-200", "n": 1, "longitud": 109.0, "anchura": 22.4, "altura": 0.0, "cantidad": 2441.60},
                            {"comentario": "AJUSTE", "n": 1004.64, "longitud": 0.0, "anchura": 0.0, "altura": 0.0, "cantidad": 1004.64}
                        ]
                    },
                    {
                        "codigo": "P44C-BR01",
                        "padre_capitulo": "06.03 REFUERZOS ESTRUCTURALES",
                        "resumen": "REFUERZO PILARES HA MEDIANTE PERFILES DE ACERO S275JR CONECTADOS",
                        "unidad": "kg",
                        "cantidad": 50618.09,
                        "coste_unitario": 3.50,
                        "precio_venta_unitario": 4.85,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para refuerzo de pilares de hormigón armado existentes mediante perfiles UPN (UPN 100 a UPN 260) conectados al fuste existente con conectores mecánicos y varillas roscadas M16 con resina epoxi de baja viscosidad y retacado perimetral con mortero sin retracción en toda su longitud. Ejecutado en plantas PS, PB, P1 a P5. Clase EXC3.",
                        "mediciones": [
                            {"comentario": "PS - UPN 120", "n": 12, "longitud": 3.0, "anchura": 13.4, "altura": 0.0, "cantidad": 482.40},
                            {"comentario": "PS - UPN 180", "n": 8, "longitud": 3.0, "anchura": 22.0, "altura": 0.0, "cantidad": 528.00},
                            {"comentario": "PS - UPN 200", "n": 98, "longitud": 3.0, "anchura": 25.3, "altura": 0.0, "cantidad": 7438.20},
                            {"comentario": "PS - UPN 240", "n": 6, "longitud": 3.0, "anchura": 33.2, "altura": 0.0, "cantidad": 597.60},
                            {"comentario": "PS - UPN 260", "n": 24, "longitud": 3.0, "anchura": 37.9, "altura": 0.0, "cantidad": 2728.80},
                            {"comentario": "PB - UPN 100", "n": 12, "longitud": 3.5, "anchura": 10.6, "altura": 0.0, "cantidad": 445.20},
                            {"comentario": "PB - UPN 140", "n": 6, "longitud": 3.5, "anchura": 16.0, "altura": 0.0, "cantidad": 336.00},
                            {"comentario": "PB - UPN 160", "n": 8, "longitud": 3.5, "anchura": 18.8, "altura": 0.0, "cantidad": 526.40},
                            {"comentario": "PB - UPN 180", "n": 4, "longitud": 3.5, "anchura": 22.0, "altura": 0.0, "cantidad": 308.00},
                            {"comentario": "PB - UPN 200", "n": 114, "longitud": 3.5, "anchura": 25.3, "altura": 0.0, "cantidad": 10094.70},
                            {"comentario": "PB - UPN 240", "n": 4, "longitud": 3.5, "anchura": 33.2, "altura": 0.0, "cantidad": 464.80},
                            {"comentario": "PB - UPN 260", "n": 4, "longitud": 3.5, "anchura": 37.9, "altura": 0.0, "cantidad": 530.60},
                            {"comentario": "P1 - UPN 120", "n": 8, "longitud": 3.0, "anchura": 13.4, "altura": 0.0, "cantidad": 321.60},
                            {"comentario": "P1 - UPN 140", "n": 6, "longitud": 3.0, "anchura": 16.0, "altura": 0.0, "cantidad": 288.00},
                            {"comentario": "P1 - UPN 160", "n": 2, "longitud": 3.0, "anchura": 18.8, "altura": 0.0, "cantidad": 112.80},
                            {"comentario": "P1 - UPN 180", "n": 4, "longitud": 3.0, "anchura": 22.0, "altura": 0.0, "cantidad": 264.00},
                            {"comentario": "P1 - UPN 200", "n": 60, "longitud": 3.0, "anchura": 25.3, "altura": 0.0, "cantidad": 4554.00},
                            {"comentario": "P2 - UPN 100", "n": 6, "longitud": 3.0, "anchura": 10.6, "altura": 0.0, "cantidad": 190.80},
                            {"comentario": "P2 - UPN 120", "n": 10, "longitud": 3.0, "anchura": 13.4, "altura": 0.0, "cantidad": 402.00},
                            {"comentario": "P2 - UPN 140", "n": 4, "longitud": 3.0, "anchura": 16.0, "altura": 0.0, "cantidad": 192.00},
                            {"comentario": "P2 - UPN 160", "n": 4, "longitud": 3.0, "anchura": 18.8, "altura": 0.0, "cantidad": 225.60},
                            {"comentario": "P2 - UPN 200", "n": 54, "longitud": 3.0, "anchura": 25.3, "altura": 0.0, "cantidad": 4098.60},
                            {"comentario": "P3 - UPN 100", "n": 12, "longitud": 3.0, "anchura": 10.6, "altura": 0.0, "cantidad": 381.60},
                            {"comentario": "P3 - UPN 120", "n": 8, "longitud": 3.0, "anchura": 13.4, "altura": 0.0, "cantidad": 321.60},
                            {"comentario": "P3 - UPN 140", "n": 4, "longitud": 3.0, "anchura": 16.0, "altura": 0.0, "cantidad": 192.00},
                            {"comentario": "P3 - UPN 160", "n": 14, "longitud": 3.0, "anchura": 18.8, "altura": 0.0, "cantidad": 789.60},
                            {"comentario": "P3 - UPN 200", "n": 38, "longitud": 3.0, "anchura": 25.3, "altura": 0.0, "cantidad": 2884.20},
                            {"comentario": "P4 - UPN 100", "n": 16, "longitud": 3.0, "anchura": 10.6, "altura": 0.0, "cantidad": 508.80},
                            {"comentario": "P4 - UPN 120", "n": 12, "longitud": 3.0, "anchura": 13.4, "altura": 0.0, "cantidad": 482.40},
                            {"comentario": "P4 - UPN 160", "n": 18, "longitud": 3.0, "anchura": 18.8, "altura": 0.0, "cantidad": 1015.20},
                            {"comentario": "P4 - UPN 200", "n": 40, "longitud": 3.0, "anchura": 25.3, "altura": 0.0, "cantidad": 3036.00},
                            {"comentario": "P5 - UPN 100", "n": 12, "longitud": 3.0, "anchura": 10.6, "altura": 0.0, "cantidad": 381.60},
                            {"comentario": "P5 - UPN 120", "n": 8, "longitud": 3.0, "anchura": 13.4, "altura": 0.0, "cantidad": 321.60},
                            {"comentario": "P5 - UPN 160", "n": 14, "longitud": 3.0, "anchura": 18.8, "altura": 0.0, "cantidad": 789.60},
                            {"comentario": "P5 - UPN 200", "n": 26, "longitud": 3.0, "anchura": 25.3, "altura": 0.0, "cantidad": 1973.40},
                            {"comentario": "AJUSTE", "n": 1, "longitud": 2410.38, "anchura": 0.0, "altura": 0.0, "cantidad": 2410.38},
                            {"comentario": "AJUSTE FINO", "n": 1, "longitud": 0.01, "anchura": 0.0, "altura": 0.0, "cantidad": 0.01}
                        ]
                    },
                    {
                        "codigo": "P44C-BR02",
                        "padre_capitulo": "06.03 REFUERZOS ESTRUCTURALES",
                        "resumen": "REFUERZO PILARES HA MEDIANTE EMPRESILLADO DE PERFILES DE ACERO S275JR",
                        "unidad": "kg",
                        "cantidad": 55953.77,
                        "coste_unitario": 3.65,
                        "precio_venta_unitario": 5.10,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para refuerzo de fuste de pilares existentes mediante empresillado compuesto con 4 perfiles angulares (L 80.8, L100.10 y L120.12) soldados con pletinas intermedias cada 40 cm y retacado interior y continuo con mortero sin retracción. Con imprimación antioxidante de taller y pintura de acabado en obra. EXC3 según Código Estructural.",
                        "mediciones": [
                            {"comentario": "PSS - L 80.8", "n": 72, "longitud": 3.0, "anchura": 9.63, "altura": 0.0, "cantidad": 2080.08},
                            {"comentario": "PSS - L 100.10", "n": 46, "longitud": 3.0, "anchura": 15.0, "altura": 0.0, "cantidad": 2070.00},
                            {"comentario": "PSS - L 120.12", "n": 131, "longitud": 3.0, "anchura": 21.6, "altura": 0.0, "cantidad": 8488.80},
                            {"comentario": "PB - L 80.8", "n": 72, "longitud": 3.5, "anchura": 9.63, "altura": 0.0, "cantidad": 2426.76},
                            {"comentario": "PB - L 100.10", "n": 88, "longitud": 3.5, "anchura": 15.0, "altura": 0.0, "cantidad": 4620.00},
                            {"comentario": "PB - L 120.12", "n": 98, "longitud": 3.5, "anchura": 21.6, "altura": 0.0, "cantidad": 7408.80},
                            {"comentario": "P1 - L 80.8", "n": 12, "longitud": 3.0, "anchura": 9.63, "altura": 0.0, "cantidad": 346.68},
                            {"comentario": "P1 - L 100.10", "n": 92, "longitud": 3.0, "anchura": 15.0, "altura": 0.0, "cantidad": 4140.00},
                            {"comentario": "P1 - L 120.12", "n": 48, "longitud": 3.0, "anchura": 21.6, "altura": 0.0, "cantidad": 3110.40},
                            {"comentario": "P2 - L 80.8", "n": 32, "longitud": 3.0, "anchura": 9.63, "altura": 0.0, "cantidad": 924.48},
                            {"comentario": "P2 - L 100.10", "n": 96, "longitud": 3.0, "anchura": 15.0, "altura": 0.0, "cantidad": 4320.00},
                            {"comentario": "P2 - L 120.12", "n": 16, "longitud": 3.0, "anchura": 21.6, "altura": 0.0, "cantidad": 1036.80},
                            {"comentario": "P3 - L 80.8", "n": 84, "longitud": 3.0, "anchura": 9.63, "altura": 0.0, "cantidad": 2426.76},
                            {"comentario": "P3 - L 100.10", "n": 52, "longitud": 3.0, "anchura": 15.0, "altura": 0.0, "cantidad": 2340.00},
                            {"comentario": "P3 - L 120.12", "n": 8, "longitud": 3.0, "anchura": 21.6, "altura": 0.0, "cantidad": 518.40},
                            {"comentario": "P4 - L 80.8", "n": 110, "longitud": 3.0, "anchura": 9.63, "altura": 0.0, "cantidad": 3177.90},
                            {"comentario": "P4 - L 100.10", "n": 24, "longitud": 3.0, "anchura": 15.0, "altura": 0.0, "cantidad": 1080.00},
                            {"comentario": "P5 - L 80.8", "n": 96, "longitud": 3.0, "anchura": 9.63, "altura": 0.0, "cantidad": 2773.44},
                            {"comentario": "AJUSTE", "n": 1, "longitud": 2664.46, "anchura": 0.0, "altura": 0.0, "cantidad": 2664.46},
                            {"comentario": "AJUSTE FINO", "n": 1, "longitud": 0.01, "anchura": 0.0, "altura": 0.0, "cantidad": 0.01}
                        ]
                    },
                    {
                        "codigo": "P44C-BR21",
                        "padre_capitulo": "06.03 REFUERZOS ESTRUCTURALES",
                        "resumen": "CAPITEL DE ACERO DE 2 JÁCENAS MEDIANTE PERFILES DE ACERO S275JR RETACADOS Y/O CONECTADOS",
                        "unidad": "kg",
                        "cantidad": 44826.60,
                        "coste_unitario": 3.70,
                        "precio_venta_unitario": 5.15,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para capiteles de nudos pilar-viga con encuentro de 2 jácenas, formados por pieza compuesta en perfiles UPN, angulares L y planchas retacadas y conectadas a la estructura existente mediante varillas químicas M16/M20 y mortero sin retracción. Imprimación y pintura C1. Clase EXC3.",
                        "mediciones": [
                            {"comentario": "PS - Tipo 1", "n": 43, "longitud": 176.0, "anchura": 0.0, "altura": 0.0, "cantidad": 7568.00},
                            {"comentario": "PS - Tipo 2", "n": 44, "longitud": 88.0, "anchura": 0.0, "altura": 0.0, "cantidad": 3872.00},
                            {"comentario": "PB - Tipo 1", "n": 43, "longitud": 176.0, "anchura": 0.0, "altura": 0.0, "cantidad": 7568.00},
                            {"comentario": "PB - Tipo 2", "n": 44, "longitud": 88.0, "anchura": 0.0, "altura": 0.0, "cantidad": 3872.00},
                            {"comentario": "P1 - Tipo 1", "n": 21, "longitud": 136.0, "anchura": 0.0, "altura": 0.0, "cantidad": 2856.00},
                            {"comentario": "P1 - Tipo 2", "n": 26, "longitud": 68.0, "anchura": 0.0, "altura": 0.0, "cantidad": 1768.00},
                            {"comentario": "P2 - Tipo 1", "n": 21, "longitud": 136.0, "anchura": 0.0, "altura": 0.0, "cantidad": 2856.00},
                            {"comentario": "P2 - Tipo 2", "n": 26, "longitud": 68.0, "anchura": 0.0, "altura": 0.0, "cantidad": 1768.00},
                            {"comentario": "P3 - Tipo 1", "n": 21, "longitud": 136.0, "anchura": 0.0, "altura": 0.0, "cantidad": 2856.00},
                            {"comentario": "P3 - Tipo 2", "n": 26, "longitud": 68.0, "anchura": 0.0, "altura": 0.0, "cantidad": 1768.00},
                            {"comentario": "P4 - Tipo 1", "n": 21, "longitud": 108.0, "anchura": 0.0, "altura": 0.0, "cantidad": 2268.00},
                            {"comentario": "P4 - Tipo 2", "n": 26, "longitud": 54.0, "anchura": 0.0, "altura": 0.0, "cantidad": 1404.00},
                            {"comentario": "P5 - Tipo 1", "n": 14, "longitud": 108.0, "anchura": 0.0, "altura": 0.0, "cantidad": 1512.00},
                            {"comentario": "P5 - Tipo 2", "n": 14, "longitud": 54.0, "anchura": 0.0, "altura": 0.0, "cantidad": 756.00},
                            {"comentario": "AJUSTE", "n": 2134.60, "longitud": 0.0, "anchura": 0.0, "altura": 0.0, "cantidad": 2134.60}
                        ]
                    },
                    {
                        "codigo": "P44C-BR22",
                        "padre_capitulo": "06.03 REFUERZOS ESTRUCTURALES",
                        "resumen": "CAPITEL DE ACERO DE 3 JÁCENAS MEDIANTE PERFILES DE ACERO S275JR RETACADOS Y/O CONECTADOS",
                        "unidad": "kg",
                        "cantidad": 25477.20,
                        "coste_unitario": 3.80,
                        "precio_venta_unitario": 5.30,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para capiteles de nudos pilar-viga con encuentro de 3 jácenas en perfiles UPN, planchas y angulares, conectado con varillas mecánicas y químicas y mortero sin retracción. En plantas PS a P5. Clase EXC3.",
                        "mediciones": [
                            {"comentario": "PS", "n": 28, "longitud": 176.0, "anchura": 0.0, "altura": 0.0, "cantidad": 4928.00},
                            {"comentario": "PB", "n": 26, "longitud": 176.0, "anchura": 0.0, "altura": 0.0, "cantidad": 4576.00},
                            {"comentario": "P1", "n": 24, "longitud": 136.0, "anchura": 0.0, "altura": 0.0, "cantidad": 3264.00},
                            {"comentario": "P2", "n": 24, "longitud": 136.0, "anchura": 0.0, "altura": 0.0, "cantidad": 3264.00},
                            {"comentario": "P3", "n": 24, "longitud": 136.0, "anchura": 0.0, "altura": 0.0, "cantidad": 3264.00},
                            {"comentario": "P4", "n": 22, "longitud": 108.0, "anchura": 0.0, "altura": 0.0, "cantidad": 2376.00},
                            {"comentario": "P5", "n": 24, "longitud": 108.0, "anchura": 0.0, "altura": 0.0, "cantidad": 2592.00},
                            {"comentario": "AJUSTE", "n": 1213.20, "longitud": 0.0, "anchura": 0.0, "altura": 0.0, "cantidad": 1213.20}
                        ]
                    },
                    {
                        "codigo": "P44C-BR23",
                        "padre_capitulo": "06.03 REFUERZOS ESTRUCTURALES",
                        "resumen": "CAPITEL DE ACERO DE 4 JÁCENAS MEDIANTE PERFILES DE ACERO S275JR RETACADOS Y/O CONECTADOS",
                        "unidad": "kg",
                        "cantidad": 6287.40,
                        "coste_unitario": 3.90,
                        "precio_venta_unitario": 5.45,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para capiteles de nudos pilar-viga centrales en cruz con encuentro de 4 jácenas, perfiles UPN, cartelas y planchas rigidizadoras conectadas y retacadas con mortero sin retracción. En plantas PS a P5. Clase EXC3.",
                        "mediciones": [
                            {"comentario": "PS", "n": 8, "longitud": 176.0, "anchura": 0.0, "altura": 0.0, "cantidad": 1408.00},
                            {"comentario": "PB", "n": 10, "longitud": 176.0, "anchura": 0.0, "altura": 0.0, "cantidad": 1760.00},
                            {"comentario": "P1", "n": 4, "longitud": 136.0, "anchura": 0.0, "altura": 0.0, "cantidad": 544.00},
                            {"comentario": "P2", "n": 4, "longitud": 136.0, "anchura": 0.0, "altura": 0.0, "cantidad": 544.00},
                            {"comentario": "P3", "n": 4, "longitud": 136.0, "anchura": 0.0, "altura": 0.0, "cantidad": 544.00},
                            {"comentario": "P4", "n": 7, "longitud": 108.0, "anchura": 0.0, "altura": 0.0, "cantidad": 756.00},
                            {"comentario": "P5", "n": 4, "longitud": 108.0, "anchura": 0.0, "altura": 0.0, "cantidad": 432.00},
                            {"comentario": "AJUSTE", "n": 299.40, "longitud": 0.0, "anchura": 0.0, "altura": 0.0, "cantidad": 299.40}
                        ]
                    },
                    {
                        "codigo": "P44C-BR31",
                        "padre_capitulo": "06.03 REFUERZOS ESTRUCTURALES",
                        "resumen": "PLACA DE ANCLAJE DE EMPRESILLADOS MEDIANTE PERFILES DE ACERO S275JR RETACADOS Y/O CONECTADOS",
                        "unidad": "kg",
                        "cantidad": 6640.70,
                        "coste_unitario": 4.15,
                        "precio_venta_unitario": 5.75,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para collarines y placas de base de arranque de empresillados a cimentación existente (sección 2-2' de planos ER.05.01), formados por angulares LPN 120.12, conectores químicos M16 y retacado con mortero sin retracción. Protección C4 en elementos enterrados. Clase EXC3.",
                        "mediciones": [
                            {"comentario": "CIM - Placas y collarines", "n": 122, "longitud": 2.4, "anchura": 21.6, "altura": 0.0, "cantidad": 6324.48},
                            {"comentario": "AJUSTE", "n": 316.22, "longitud": 0.0, "anchura": 0.0, "altura": 0.0, "cantidad": 316.22}
                        ]
                    },
                    {
                        "codigo": "P44C-BR32",
                        "padre_capitulo": "06.03 REFUERZOS ESTRUCTURALES",
                        "resumen": "PLACA DE ANCLAJE DE EMPRESILLADOS A MURO DE FÁBRICA M/ PERFILES DE ACERO RETACADOS CONECTADOS",
                        "unidad": "kg",
                        "cantidad": 2080.80,
                        "coste_unitario": 4.05,
                        "precio_venta_unitario": 5.65,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para placas y pletinas de conexión de empresillados a muros de fábrica existentes con conectores químicos, pernos pasantes y mortero sin retracción. En plantas PS a P5. Clase EXC3.",
                        "mediciones": [
                            {"comentario": "PS - Pilares a muro", "n": 20, "longitud": 3.0, "anchura": 5.1, "altura": 0.0, "cantidad": 306.00},
                            {"comentario": "PB - Pilares a muro", "n": 20, "longitud": 3.0, "anchura": 5.1, "altura": 0.0, "cantidad": 306.00},
                            {"comentario": "P1 - Pilares a muro", "n": 20, "longitud": 3.0, "anchura": 5.1, "altura": 0.0, "cantidad": 306.00},
                            {"comentario": "P2 - Pilares a muro", "n": 20, "longitud": 3.0, "anchura": 5.1, "altura": 0.0, "cantidad": 306.00},
                            {"comentario": "P3 - Pilares a muro", "n": 20, "longitud": 3.0, "anchura": 5.1, "altura": 0.0, "cantidad": 306.00},
                            {"comentario": "P4 - Pilares a muro", "n": 20, "longitud": 3.0, "anchura": 5.1, "altura": 0.0, "cantidad": 306.00},
                            {"comentario": "P5 - Pilares a muro", "n": 16, "longitud": 3.0, "anchura": 5.1, "altura": 0.0, "cantidad": 244.80}
                        ]
                    },
                    {
                        "codigo": "P442-BR21",
                        "padre_capitulo": "06.03 REFUERZOS ESTRUCTURALES",
                        "resumen": "REFUERZO PILARES DE ACERO INTERIORES MEDIANTE PLETINAS DE ACERO S275JR SOLDADAS",
                        "unidad": "kg",
                        "cantidad": 257.04,
                        "coste_unitario": 4.35,
                        "precio_venta_unitario": 6.00,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para refuerzo de pilares existentes de acero formados por pieza compuesta, en pletinas laminadas soldadas longitudinalmente al fuste de perfiles HEB-180 en Planta Semisótano (PS). Clase EXC2.",
                        "mediciones": [
                            {"comentario": "PS - Pletinas HEB-180", "n": 4, "longitud": 3.6, "anchura": 17.0, "altura": 0.0, "cantidad": 244.80},
                            {"comentario": "AJUSTE", "n": 12.24, "longitud": 0.0, "anchura": 0.0, "altura": 0.0, "cantidad": 12.24}
                        ]
                    },
                    {
                        "codigo": "01.04.20.03",
                        "padre_capitulo": "06.03 REFUERZOS ESTRUCTURALES",
                        "resumen": "REFUERZO NUEVOS NERVIOS HA FORJADO UNIDIRECCIONAL MEDIANTE VIGAS DE ACERO S275JR",
                        "unidad": "kg",
                        "cantidad": 2445.87,
                        "coste_unitario": 3.45,
                        "precio_venta_unitario": 4.80,
                        "descripcion": "Acero S275JR según UNE-EN 10025-2, para vigas formadas por perfiles HEB-200 retacadas con mortero sin retracción en toda su longitud, colocadas en plantas TPSS y TPB para refuerzo de nuevos nervios de hormigón armado. Clase EXC3.",
                        "mediciones": [
                            {"comentario": "TPSS - HEB-200 (L=5.5 m)", "n": 2, "longitud": 5.5, "anchura": 61.3, "altura": 0.0, "cantidad": 674.30},
                            {"comentario": "TPSS - HEB-200 (L=4.0 m)", "n": 2, "longitud": 4.0, "anchura": 61.3, "altura": 0.0, "cantidad": 490.40},
                            {"comentario": "TPB - HEB-200 (L=5.5 m)", "n": 2, "longitud": 5.5, "anchura": 61.3, "altura": 0.0, "cantidad": 674.30},
                            {"comentario": "TPB - HEB-200 (L=4.0 m)", "n": 2, "longitud": 4.0, "anchura": 61.3, "altura": 0.0, "cantidad": 490.40},
                            {"comentario": "AJUSTE", "n": 116.47, "longitud": 0.0, "anchura": 0.0, "altura": 0.0, "cantidad": 116.47}
                        ]
                    }
                ]
            }
        ]
    }

    # Calcular totales
    total_coste = 0.0
    total_venta = 0.0
    total_kg_acero = 0.0
    total_m2_forjado = 0.0

    for sub in raw_data["subcapitulos"]:
        sub_coste = 0.0
        sub_venta = 0.0
        for p in sub["partidas"]:
            imp_venta = round(p["cantidad"] * p["precio_venta_unitario"], 2)
            imp_coste = round(p["cantidad"] * p["coste_unitario"], 2)
            p["importe_venta"] = imp_venta
            p["importe_coste"] = imp_coste
            p["margen_bruto"] = round(imp_venta - imp_coste, 2)
            p["margen_porcentaje"] = round((p["margen_bruto"] / imp_venta) * 100, 2) if imp_venta > 0 else 0.0
            
            sub_coste += imp_coste
            sub_venta += imp_venta
            
            if p["unidad"] == "kg":
                total_kg_acero += p["cantidad"]
            elif p["unidad"] == "m²":
                total_m2_forjado += p["cantidad"]

        sub["subtotal_coste"] = round(sub_coste, 2)
        sub["subtotal_venta"] = round(sub_venta, 2)
        sub["subtotal_margen"] = round(sub_venta - sub_coste, 2)
        sub["subtotal_margen_porcentaje"] = round((sub["subtotal_margen"] / sub_venta) * 100, 2) if sub_venta > 0 else 0.0

        total_coste += sub_coste
        total_venta += sub_venta

    iva_pct = 21.0
    iva_imp = round(total_venta * (iva_pct / 100.0), 2)
    tot_con_iva = round(total_venta + iva_imp, 2)
    margen_tot = round(total_venta - total_coste, 2)
    margen_pct = round((margen_tot / total_venta) * 100, 2) if total_venta > 0 else 0.0

    raw_data["totales"] = {
        "total_kg_acero": round(total_kg_acero, 2),
        "total_m2_forjado": round(total_m2_forjado, 2),
        "coste_directo_total": round(total_coste, 2),
        "base_imponible": round(total_venta, 2),
        "iva_porcentaje": iva_pct,
        "iva_importe": iva_imp,
        "total_con_iva": tot_con_iva,
        "margen_bruto_total": margen_tot,
        "margen_porcentaje_sobre_venta": margen_pct
    }

    out_path = os.path.join(BASE_DIR, "datos.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)
    print(f"datos.json generado en: {out_path}")
    return raw_data

if __name__ == "__main__":
    build_data()
