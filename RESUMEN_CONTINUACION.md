# Resumen de Continuación

Este documento resume el estado del repositorio para continuar el trabajo desde otro ordenador u otra sesión de OpenCode.

## Objetivo del repositorio

Crear un entorno documental, no una aplicación, para ayudar a un agente IA a presupuestar trabajos técnicos y comerciales de artículos industriales fabricados a medida.

El repositorio contiene conocimiento estructurado en Markdown, YAML y JSON para razonar sobre:

- Composición técnica real del producto.
- Materiales, mano de obra, maquinaria, tratamientos, transporte y montaje.
- Complejidad de fabricación.
- Riesgo técnico.
- Capacidad productiva.
- Oferta y demanda.
- Margen objetivo.
- Urgencia del cliente.
- Tipo de cliente.
- Histórico de reglas y criterios de presupuestación.

## Estructura creada

Carpetas principales:

- `skills/`: habilidades de presupuestación por tipo de producto y situación.
- `productos/composiciones/`: composiciones YAML de productos.
- `productos/reglas-tecnicas/`: reglas técnicas y normativas.
- `presupuestacion/costes/`: precios, proveedores, costes de MO, transporte e histórico.
- `presupuestacion/margenes/`: política de márgenes.
- `presupuestacion/oferta-demanda/`: ajustes por mercado y carga de trabajo.
- `presupuestacion/complejidad/`: evaluación de complejidad.
- `presupuestacion/checklists/`: revisiones técnicas, comerciales y de presentación.
- `plantillas/`: plantillas de presupuesto.
- `ejemplos/`: ejemplos completos de presupuestación.
- `glosario/`: términos técnicos.

## Skills existentes

Las skills principales están en `skills/`:

- `skill_presupuestacion_general.md`
- `skill_barandillas.md`
- `skill_puertas_metalicas.md`
- `skill_estructuras_metalicas.md`
- `skill_carpinteria_aluminio.md`
- `skill_instalaciones.md`
- `skill_montaje_en_obra.md`
- `skill_tratamientos_superficiales.md`
- `skill_oferta_demanda.md`
- `skill_complejidad.md`
- `skill_revision_presupuesto.md`
- `skill_escaleras.md`
- `skill_herreria.md`
- `skill_rejas.md`
- `skill_portones_cancelas.md`
- `skill_marquesinas_pergolas.md`
- `skill_productos_compuestos.md`

## Composiciones existentes

Las composiciones YAML están en `productos/composiciones/`:

- `barandilla.yaml`
- `puerta_metalica.yaml`
- `estructura_metalica.yaml`
- `ventana_aluminio.yaml`
- `cerramiento_aluminio.yaml`
- `instalacion_electrica.yaml`
- `instalacion_fontaneria.yaml`
- `instalacion_clima.yaml`
- `escalera_metalica.yaml`
- `herreria.yaml`
- `rejas.yaml`
- `porton_cancela.yaml`
- `marquesina_pergola.yaml`
- `producto_compuesto.yaml`

## Fases mentales del presupuesto

Se acordó este flujo mental:

1. Recepción y análisis de la solicitud.
2. Desarrollo de la idea de producto.
3. Desarrollo del tipo de materiales.
4. Definición de procesos de fabricación.
5. Cálculo de horas de montaje y fabricación.
6. Petición de precio a proveedores, si hace falta.
7. Evaluación de complejidad y riesgo.
8. Cálculo del coste técnico base.
9. Aplicación de margen y ajuste comercial.
10. Revisión y documentación.
11. Presentación y negociación.

## Reglas importantes acordadas

### Menorca como entorno base

Todos los presupuestos se consideran por defecto para **Menorca**, isla con ambiente muy salino, oxidante y corrosivo, salvo que el usuario indique expresamente otra ubicacion.

Regla practica:

- Interior protegido: C3 minimo practico.
- Exterior normal en Menorca: C4 recomendado.
- Costa, terraza, balcon, piscina, cubierta o exposicion directa: C5-M / ambiente marino severo.
- En exterior, priorizar AISI 316, acero galvanizado en caliente, galvanizado + pintura adecuada o sistemas epoxi/poliuretano C4/C5.
- Evitar acero pintado simple sin galvanizar en exteriores de Menorca salvo aceptacion expresa.

Ver `presupuestacion/criterios-ambientales-menorca.md`.

### No depender siempre de proveedores

El sistema debe poder presupuestar rápido usando históricos y reglas internas, sin esperar presupuesto de proveedores, salvo trabajos especiales.

