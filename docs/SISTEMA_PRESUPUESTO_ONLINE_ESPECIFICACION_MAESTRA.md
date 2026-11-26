# SISTEMA DE PRESUPUESTACIÓN ONLINE — ESPECIFICACIÓN MAESTRA DE CONOCIMIENTO, ARQUITECTURA Y FORMATO DE DOCUMENTOS

> **Documento Técnico y de Negocio para el Desarrollo del SaaS de Presupuestación de Carpintería Metálica, Herrería y Estructuras**  
> **Basado en la experiencia acumulada de más de 65 presupuestos reales ejecutados en HAM Estructuras Metálicas Menorca / Dixis Recursos y Soluciones S.L.**  
> **Fecha de Compilación:** Noviembre 2026 · **Versión:** 1.0 (Producción)

---

## 1. RESUMEN EJECUTIVO Y VISIÓN DEL PRODUCTO

### 1.1. Propósito del Sistema Online
El objetivo de este sistema es transformar el proceso tradicional de elaboración de presupuestos en talleres de carpintería metálica, cerrajería, calderería y estructuras de acero en una plataforma SaaS interactiva, automatizada e inteligente. El sistema permite pasar de una descripción informal del cliente (o un croquis en servilleta, PDF o plano técnico) a un **presupuesto comercial cerrado de alta gama** y a su correspondiente **escandallo técnico interno de taller** en menos de 5 minutos, garantizando un margen de beneficio estricto y eliminando los errores comunes de costes ocultos.

### 1.2. El Reto Industrial Específico
A diferencia de los productos de catálogo seriado, la carpintería metálica y la herrería son industrias de **fabricación a medida con alta incertidumbre**:
1. Cada trabajo combina materiales heterogéneos (acero estructural S275, acero inoxidable AISI 304/316, aluminio lacado marino, vidrios laminares/templados, tramex, madera).
2. Procesos internos de taller (corte, mecanizado, taladrado, soldadura MIG/TIG, curvado, desbaste, imprimación) combinados con procesos subcontratados (corte láser, plegado CNC, galvanizado en caliente, lacado).
3. Mano de obra en taller versus montaje en obra con medios auxiliares (andamios, plataformas elevadoras tijera/articuladas, grúas pluma).
4. El **factor geográfico e insular** (en entornos como Menorca, la corrosión marina C4/C5-M exige calidades estrictas de tratamiento superficial y la logística marítima añade 0,20 €/kg a los suministros desde la península).

### 1.3. Usuarios del Sistema y Roles
- **Comercial / Recepción:** Introduce la solicitud, lanza los cuestionarios rápidos al cliente, genera la versión de oferta comercial y realiza el seguimiento del estado de la propuesta.
- **Oficina Técnica / Ingeniero:** Define el desglose de materiales, valida cálculos estructurales CTE (cargas de viento/nieve), define despieces y listas de corte.
- **Jefe de Taller / Producción:** Gestiona el escandallo interno, valida tiempos de fabricación (horas hombre), asigna máquinas y controla el avance FAM (Fabricación, Acabados, Montaje).
- **Gerencia / Dirección Financiera:** Supervisa el margen comercial sobre venta, analiza desviaciones entre presupuesto y coste real (post-cálculo) y ajusta tarifas horarias.

---

## 2. METODOLOGÍA COGNITIVA: EL FLUJO DE PRESUPUESTACIÓN EN 11 FASES

El sistema online debe estructurar la experiencia de usuario guiándolo a través de las 11 fases mentales contrastadas en la operativa diaria:

```
 [1. Recepción y Análisis] ──> [2. Conceptualización de Producto] ──> [3. Despiece y Materiales]
           │
           ▼
 [4. Procesos de Fabricación] ─> [5. Cálculo Mano de Obra] ─> [6. Cotización Subcontratas]
           │
           ▼
 [7. Evaluación Riesgo/Complejidad] ─> [8. Coste Técnico Base] ─> [9. Aplicación de Márgenes]
           │
           ▼
 [10. Generación Dual de Documentos] ──> [11. Presentación, Firma y Seguimiento]
```

