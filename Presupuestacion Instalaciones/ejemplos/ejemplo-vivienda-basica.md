# Ejemplo: Vivienda Basica

## Datos

| Campo | Valor |
|---|---|
| Tipo de inmueble | Vivienda |
| Zonas | Salon-cocina, 2 dormitorios, 1 baño, terraza |
| Fuente | Descripcion preliminar sin plano escalado |
| Nivel | Conteo rapido |

## Alcance interpretado

- Electricidad basica por estancias.
- Domotica para persianas y encendidos principales.
- IoT para sensores de fuga y gateway.
- Fontaneria de cocina y baño.
- No se miden metros lineales por falta de plano.

## Medicion

| Disciplina | Zona | Partida | Unidad | Cantidad | Estado | Criterio / observacion |
|---|---|---|---:|---:|---|---|
| Electricidad | Salon-cocina | Punto de luz | punto | 3 | supuesto | Salon, cocina y zona comedor |
| Electricidad | Salon-cocina | Enchufe monofasico | ud | 10 | supuesto | Tomas generales y encimera |
| Electricidad | Cocina | Circuito dedicado | ud | 4 | supuesto | Horno, vitro, lavavajillas, frigorifico |
| Electricidad | Dormitorios | Punto de luz | punto | 2 | supuesto | 1 por dormitorio |
| Electricidad | Dormitorios | Enchufe monofasico | ud | 8 | supuesto | 4 por dormitorio |
| Electricidad | Baño | Punto de luz | punto | 2 | supuesto | Techo y espejo |
| Electricidad | Terraza | Punto estanco | punto | 2 | supuesto | Luz y enchufe exterior |
| Domotica | General | Actuador de persiana | canal | 3 | supuesto | Salon y dos dormitorios |
| Domotica | General | Sensor de presencia | ud | 2 | supuesto | Pasillo/entrada y baño |
| Domotica | General | Gateway domotico | ud | 1 | supuesto | Sistema pendiente de definir |
| IoT | Cocina/baño | Sensor de fuga de agua | ud | 2 | supuesto | Bajo fregadero y baño |
| IoT | General | Gateway / hub IoT | ud | 1 | supuesto | Puede coincidir con gateway domotico; confirmar |
| Fontaneria | Cocina | Punto AF | punto | 2 | supuesto | Fregadero y lavavajillas |
| Fontaneria | Cocina | Punto ACS | punto | 1 | supuesto | Fregadero |
| Fontaneria | Cocina | Punto desague | punto | 2 | supuesto | Fregadero y lavavajillas |
| Fontaneria | Baño | Punto AF | punto | 3 | supuesto | Lavabo, ducha, inodoro |
| Fontaneria | Baño | Punto ACS | punto | 2 | supuesto | Lavabo y ducha |
| Fontaneria | Baño | Punto desague | punto | 3 | supuesto | Lavabo, ducha, inodoro |
| Fontaneria | Baño | Aparato sanitario | ud | 3 | supuesto | Lavabo, ducha, inodoro |

## Dudas

| Duda | Impacto | Confirmacion necesaria |
|---|---|---|
| No hay plano escalado | medio | Medir ml de tubo/cable en visita o plano acotado |
| Sistema domotico no definido | alto | Confirmar protocolo y marca |
| Gateway domotico e IoT pueden ser el mismo | medio | Confirmar plataforma elegida |

## Exclusiones

- Precio final.
- Legalizacion y boletines.
- Rozas, reposiciones y pintura.
- Metros lineales de cableado y tuberia.
