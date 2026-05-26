# Skill: Conteo de Domotica

## Cuándo usar esta skill

Para instalaciones de automatizacion de vivienda o local: iluminacion regulada, persianas, climatizacion, escenas, sensores, actuadores, pantallas, videoportero, control de accesos y sistemas KNX, Zigbee, Z-Wave, Matter, WiFi o propietarios.

## Unidades habituales

| Elemento | Unidad | Criterio de conteo |
|---|---:|---|
| Sensor de presencia / movimiento | ud | Cada detector fisico |
| Sensor de luminosidad | ud | Cada sensor independiente |
| Sensor de temperatura / humedad | ud | Cada punto de medicion |
| Sensor de apertura | ud | Cada puerta o ventana monitorizada |
| Actuador de iluminacion | canal | Cada canal conmutado o regulado |
| Actuador de persiana / toldo | canal | Cada motor controlado |
| Termostato / controlador clima | ud | Cada zona de control |
| Pulsador domotico | ud | Cada mecanismo, botonera o teclado |
| Pantalla / panel tactil | ud | Cada interfaz fija |
| Gateway / controlador central | ud | Cada servidor, hub o pasarela |
| Fuente de alimentacion / acoplador bus | ud | Cada equipo auxiliar necesario |
| Programacion de escenas | escena | Cada escena o automatizacion definida |
| Cable bus / alimentacion | ml | Si se mide aparte por recorrido |

## Datos a extraer

- Protocolo o sistema previsto.
- Numero de zonas de control.
- Funciones a automatizar: luz, persianas, clima, riego, seguridad, accesos.
- Sensores por estancia.
- Actuadores por circuito o motor.
- Necesidad de cuadro domotico o modulos en cuadro electrico.
- Interfaces de usuario: pantallas, pulsadores, app, voz.

## Criterios especificos

- Contar actuadores por canal, no solo por modulo fisico, porque un modulo puede tener varios canales.
- Contar sensores por punto real de medicion o deteccion.
- Separar suministro de dispositivos, instalacion, conexionado y programacion.
- Las escenas no son puntos fisicos, pero consumen configuracion y pruebas; contarlas si el alcance incluye programacion.
- Si el sistema usa radio, contar alimentaciones y pilas/baterias si son relevantes.
- Si el sistema usa bus, contar cableado bus y fuentes/acopladores.

## Checklist

- [ ] Protocolo identificado o marcado como pendiente.
- [ ] Sensores contados por tipo.
- [ ] Actuadores contados por canal.
- [ ] Controladores/gateways contados.
- [ ] Programacion y escenas separadas.
- [ ] Integracion con electricidad/clima/fontaneria marcada.
- [ ] Pruebas y puesta en marcha incluidas o excluidas.