### Detalle de cada fase en la plataforma:

1. **Fase 1: Recepción y Análisis de la Solicitud:** Ingesta del requerimiento del cliente (correo, WhatsApp, formulario web o plano CAD/PDF). La IA extrae entidades clave: cliente, tipología de obra, ubicación geográfica, plazos exigidos y presupuesto objetivo si existe.
2. **Fase 2: Conceptualización del Producto:** Activación del configurador paramétrico correspondiente (ej. Pérgola, Escalera, Barandilla, Nave, Dintel, Cancela). El sistema formula un **cuestionario inteligente** con los parámetros críticos que faltan.
3. **Fase 3: Desarrollo de Materiales y Mermas:** Determinación de perfiles, chapas y tornillería. El sistema aplica longitudes comerciales de compra (barras de 6 m o 12 m, chapas de 1,5x3 m o 2x4 m) y calcula el porcentaje de merma y aprovechamiento de retales.
4. **Fase 4: Definición de Procesos de Fabricación:** Secuencia de operaciones de taller: corte con sierra de cinta, corte láser, mecanizado/taladrado, escotado, armado, soldeo (longitud de cordón), desbarbado, decapado/pasivado y tratamiento superficial.
5. **Fase 5: Estimación de Mano de Obra (Horas-Hombre):** Desglose diferenciado por especialidad:
   - *Horas Técnicas:* Medición en obra, diseño 3D, planos de taller y despiece.
   - *Horas de Taller:* Oficial de 1ª para fabricación y soldadura.
   - *Horas de Montaje:* Cuadrilla de montaje en obra exterior.
6. **Fase 6: Cotización de Procesos Externos y Subcontratas:** Consulta de históricos tabulados de proveedores habituales (ej. Ferros Puig Sallent para perfiles y galvanizado, corte láser de chapa, lacadores certificados Qualicoat Seaside) o generación de borradores de solicitud de precio si no hay precio estándar.
7. **Fase 7: Evaluación de Complejidad y Riesgos:** Ponderación de factores de riesgo: tolerancias milimétricas, accesos difíciles para camión o grúa, solapes de gremios, alturas de trabajo y trabajos en caliente.
8. **Fase 8: Cálculo del Coste Técnico Base (CDT):** Suma algebraica estricta:
   $$\text{CDT} = \text{Coste Materiales} + \text{Coste Mano de Obra Directa} + \text{Coste Subcontratas} + \text{Portes y Maquinaria Auxiliar}$$
9. **Fase 9: Política de Márgenes y Ajuste Comercial:** Aplicación del coeficiente de margen sobre venta deseado (típicamente entre el 40% y el 55% para fabricación propia, o factor $1,10$ para subcontratación pura de apoyo).
10. **Fase 10: Generación Dual de Documentos (El "Doble Estándar"):** Generación automática e instantánea de la pareja documental: **Presupuesto Comercial (Cliente)** y **Estudio Técnico Interno (Escandallo)**, más la hoja de cálculo viva en Excel (.xlsx) y la propuesta de email en castellano o inglés.
11. **Fase 11: Presentación, Cierre y Pasarela FAM:** Envío al cliente con enlace de aceptación/firma digital. Al aprobarse, el presupuesto se vuelca directamente a producción bajo las fases **FAM** (Fabricación, Acabados, Montaje).

---

## 3. EL CEREBRO DE REGLAS DE NEGOCIO Y CRITERIOS DE TALLER

Para que el software presupueste con precisión quirúrgica, el motor de reglas debe contener codificadas las siguientes directivas inviolables:

