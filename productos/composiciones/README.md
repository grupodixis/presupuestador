# Composiciones de Producto

Archivos YAML que describen la composición típica de cada producto fabricado por la empresa.

## Propósito

Cada composición define:

- Material principal.
- Material auxiliar.
- Tornillería y anclajes.
- Consumibles.
- Mano de obra de taller.
- Mano de obra de montaje.
- Maquinaria.
- Tratamientos externos.
- Transporte.
- Medición y replanteo.
- Diseño técnico.
- Riesgos.
- Tolerancias.
- Mermas.
- Controles de calidad.

## Formato

Los archivos están en YAML para facilitar su lectura por el agente IA. Ver `barandilla.yaml` como ejemplo de estructura completa.

## Lista de composiciones

| Archivo | Producto |
|---|---|
| `barandilla.yaml` | Barandilla metálica |
| `puerta_metalica.yaml` | Puerta metálica |
| `estructura_metalica.yaml` | Estructura metálica |
| `ventana_aluminio.yaml` | Ventana de aluminio |
| `cerramiento_aluminio.yaml` | Cerramiento de aluminio |
| `instalacion_electrica.yaml` | Instalación eléctrica |
| `instalacion_fontaneria.yaml` | Instalación de fontanería |
| `instalacion_clima.yaml` | Instalación de climatización |
| `escalera_metalica.yaml` | Escalera metálica |
| `herreria.yaml` | Herrería (forja artística y funcional) |
| `rejas.yaml` | Rejas de protección |
| `porton_cancela.yaml` | Portón y cancela metálica |
| `marquesina_pergola.yaml` | Marquesina, pérgola y toldo |
| `producto_compuesto.yaml` | Producto compuesto a medida (multimaterial) |

## Uso por el agente

1. Identificar el producto en la descripción del trabajo.
2. Cargar el YAML de composición correspondiente.
3. Usar los campos como checklist para no omitir partidas.
4. Adaptar cantidades según las dimensiones reales del trabajo.
5. Cruzar con la skill correspondiente para aplicar criterios.