Se pide presupuesto real solo cuando:

- El importe estimado es alto.
- Hay geometría o soldadura especial.
- Hay galvanizado real no tabulado.
- El montaje es complejo o requiere grúa.
- Hay tolerancias críticas.
- El cliente exige precio cerrado contractual.

### Margen rápido en subcontratación

Para presupuesto rápido con subcontratación conocida, aplicar:

```text
Precio rápido al cliente = coste estimado proveedor x 1,10
```

Este 10% se documentó en:

- `presupuestacion/costes/proveedores-conocidos.md`
- `presupuestacion/costes/historico-ferros-puig.md`

### Transporte Barcelona → Menorca

Se acordó que los portes desde Barcelona a Menorca se estiman en:

```text
0,20 €/kg
```

Está documentado en:

- `presupuestacion/costes/costes-transporte.json`
- `presupuestacion/costes/costes-materiales.md`
- `presupuestacion/costes/README.md`

### Medidas estándar de materiales

El sistema debe considerar medidas comerciales reales, por ejemplo:

- Perfiles, tubos, pletinas y barras: normalmente 6 m.
- Perfiles laminados: 6 m / 12 m / 15 m según perfil.
- Chapa: formatos habituales como 1,5 x 3 m o 2 x 4 m.

Esto afecta directamente a mermas y coste real de compra.

Ver `presupuestacion/costes/costes-materiales.md`.

## Ferros Puig Sallent

Proveedor/taller subcontratado habitual para:

- Hierro grande.
- Cerrajería de acero negro.
- Estructuras que suelen ir a galvanizado en caliente.

Contactos extraídos de presupuestos:

- Tomas Tejero: `ttejero@ferrospuig.com`, 661 909 920.
- Josep Bramon: `jbramon@ferrospuig.com`.
- Técnicos Sallent: `tecnicsallent@ferrospuig.com`.
- Teléfono general: 936 33 37 93.

Reglas extraídas de presupuestos reales:

| Concepto | Regla usable |
|---|---:|
| Perfil laminado S275 tipo IPN/IPE/HEB | 1,40 €/kg |
| Redondo / plano acero negro | 0,87 €/kg |
| Tubo cuadrado S235 50x50x4 | 5,80 €/ml |
| Placa S275 10 mm cortada pequeña | 2,20 - 5,00 €/ud |
| Corte recto | 15 €/corte |
| Taladro / perforación | 3 €/ud |
| Escote | 40 €/ud |
| G+I rojo | 0,10 €/kg |
| Montaje sencillo | 400 €/servicio |
| Montaje grande | 4.000 €/servicio |
| Envío pequeño | 32-60 € mínimo |

Ver:

- `presupuestacion/costes/proveedores-conocidos.md`
- `presupuestacion/costes/historico-ferros-puig.md`

## Aluminio EXTRUAL / Perfila Menorca

Se incorporo historico real de Perfila Menorca / Graguamaho S.L. con fabricante EXTRUAL, fecha 25/02/2026, serie Corredera E150 Minimalista lacado blanco.

Reglas extraidas:

| Concepto | Regla usable |
|---|---:|
| Perfil EXTRUAL lacado blanco sobre barras compradas | 11,24 EUR/kg |
| Perfil EXTRUAL lacado blanco medio por metro comprado | 7,41 EUR/ml |
| Perfil por peso neto de unidad terminada | 16,74 EUR/kg |
| Perfiles por superficie de unidad corredera E150 | 122 EUR/m2 |
| Accesorios E150 herraje alto | 100-105% del coste de perfiles |
| Accesorios E150 variante sencilla | 70% del coste de perfiles |
| Accesorios E150 si no se conoce herraje | 85% del coste de perfiles |

Ver `presupuestacion/costes/historico-aluminio-extrual.md`.

## Pergolas EXTRUAL E110

Se incorporo el catalogo tecnico EXTRUAL E110 Techo Fijo como referencia para pergolas de aluminio.

Datos clave:

- Aluminio 6063 T5.
- Lacado QUALICOAT-SEASIDE minimo 60 micras o anodizado minimo 15 micras.
- Sistema para acristalamiento/panelado de 6 a 88 mm.
- Pesos utiles: viga 140 mm 1,89 kg/ml; viga 140 reforzada 2,99 kg/ml; viga canalon 3,64 kg/ml; viga canalon reforzada 6,38 kg/ml; poste 2,006 kg/ml; tapa poste 1,531 kg/ml.
- Las tablas de luces del catalogo son para lugar no expuesto al viento y altura a suelo inferior a 6 m; en Menorca expuesta hay que aplicar cautela o calculo.