### 3.1. Normas Estrictas de Fabricación y Acabados HAM
- **Pintura en HAM (Regla Estricta):** En HAM la pintura **NUNCA es al horno (termolacado)**. Todos los procesos de pintura de taller se realizan mediante:
  1. Preparación mecánica y desengrasado (Grado St 3 / chorreado Sa 2).
  2. Imprimación de alta adherencia y protección anticorrosiva adecuada al metal base (epoxi fosfatante / fosfato de zinc alifático de secado rápido).
  3. Esmalte de acabado bicomponente o poliuretano de alta resistencia a la intemperie.
  *Nunca especificar ni presupuestar pintura al horno en los presupuestos de fabricación de taller.*
- **Estructuras Desmontables y Atornilladas:** Salvo imperativo estructural que requiera soldadura in situ continua, las estructuras, pérgolas y barandillas deben proyectarse como **desmontables mediante uniones atornilladas**. Esto permite:
  - Optimizar el transporte marítimo y terrestre (paquetes planos apilables).
  - El transporte se dimensiona únicamente como la **ida de un camión** con el material despiezado para su posterior montaje in situ.
- **Tubo Inoxidable AISI 316 40x40x2 mm:**
  - Coste de compra estándar para el taller: **10,00 €/metro lineal**.
  - Precio de venta unitario estándar al cliente: **20,00 €/metro lineal**.

### 3.2. Criterios Ambientales e Insulares (Factor Menorca)
- **Clasificación de Exposición Marina (ISO 12944):**
  - *Interior protegido:* Mínimo C3.
  - *Exterior urbano o rural interior:* Recomendado C4.
  - *Litoral, terrazas expuestas, cubiertas, barandillas de primera línea:* **C5-M (Ambiente marino severo)**.
  - *Directriz de acero al carbono:* **Prohibido el acero al carbono simplemente pintado en exteriores sin galvanizar en caliente previo**. En exterior costero, la combinación obligatoria es:
    - Acero inoxidable AISI 316 con pasivado químico y tornillería A4.
    - O acero estructural galvanizado en caliente según UNE-EN ISO 1461 + sistema dúplex (imprimación epoxi + poliuretano).
- **Logística Marítima Península → Baleares:**
  - Flete y portes desde Barcelona a Menorca para aceros estructurales y materiales pesados: **0,20 €/kg**.
  - Recargo mínimo por envío pequeño agrupado: entre 32 € y 60 € por expedición.

### 3.3. Tarifas de Mano de Obra y Rendimientos de Taller
| Especialidad / Perfil | Coste Interno Directo | Tarifa de Venta Estándar Repercutida |
|---|---:|---:|
| **Oficial 1ª Taller (Soldador / Calderero)** | 30,00 €/h | 45,00 - 55,00 €/h |
| **Oficial Montador en Obra** | 35,00 €/h | 55,00 - 65,00 €/h |
| **Oficina Técnica (Delineación / Mediciones / 3D)** | 35,00 €/h | 60,00 - 75,00 €/h |
| **Ayudante / Peón de Taller** | 22,00 €/h | 35,00 - 40,00 €/h |

### 3.4. Costes Unitarios y Operaciones de Taller Validadas
- **Perfiles laminados S275JR (IPE, IPN, HEB, UPN):** 1,40 €/kg - 1,50 €/kg base + 0,20 €/kg transporte marítimo.
- **Pletinas, redondos y calibrados de acero negro:** 0,87 €/kg - 1,10 €/kg.
- **Chapa de acero lágrima 5/3 mm para rampas/suelos:** 2,40 €/kg.
- **Tubo estructural cuadrado acero negro 40x40x2 / 50x50x2:** 8,00 €/ml.
- **Peldaños de entramado metálico (Tramex) galvanizado:** 70,00 €/ud.
- **Placas de anclaje cortadas de 10 mm pequeñas:** 2,20 - 5,00 €/ud.
- **Operaciones de taller tarifadas:**
  - Corte recto con sierra de cinta: **15,00 €/corte**.
  - Taladro pasante estándar: **3,00 €/unidad**.
  - Escote / cajeo en perfiles: **40,00 €/unidad**.
  - Imprimación de taller básica (G+I rojo/gris): **0,10 - 0,15 €/kg** o **3,50 €/m²**.
