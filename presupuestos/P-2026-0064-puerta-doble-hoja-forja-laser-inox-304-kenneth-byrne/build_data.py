import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA = {
    "codigo": "P-2026-0064",
    "referencia": "PRE-2026-1123-PUERTA-FORJA-INOX-BYRNE",
    "estado_presupuesto": "ORIENTATIVO — Sujeto a visita técnica en propiedad y toma de medidas definitivas",
    "fecha": "23 de noviembre de 2026",
    "validez_dias": 30,
    "forma_pago": "100% a la aceptación del presupuesto definitivo (tras visita técnica de medición y confirmación en obra)",
    "plazo_entrega": "4 a 5 semanas desde la visita de medición, confirmación de medidas definitivas y aprobación del diseño CAD",
    "calidad_base": "Acero Inoxidable AISI 304 (EN 1.4301) con adornos tipo forja cortados con láser CNC en placa de 10 mm y acabado negro bicomponente exterior",
    "calidad_alternativa": "Acero Inoxidable AISI 316 (EN 1.4401) Calidad Marina para primera línea de mar / exposición salina severa C5-M",
    "cliente": {
        "nombre": "Kenneth Byrne",
        "cif": "Pendiente de facilitar en aceptación",
        "domicilio": "Propiedad particular en Menorca (dirección exacta pendiente de visita técnica)",
        "contacto": "Kenneth Byrne",
        "obra": "Puerta exterior abatible de doble hoja estilo forja clásica en acero inoxidable acabado negro",
        "ubicacion": "Menorca (Illes Balears)"
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
        "titulo": "Puerta Exterior Abatible de Doble Hoja Estilo Forja Clásica (≈ 1,83 × 1,52/1,83 m) en Acero Inoxidable AISI 304 con Adornos en Placa de 10 mm Cortados con Láser CNC y Acabado Negro Exterior",
        "medidas_aprox": {
            "ancho_total": "≈ 1,83 m (dos hojas simétricas de aprox. 0,91 m cada una)",
            "altura_laterales": "≈ 1,52 m",
            "altura_centro": "≈ 1,83 m (incluyendo arco y crestería decorativa superior)"
        },
        "pesos_estimados": {
            "peso_hoja_kg": 57.0,
            "peso_total_conjunto_kg": 114.0,
            "peso_neto_laser_10mm_kg": 50.0,
            "peso_bruto_chapa_10mm_kg": 138.0
        },
        "justificacion_menorca": "En lugar de hierro negro o forja convencional —que en el ambiente húmedo y salino de Menorca termina oxidándose en juntas y aristas—, proponemos fabricar íntegramente la puerta en acero inoxidable AISI 304 y cortar todos los adornos estilo forja en placa maciza inoxidable de 10 mm mediante láser CNC. Con el tratamiento de imprimación epoxi especial para inoxidable y dos manos de esmalte poliuretano alifático bicomponente negro exterior, se obtiene exactamente la estética clásica y robusta de la forja tradicional sin riesgo de corrosión estructural ni exfoliación de óxido. Si la propiedad estuviera en primera línea de mar o con exposición salina muy severa (C5-M), valoraremos en la visita la conveniencia de fabricar en calidad marina AISI 316.",
        "especificaciones_tecnicas": [
            "Bastidores perimetrales de hojas en tubo cuadrado de acero inoxidable AISI 304 de 40×40×2 mm con arcos superiores curvados en taller.",
            "Arco intermedio interior en tubo rectangular inoxidable AISI 304 de 40×20×2 mm y 12 barrotes verticales en barra cuadrada maciza de 14×14 mm AISI 304.",
            "Adornos clásicos tipo forja (crestería superior con remate central tipo flor de lis, cenefa curva entre arcos, rizos superiores, friso inferior de anillas y zócalos inferiores de volutas) cortados con láser CNC de alta precisión en placa maciza de acero inoxidable AISI 304 de 10 mm de espesor.",
            "Jambas laterales de fijación en perfil inoxidable con anclajes químicos de varilla roscada M10/M12 en acero inoxidable A4.",
            "Soldadura TIG bajo atmósfera de argón puro, repasado limpio de cordones visibles y decapado/pasivado químico completo.",
            "Herrajes completos en acero inoxidable: 6 bisagras reforzadas regulables (3 por hoja), cerradura exterior inoxidable con bombín europeo y 3 llaves, manilla/tirador, pasador vertical de bloqueo al suelo y tope/cazoleta inoxidable.",
            "Sistema de acabado negro exterior en taller: desengrasado y matizado mecánico/químico del acero inoxidable, aplicación de imprimación epoxi fosfatante de alta adherencia y dos capas de esmalte poliuretano alifático bicomponente negro RAL 9005 (satinado, mate o efecto forja fina)."
        ]
    },
    "partidas_cliente": [
        {
            "id": "01",
            "concepto": "Visita técnica de replanteo en propiedad y desarrollo de diseño CAD/CAM de forja decorativa",
            "descripcion": "Desplazamiento a la propiedad en Menorca para toma de medidas definitivas entre pilares, verificación de plomos, nivelación de suelo y evaluación del grado de exposición ambiental. Desarrollo de planos de fabricación y vectorización CAD/DXF del diseño clásico de forja para su aprobación previa por el cliente.",
            "unidad": "lote",
            "cantidad": 1,
            "precio_unitario": 350.00,
            "subtotal": 350.00
        },
        {
            "id": "02",
            "concepto": "Fabricación a medida de puerta abatible de doble hoja (≈ 1,83 × 1,52/1,83 m) en Acero Inoxidable AISI 304 con adornos tipo forja cortados con láser CNC en placa de 10 mm",
            "descripcion": "Suministro de perfiles y fabricación en taller mediante soldadura TIG de dos hojas simétricas (~0,91 m/hoja) con bastidor en tubo inox AISI 304 40×40×2 mm curvado en arco, arco interior en tubo 40×20×2 mm, 12 barrotes macizos de 14×14 mm, jambas de fijación y conjunto integral de ornamentos clásicos tipo forja (crestería con remate central, cenefas curvas, rizos, anillas y zócalos de volutas) cortados con láser CNC en placa maciza de acero inoxidable AISI 304 de 10 mm de espesor. Incluye desbarbado fino de cantos, decapado y pasivado químico de soldaduras y premontaje de ajuste.",
            "unidad": "conj",
            "cantidad": 1,
            "precio_unitario": 4950.00,
            "subtotal": 4950.00
        },
        {
            "id": "03",
            "concepto": "Conjunto completo de herrajes, cerradura exterior y anclajes químicos en Acero Inoxidable",
            "descripcion": "Suministro y montaje en taller de 6 bisagras reforzadas regulables de acero inoxidable (3 por hoja, aptas para alto peso), cerradura exterior inoxidable con bombín de perfil europeo y 3 llaves, manilla/tirador en acabado coordinado, pasador vertical de sujeción de hoja pasiva, tope/cazoleta de suelo inoxidable y anclajes químicos con varillas roscadas M10/M12 en acero inoxidable A4.",
            "unidad": "lote",
            "cantidad": 1,
            "precio_unitario": 580.00,
            "subtotal": 580.00
        },
        {
            "id": "04",
            "concepto": "Tratamiento superficial y acabado negro exterior bicomponente en taller",
            "descripcion": "Preparación integral del acero inoxidable mediante desengrasado profundo y matizado superficial para asegurar anclaje mecánico y químico, aplicación de imprimación epoxi fosfatante especial adherencia sobre inoxidable y dos capas de acabado con esmalte poliuretano alifático bicomponente negro exterior (RAL 9005 satinado, mate o textura forja fina) de alta resistencia frente a radiación UV, humedad y ambiente salino.",
            "unidad": "lote",
            "cantidad": 1,
            "precio_unitario": 720.00,
            "subtotal": 720.00
        },
        {
            "id": "05",
            "concepto": "Transporte protegido e instalación completa en propiedad en Menorca",
            "descripcion": "Embalaje protector de hojas y bastidores para transporte seguro desde taller hasta la propiedad en Menorca. Descarga, replanteo, fijación química de jambas y bisagras a pilares existentes, colgado y nivelación de ambas hojas, regulación fina de holguras, ajuste de cerradura, pasador y tope de suelo, pruebas de apertura/cierre y repasos de acabado in situ.",
            "unidad": "lote",
            "cantidad": 1,
            "precio_unitario": 950.00,
            "subtotal": 950.00
        }
    ],
    "costes_internos": [
        {
            "id": "C01",
            "concepto": "Visita técnica, replanteo y diseño CAD/DXF",
            "descripcion": "Visita en Menorca, medición de pilares/suelo, planos taller y vectorización DXF de adornos forja (5,0 h @ 40,00 €/h)",
            "unidad": "h",
            "cantidad": 5.0,
            "coste_unitario": 40.00,
            "coste_total": 200.00,
            "origen": "Oficina técnica / replanteo HAM"
        },
        {
            "id": "C02",
            "concepto": "Adornos forja corte láser CNC Inox 304 e=10 mm",
            "descripcion": "Subcontrata chapa AISI 304 e=10 mm (~1,75 m² / ~138 kg brutos, ~50 kg netos en piezas) + corte láser CNC nitrógeno + desbarbado",
            "unidad": "lote",
            "cantidad": 1.0,
            "coste_unitario": 1350.00,
            "coste_total": 1350.00,
            "origen": "Estimado ref. Recam Laser (confirmar con DXF)"
        },
        {
            "id": "C03",
            "concepto": "Porte marítimo Península → Menorca (láser)",
            "descripcion": "Transporte paletizado de piezas cortadas en 10 mm desde Barcelona/taller láser hasta Menorca",
            "unidad": "lote",
            "cantidad": 1.0,
            "coste_unitario": 80.00,
            "coste_total": 80.00,
            "origen": "Tarifa logística marítima Baleares"
        },
        {
            "id": "C04",
            "concepto": "Perfilería estructural Inox AISI 304 y curvado",
            "descripcion": "Tubo 40×40×2 mm (18 ml / 3 barras), tubo 40×20×2 mm (6 ml / 1 barra), barra maciza 14×14 mm (18 ml / 3 barras), pletinas, curvado 4 arcos y porte",
            "unidad": "lote",
            "cantidad": 1.0,
            "coste_unitario": 490.00,
            "coste_total": 490.00,
            "origen": "Tarifa perfiles inox 304 + curvado"
        },
        {
            "id": "C05",
            "concepto": "Herrajes y fijaciones en Acero Inoxidable",
            "descripcion": "6 bisagras reforzadas regulables inox (>120 kg), cerradura exterior inox + bombín + manilla, pasador suelo + cazoleta inox, taco químico + varillas A4",
            "unidad": "lote",
            "cantidad": 1.0,
            "coste_unitario": 350.00,
            "coste_total": 350.00,
            "origen": "Ferretería industrial inox"
        },
        {
            "id": "C06",
            "concepto": "Consumibles taller TIG, abrasivos y pasivado",
            "descripcion": "Gas argón puro, varilla TIG ER308L/316L, discos corte/desbaste fino inox y gel decapante/pasivante",
            "unidad": "lote",
            "cantidad": 1.0,
            "coste_unitario": 100.00,
            "coste_total": 100.00,
            "origen": "Consumibles directos taller HAM"
        },
        {
            "id": "C07",
            "concepto": "MO Taller fabricación, armado y soldadura TIG",
            "descripcion": "Corte, ingletes, armado bastidores/barrotes, soldadura TIG paneles 10 mm, montaje herrajes, decapado/pasivado y premontaje (28,0 h @ 35,00 €/h)",
            "unidad": "h",
            "cantidad": 28.0,
            "coste_unitario": 35.00,
            "coste_total": 980.00,
            "origen": "Oficial 1ª Taller Soldador TIG"
        },
        {
            "id": "C08",
            "concepto": "Tratamiento pintura taller HAM (sin horno)",
            "descripcion": "Matizado inox + imprimación epoxi fosfatante adherencia inox + 2 capas poliuretano 2C RAL 9005 (mat. 160 € + 8,0 h @ 30,00 €/h = 240 €)",
            "unidad": "lote",
            "cantidad": 1.0,
            "coste_unitario": 400.00,
            "coste_total": 400.00,
            "origen": "Norma taller HAM (imprimación + acabado sin horno)"
        },
        {
            "id": "C09",
            "concepto": "Transporte protegido a obra en Menorca",
            "descripcion": "Embalaje protector completo de las 2 hojas y bastidores y porte con vehículo taller en Menorca",
            "unidad": "porte",
            "cantidad": 1.0,
            "coste_unitario": 100.00,
            "coste_total": 100.00,
            "origen": "Logística local Menorca"
        },
        {
            "id": "C10",
            "concepto": "MO Montaje e instalación completa en obra",
            "descripcion": "2 operarios (14,0 h totales @ 35,00 €/h): anclaje químico jambas, colgado hojas (~57 kg/hoja), nivelación, ajuste cerradura/pasador y retoques",
            "unidad": "h",
            "cantidad": 14.0,
            "coste_unitario": 35.00,
            "coste_total": 490.00,
            "origen": "Equipo montaje en obra HAM"
        }
    ],
    "suplemento_316": {
        "descripcion_cliente": "Suplemento opcional por fabricación íntegra en Acero Inoxidable AISI 316 Calidad Marina (C5-M) en sustitución del AISI 304 — recomendado si la propiedad está en primera línea de mar o exposición salina directa severa (a confirmar durante la visita técnica).",
        "desglose_interno": {
            "chapa_10mm_316": 415.00,
            "perfileria_316": 250.00,
            "herrajes_316_a4": 55.00,
            "total_coste_suplemento": 720.00
        },
        "suplemento_venta_bi": 1100.00
    },
    "totales_base_304": {
        "coste_directo_total": 4540.00,
        "base_imponible": 7550.00,
        "iva_porcentaje": 21,
        "iva_importe": 1585.50,
        "total_con_iva": 9135.50,
        "beneficio_bruto": 3010.00,
        "margen_sobre_venta_pct": 39.87,
        "margen_sobre_coste_pct": 66.30
    },
    "totales_alternativa_316": {
        "coste_directo_total": 5260.00,
        "base_imponible": 8650.00,
        "iva_porcentaje": 21,
        "iva_importe": 1816.50,
        "total_con_iva": 10466.50,
        "beneficio_bruto": 3390.00,
        "margen_sobre_venta_pct": 39.19,
        "margen_sobre_coste_pct": 64.45
    },
    "incluidos": [
        "Visita técnica previa a la propiedad en Menorca para toma de medidas reales y revisión de pilares.",
        "Diseño vectorial CAD/CAM de los motivos decorativos tipo forja y presentación de plano para aprobación.",
        "Fabricación integral en Acero Inoxidable AISI 304 (adornos cortados con láser CNC en placa maciza de 10 mm y bastidores soldados a TIG con decapado y pasivado).",
        "Herrajes completos inoxidables: 6 bisagras regulables reforzadas, cerradura con bombín y 3 llaves, manilla, pasador al suelo, cazoleta/tope y anclajes químicos A4.",
        "Acabado protector en negro exterior mediante matizado del inoxidable, imprimación epoxi especial adherencia inox y dos capas de esmalte poliuretano alifático bicomponente RAL 9005.",
        "Transporte protegido en Menorca e instalación completa en obra sobre pilares existentes."
    ],
    "exclusiones": [
        "Obra civil, construcción, reparación o recrecido de pilares (mampostería, piedra de marés, hormigón o morteros), así como ejecución de solera o pavimento.",
        "Desmontaje y retirada de puerta existente o gestión de residuos (a valorar en visita si existiera puerta previa).",
        "Motorización / automatización eléctrica, fotocélulas, portero automático o acometida eléctrica en obra (presupuestable aparte si se desea automatizar).",
        "Tasas municipales, licencias urbanísticas o permisos de obra.",
        "IVA (21%) mostrado de forma separada en el cuadro de totales."
    ],
    "analisis_interno": {
        "complejidad": {
            "puntuacion": 10,
            "factor_recomendado": "1,3x",
            "factores": [
                "Geometría curva en arcos superiores y ajuste de crestería simétrica en dos hojas (Alto: 3)",
                "Mecanizado y soldadura TIG de acero inoxidable combinando tubo de 2 mm con placa maciza de 10 mm sin deformaciones térmicas (Alto: 3)",
                "Subcontratación crítica de corte láser CNC en espesor de 10 mm con diseño artístico por vectorizar (Alto: 3)",
                "Medición en obra pendiente sobre pilares existentes en Menorca (Medio: 2 -> ajustado a 1 en factor conjunto = total 10/11)"
            ]
        },
        "riesgos": [
            "Desplomes o descuadres en los pilares existentes de piedra/marés o fábrica (requiere replanteo exacto antes de cortar el láser y jambas regulables).",
            "Variación del precio final del corte láser CNC en chapa inox 304 de 10 mm según la densidad exacta de corte y perímetro de perforaciones del DXF definitivo (confirmar oferta cerrada con Recam Laser antes de lanzar pedido).",
            "Riesgo de adherencia de pintura sobre inoxidable si no se realiza desengrasado estricto y matizado uniforme en los cantos cortados por láser con nitrógeno antes de aplicar la imprimación epoxi fosfatante.",
            "Riesgo de oxidación superficial ('tea staining') si la vivienda está en primera línea de mar y se ejecutara en AISI 304 en lugar de AISI 316 (verificar distancia al mar en la visita)."
        ],
        "checklist_visita_obra": [
            "Medir luz libre exacta entre pilares en 3 alturas (abajo, centro, arriba) y verificar aplomado.",
            "Comprobar material y resistencia de los pilares (marés, bloque relleno, hormigón, piedra) para definir longitud de varillas M10/M12 A4 o placas de anclaje.",
            "Verificar pendiente del suelo en el radio de barrido de ambas hojas y sentido de apertura (hacia interior o exterior).",
            "Evaluar distancia a la costa / exposición salina directa para recomendar Opción Base AISI 304 o Opción Marina AISI 316.",
            "Confirmar con el cliente el acabado negro deseado (RAL 9005 satinado, mate o efecto forja fina), sentido de apertura de hoja activa y altura/diseño de manilla y cerradura."
        ]
    }
}

out_path = os.path.join(BASE_DIR, "datos.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=2)

print(f"datos.json generado correctamente en {out_path}")