Ver `productos/reglas-tecnicas/pergolas-extrual-e110.md`.

## Notion y proveedores

Se planteó una futura integración con Notion:

- Base de datos de proveedores con emails, categorías, contactos, plazos y valoración.
- El agente debe consultar proveedores cuando falten precios.
- Primero debe preparar borradores de email.
- El usuario debe confirmar antes de enviar.
- Puede crearse una casilla de correo específica para presupuestos.

Se añadió una estructura operativa para conectar Notion:

- `presupuestacion/costes/notion-proveedores.md`: campos exactos de la base de datos, filtros y reglas de uso.
- `presupuestacion/costes/proveedores-config.example.json`: plantilla local sin credenciales reales.
- `.gitignore`: excluye `proveedores-config.json`, `.env` y `*.local.json`.

Para conectar realmente Notion, crear localmente `presupuestacion/costes/proveedores-config.json` con el token de integración y el ID de la base de datos. No subir ese archivo a GitHub.

Ver `presupuestacion/costes/proveedores.md` y `presupuestacion/costes/notion-proveedores.md`.

### Partidas de obra en Notion

- FAM significa Fabricacion, Acabados y Montaje.
- La vista de partidas de obra de Notion se consulta como referencia operativa, no como fuente de costes base.
- Base de datos `Partidas de obra`: `1ce598ce45458038b16ef344424e0dae`.
- Vista consultada: `1ce598ce45458027b2e9000c16abc6a6`.
- Endpoint validado: `POST /v1/views/{view_id}/queries` con `Notion-Version: 2026-03-11`.
- Total leido correctamente: 514 partidas.

Resumen global leido de Notion:

| Campo | Valores principales |
|---|---|
| Estado Partida | 402 No iniciado; 31 ANULADO; 26 Pausado; 25 Completado; 14 En curso; 12 ENTREGADO |
| Situacion de partida | 219 Factura/Completo; 73 Control de Costes; 60 Novedad; 48 Sistema interno; 38 Anulado |
| Estado en Tecnico | 325 Completado; 77 vacio; 39 Medicion; 24 No aplica |
| Estado FAM | 373 Terminado; 85 vacio; 36 Pendiente |
| Estado Compras | 311 vacio; 101 Comprado; 67 No aplica; 21 Comprar |
| Estado en Logistica | 292 Finalizado; 84 vacio; 44 No aplica; 41 Pendiente escandallo |
| Estado Administrativo | 240 Facturar; 97 Controlar costes; 85 vacio; 36 Novedad |
| Estado Comercial | 402 Adjudicado; 75 Cancelado; 14 No aplica |
| Team | 409 HAM; 58 ALUFAC; 47 vacio |

## Estado de GitHub

Repositorio remoto:

```text
https://github.com/grupodixis/presupuestador.git
```

Rama usada:

```text
master
```

Primer commit subido:

```text
7ba1e9e Crear entorno documental de presupuestacion
```

Ultimos commits subidos:

```text
9d387e3 Documentar criterios Menorca y aluminio
f0b0f56 Documentar criterios comerciales y proveedores
3386d81 soporte a notion
```

Estado tras el ultimo push:

- Rama `master` pusheada a `origin/master` hasta `9d387e3`.
- El commit `9d387e3` contiene criterios ambientales Menorca, historico aluminio EXTRUAL, reglas EXTRUAL E110 y definicion de FAM.

## Archivos locales no subidos

En el equipo original existían dos HTML no incluidos en el commit porque no forman parte del entorno documental:

- `presupuesto-cliente-pergola-terraza-01.html`
- `presupuesto-pergola-terraza-01.html`

No modificarlos ni asumir que forman parte del repositorio salvo que el usuario lo pida.

## Próximos pasos sugeridos

1. Convertir más presupuestos históricos en reglas de estimación.
2. Crear una plantilla de entrada para nuevos presupuestos históricos.
3. Completar proveedores conocidos con emails reales y categorías.
4. Añadir reglas de precios para corte láser inoxidable.
5. Añadir reglas de galvanizado en caliente con tarifa real.
6. Crear ejemplos adicionales de presupuestos rápidos usando Ferros Puig.
7. Si se usa Notion operativamente, documentar consultas utiles sobre partidas por estado, equipo y fase.