- **Fórmula de Subcontratación Rápida:**
  $$\text{Precio Venta Rápido Subcontrata} = \text{Coste Proveedor} \times 1,10$$
  *(Aplicable a partidas cerradas de talleres colaboradores como Ferros Puig o servicios de grúa externa donde no se asume transformación).*

---

## 4. ESPECIFICACIÓN DEL FORMATO DE DOCUMENTOS Y ENTREGABLES

El sistema online debe generar 4 salidas automáticas complementarias por cada expediente de presupuesto:

```
                                  [ MOTOR DE PRESUPUESTACIÓN ]
                                               │
      ┌──────────────────┬─────────────────────┴──────────────────┬──────────────────┐
      ▼                  ▼                                        ▼                  ▼
1. Presupuesto     2. Estudio Técnico                       3. Hoja Excel      4. Plantillas
   Cliente            Interno (Escandallo)                     Dinámica           Email/Mensajes
   (PDF / HTML)       (PDF / HTML)                             (.xlsx)            (.md / texto)
```

### 4.1. Presupuesto Cliente (`presupuesto-cliente.html` / `.pdf`)
- **Público:** Promotor, particular, arquitecto, constructor.
- **Estilo Visual:** Limpio, moderno, corporativo. Tipografía *Segoe UI* o *Inter*. Colores base: Slate Navy (`#0F172A`), Acento Dorado/Ámbar (`#B45309`), Verde Confirmación (`#15803D`).
- **Contenido Clave:**
  - Encabezado institucional con logo, razón social emisor (Dixis Recursos y Soluciones S.L.), CIF B57825432, marca comercial (HAM Estructuras Metálicas Menorca), dirección y contactos.
  - Bloque metadatos: Código de expediente (`P-2026-XXXX`), Referencia, Cliente fiscal y CIF, Dirección, Fecha y Validez (30 días naturales por defecto).
  - Banner destacado de **Alcance Técnico Resumido**.
  - Tabla de partidas cliente: Nº, Código de partida, Concepto y Descripción técnica exhaustiva, Ud., Cantidad, Precio Unitario e Importe total.
  - Tabla de liquidación: Subtotal Base Imponible, I.V.A. (21%) y Total General Presupuesto.
  - Pliego de condiciones particulares y garantías LOE / UNE-EN 1090.
  - **Inviolabilidad:** En ningún caso se revelan horas de taller, costes unitarios de compra de materiales ni porcentajes de margen bruto.

### 4.2. Estudio Técnico Interno y Escandallo (`presupuesto-interno-tecnico.html` / `.pdf`)
- **Público:** Oficina Técnica, Dirección y Jefe de Taller.
- **Marca de Agua / Badge:** "USO INTERNO / CONFIDENCIAL / ESCANDALLO DE TALLER".
- **Contenido Clave:**
  - Desglose físico de elementos: tabla con dimensiones, metros lineales, pesos en kg, superficies de pintura en m², taladros y uniones.
  - Escandallo de materiales: lista de la compra detallada con proveedores previstos, cantidades con mermas, coste unitario y coste total.
  - Escandallo de mano de obra: desglose de horas por puesto (diseño, corte, taladrado, soldadura, pintura, montaje) a coste horario real.
  - Tarjetas de Rentabilidad (KPIs financieros):
    - *Coste Directo Total (CDT)*
    - *Precio Venta Final al Cliente*
    - *Beneficio Bruto en Euros* ($\text{Venta} - \text{Coste}$)
    - *Margen Bruto sobre Venta (%)* (alerta si es $< 40\%$)
  - Análisis de riesgos, supuestos de cálculo y notas para el encargado de montaje.

### 4.3. Libro de Trabajo Excel Dinámico (`.xlsx`)
- Generado con librerías como `openpyxl` o similar.
- **Hoja 1: "Presupuesto Cliente":** Formato oficial para entregar al cliente o exportar a Excel, con celdas de importe vinculadas mediante fórmulas matemáticas (`=D11*E11`), suma de base imponible (`=SUM(G11:G15)`), cálculo de IVA (`=G16*0.21`) y Total Presupuesto (`=G16+G17`).
- **Hoja 2: "Escandallo Interno":** Fórmulas de coste directo de materiales, cálculo de coste horario de mano de obra (`=Horas*Tarifa`), suma de costes directos y fórmula de margen real:
  $$\text{Margen \%} = \frac{\text{Venta} - \text{Coste Directo}}{\text{Venta}} \times 100$$
- Diseño ejecutivo con celdas cabecera Navy `#0F172A`, texto blanco, bordes finos `#CBD5E1` y formato monetario nativo `#,##0.00 €`.

### 4.4. Comunicaciones Multicanal Automatizadas
- **Respuesta de Email Formal en Castellano:** Saludo formal, resumen ejecutivo de la propuesta, desglose sintético de importes, plazo de ejecución, validez, aviso de archivos adjuntos (PDF y Excel) e instrucciones para confirmación de pedido.
- **Respuesta de Email Formal en Inglés:** Para el elevado volumen de clientes extranjeros en Menorca (británicos, franceses, alemanes), con terminología técnica equivalente (mild steel, hot-dip galvanized, powder coating alternatives, marine grade stainless steel AISI 316).
- **Mensaje Corto para WhatsApp:** Resumen ultra-directo de importe neto, plazo y enlace al visor web interactivo.

---

## 5. ESPECIFICACIÓN DEL MODELO DE DATOS ESTÁNDAR (`datos.json`)

Para que la aplicación web funcione con desacoplamiento total entre frontend, motor de cálculo y renderizadores de documentos, todos los presupuestos deben responder al siguiente esquema canónico JSON:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "PresupuestoTecnicoIndustrialSchema",
  "type": "object",
  "required": ["proyecto", "cliente", "emisor", "partidas_cliente", "totales_economicos", "escandallo_interno"],
  "properties": {
    "proyecto": {
      "type": "object",
      "properties": {
        "codigo": { "type": "string", "example": "P-2026-0065" },
        "referencia": { "type": "string", "example": "PRE-2026-1124-DINT-REFORMARC" },
        "titulo": { "type": "string" },
        "fecha": { "type": "string" },
        "validez_dias": { "type": "integer", "default": 30 },
        "plazo_entrega": { "type": "string" },
        "forma_pago": { "type": "string", "default": "100% a la confirmación de presupuesto" },
        "lugar_entrega": { "type": "string" }
      }
    },
    "cliente": {
      "type": "object",
      "properties": {
        "codigo_factusol": { "type": "string" },
        "nombre_fiscal": { "type": "string" },
        "nombre_comercial": { "type": "string" },
        "nif": { "type": "string" },
        "domicilio": { "type": "string" },
        "codigo_postal": { "type": "string" },
        "poblacion": { "type": "string" },
        "provincia": { "type": "string" },
        "pais": { "type": "string", "default": "España" },
        "email": { "type": "string", "format": "email" },
        "telefono": { "type": "string" },
        "referencia_contacto": { "type": "string" },
        "destino_obra": { "type": "string" }
      }
    },
    "emisor": {
      "type": "object",
      "properties": {
        "razon_social": { "type": "string", "default": "Dixis Recursos y Soluciones S.L." },
        "cif": { "type": "string", "default": "B57825432" },
        "marca_comercial": { "type": "string", "default": "HAM Estructuras Metálicas Menorca" },
        "domicilio": { "type": "string", "default": "Av. Circunval·lació, 11, Pol. Ind. Sant Lluís" },
        "codigo_postal": { "type": "string", "default": "07710" },
        "localidad": { "type": "string", "default": "Sant Lluís" },
        "provincia": { "type": "string", "default": "Illes Balears" },
        "telefono": { "type": "string", "default": "+34 971 35 20 18" },
        "movil": { "type": "string", "default": "+34 669 769 541" },
        "email": { "type": "string", "default": "pablo@dixis.es" },
        "email_admon": { "type": "string", "default": "administracion@dixis.es" },
        "web": { "type": "string", "default": "https://www.hamenorca.com" }
      }
    },
    "especificaciones_tecnicas": {
      "type": "object",
      "properties": {
        "normativa_acero": { "type": "string" },
        "tratamiento_superficial": { "type": "string" },
        "fijaciones_tornilleria": { "type": "string" },
        "tolerancias_fabricacion": { "type": "string", "default": "UNE-EN 1090-2 (EXC2)" }
      }
    },
    "elementos": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "descripcion": { "type": "string" },
          "tipo_perfil": { "type": "string" },
          "total_ml": { "type": "number" },
          "peso_total_kg": { "type": "number" },
          "superficie_total_m2": { "type": "number" },
          "precio_unitario": { "type": "number" },
          "importe": { "type": "number" }
        }
      }
    },
    "partidas_cliente": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["num", "codigo_partida", "concepto", "descripcion", "unidad", "cantidad", "precio_unitario", "importe"],
        "properties": {
          "num": { "type": "string" },
          "codigo_partida": { "type": "string" },
          "concepto": { "type": "string" },
          "descripcion": { "type": "string" },
          "unidad": { "type": "string" },
          "cantidad": { "type": "number" },
          "precio_unitario": { "type": "number" },
          "importe": { "type": "number" }
        }
      }
    },
    "totales_economicos": {
      "type": "object",
      "required": ["base_imponible", "iva_porcentaje", "iva_importe", "total_presupuesto"],
      "properties": {
        "base_imponible": { "type": "number" },
        "iva_porcentaje": { "type": "number", "default": 21 },
        "iva_importe": { "type": "number" },
        "total_presupuesto": { "type": "number" }
      }
    },
    "escandallo_interno": {
      "type": "object",
      "required": ["resumen_materiales", "resumen_mano_obra", "totales_escandallo"],
      "properties": {
        "resumen_materiales": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "concepto": { "type": "string" },
              "unidad": { "type": "string" },
              "cantidad": { "type": "number" },
              "coste_unitario": { "type": "number" },
              "coste_total": { "type": "number" }
            }
          }
        },
        "resumen_mano_obra": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "concepto": { "type": "string" },
              "horas": { "type": "number" },
              "tarifa_hora": { "type": "number" },
              "coste_total": { "type": "number" }
            }
          }
        },
        "totales_escandallo": {
          "type": "object",
          "properties": {
            "coste_materiales": { "type": "number" },
            "coste_mano_obra": { "type": "number" },
            "coste_subcontratas": { "type": "number", "default": 0 },
            "horas_totales": { "type": "number" },
            "coste_directo_total": { "type": "number" },
            "precio_venta": { "type": "number" },
            "margen_bruto_euros": { "type": "number" },
            "margen_bruto_porcentaje": { "type": "number" }
          }
        }
      }
    }
  }
}
```

---

## 6. ARQUITECTURA TÉCNICA DEL SOFTWARE (FULLSTACK SAAS WEB)

Para construir la plataforma web online definitiva, se recomienda una arquitectura moderna desacoplada en tres niveles:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FRONTEND CLIENTE (Next.js / React)              │
│  - Dashboard FAM            - Configuradores 3D Paramétricos (Three.js)│
│  - Editor de Partidas Dual  - Visor A4 PDF & Excel                     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTPS / REST / WebSockets
┌───────────────────────────────────▼────────────────────────────────────┐
│                  BACKEND CORE API (FastAPI / Node.js)                  │
│  - Auth & RBAC               - Motor de Reglas Industriales & Ratios   │
│  - Ingesta Documental & IA   - Servicio de Generación PDF (Puppeteer)  │
│  - Generador Excel OpenPyXL  - Notificador Email / WhatsApp            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌──────────────┐           ┌──────────────────┐         ┌────────────────┐
│  BASE DATOS  │           │ MOTOR IA / LLM   │         │ INTEGRACIONES  │
│  PostgreSQL  │           │ - Gemini 1.5/2.0 │         │ - FactuSol ERP │
│  + pgvector  │           │ - RAG de Skills  │         │ - Notion API   │
│  (Supabase)  │           │ - Extracción PDF │         │ - Firma Valid. │
└──────────────┘           └──────────────────┘         └────────────────┘
```

### 6.1. Componentes del Backend Core
1. **Módulo de Cálculo Paramétrico e Ingeniería de Costes:**
   - Calcula pesos automáticos a partir de tablas dimensionales de perfiles (IPE, HEB, tubos huecos, chapas).
   - Calcula superficies a pintar según perímetro de perfil: $\text{Superficie} = \text{Perímetro (m)} \times \text{Longitud (m)}$.
   - Estimación de tiempos de soldeo: según espesor de garganta $a$ y proceso (MIG hilo macizo o TIG en inoxidable).
2. **Servicio Headless de Generación Documental:**
   - Emite PDF exactos píxel a píxel mediante Chromium headless con parámetros:
     `--headless --print-to-pdf-no-header --disable-gpu` y CSS `@page { size: A4 portrait; margin: 10mm 12mm; }`.
   - Generación de Excel nativo con openpyxl / ExcelJS garantizando fórmulas vivas en las celdas de totales.
3. **Módulo de Ingesta Inteligente y RAG (Retrieval-Augmented Generation):**
   - Ingesta de descripciones desestructuradas enviadas por clientes vía email o WhatsApp.
   - Vectorización de las skills de taller (`skill_barandillas.md`, `skill_naves_industriales.md`, `skill_puertas_metalicas.md`).
   - El LLM sugiere automáticamente la lista de materiales, operaciones y partidas estándar correspondientes al catálogo de FactuSol.
4. **Módulo de Aprendizaje Activo (Learning Loop):**
   - Cada vez que el técnico modifica un precio sugerido en pantalla o altera un tiempo de mano de obra, el sistema registra un evento de aprendizaje (`skills/aprendizaje/`).
   - Cuando una corrección se repite 3 veces en un producto similar (ej. "el precio del tubo 40x40 en Menorca subió a 8 €/ml"), el sistema propone actualizar automáticamente el coste maestro.

---

## 7. ESPECIFICACIÓN DE INTERFAZ DE USUARIO (UI / UX)

Para asegurar una adopción inmediata por parte de los presupuestadores y el personal técnico de taller, la interfaz debe diseñarse siguiendo 4 pantallas clave:

### 7.1. Pantalla 1: Dashboard de Control y Pipeline FAM
- **Métricas Superiores:** Presupuestos emitidos en el mes, % de conversión/cierre, Facturación potencial, Margen medio proyectado.
- **Tablero Kanban de Estado FAM:**
  - *Borrador / Estudio Técnico.*
  - *Enviado al Cliente.*
  - *Adjudicado / En Fábrica (F).*
  - *En Acabados / Pintura (A).*
  - *En Montaje en Obra (M).*
  - *Completado / Facturado.*

### 7.2. Pantalla 2: Configurador Paramétrico Inteligente
- Selector rápido de familia: **Estructuras/Naves | Pérgolas | Barandillas | Escaleras | Puertas/Portones | Dinteles/Refuerzos | Herrería**.
- Inputs directos con valores por defecto preconfigurados (ej. si se elige barandilla exterior en Menorca, preselecciona acero inoxidable AISI 316 o galvanizado caliente con acabado marino C5-M).
- Visualizador 3D interactivo en Three.js / Canvas para comprobar cotas y geometría antes de presupuestar.

### 7.3. Pantalla 3: Editor de Partidas con Escandallo Dual en Tiempo Real
- **Diseño a Doble Panel:**
  - **Panel Izquierdo (Visión Cliente):** Tabla interactiva con partidas, descripciones comerciales, unidades, precios de venta e importes.
  - **Panel Derecho (Escandallo Técnico Interno):** Desglose en tiempo real de materiales (kg, ml, coste base), tiempos de taller por operación (horas x coste), subcontratas y **Semáforo de Rentabilidad**:
    - *Verde:* Margen sobre venta $> 45\%$.
    - *Amarillo:* Margen entre $35\%$ y $45\%$.
    - *Rojo:* Margen $< 35\%$ (requiere justificación o autorización expresa de gerencia).

### 7.4. Pantalla 4: Visor de Documentos y Lanzadera de Cierre
- Pestañas conmutables: `[Presupuesto Cliente PDF]` | `[Estudio Técnico Interno]` | `[Hoja Excel]` | `[Email Comercial]`.
- Botones de acción directa:
  - `Imprimir / Guardar PDF`.
  - `Descargar Excel con Fórmulas`.
  - `Enviar por Correo al Cliente (con copia a administracion@dixis.es)`.
  - `Copiar Mensaje para WhatsApp con Enlace Web`.
  - `Vincular a FactuSol (Crear Presupuesto con código FactuSol)`.

---

## 8. PLAN DE IMPLEMENTACIÓN Y ROADMAP DE DESARROLLO

Se propone un plan de despliegue en 3 fases progresivas para asegurar continuidad operativa:

```
┌────────────────────────────────┐  ┌────────────────────────────────┐  ┌────────────────────────────────┐
│            FASE 1              │  │            FASE 2              │  │            FASE 3              │
│    MVP NÚCLEO DE CÁLCULO       │  │      IA & CONFIGURADORES       │  │   CONECTIVIDAD TOTAL ERP/FAM   │
│         (Semanas 1-4)          │  │         (Semanas 5-8)          │  │         (Semanas 9-12)         │
├────────────────────────────────┤  ├────────────────────────────────┤  ├────────────────────────────────┤
│ - Base de datos PostgreSQL/SQL │  │ - Asistente IA RAG integrado   │  │ - Conexión bidireccional       │
│ - Motor de cálculo escandallo  │  │ - Configuradores paramétricos  │    con FactuSol (16.820 arts.)    │
│ - Editor de partidas cliente   │  │   (Pérgolas, Naves, Barand.)   │  │ - Sincronización con Notion    │
│ - Generador HTML/PDF (Chrome)  │  │ - Visor 3D Three.js            │    (Partidas de Obra FAM)         │
│ - Exportador Excel (OpenPyXL)  │  │ - Motor de Aprendizaje Activo  │  │ - Firma digital del cliente    │
│ - Control de márgenes en vivo  │  │ - Redactor bilingüe de emails  │  │ - App móvil para montaje obra  │
└────────────────────────────────┘  └────────────────────────────────┘  └────────────────────────────────┘
```

### 8.1. Métricas de Éxito del Sistema
- **Reducción del tiempo de presupuestación:** de 120-180 minutos a menos de 5 minutos por presupuesto.
- **Tasa de error en costes de materiales y portes:** inferior al $2\%$.
- **Protección de margen comercial:** margen medio garantizado $> 45\%$ sin partidas deficitarias por olvido de consumibles, mermas o fletes marítimos.
- **Calidad de presentación comercial:** percepción premium por parte del cliente gracias a presupuestos limpios, especificaciones técnicas precisas y pliego de garantías transparentes.

---
*Fin de la Especificación Maestra.*
