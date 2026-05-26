# Analisis de Medicion - Contadores Telelectura y Telecontrol
## Es Migjorn Gran - Expediente E0038/2026/000001

## Alcance interpretado

- **Disciplinas incluidas**: IoT (telelectura de contadores de agua), IoT/automatizacion (telecontrol de pozos y depositos), electricidad (alimentacion de equipos de campo), fontaneria (conexion hidraulica de contadores)
- **Zonas incluidas**: 969 puntos de suministro (domicilios + municipales) + 4 pozos (Son Xua, Es Revolt, Es Pujolet, Es Boeret) + 4 depositos (Son Xua 400m3, Can Borras 380m3, Piruli 50m3, prefabricado 20m3)
- **Zonas excluidas**: Red de distribucion enterrada (no se interviene), captaciones fuera del nucleo, obra civil de via publica
- **Criterio general de conteo**: Conteo por equipos/componentes extraidos del presupuesto del proyecto; verificar cantidades antes de ofertar

## Medicion por disciplina

### IoT - Telelectura (LOTE 1)

| Zona | Partida | Unidad | Cantidad | Precio proyecto | Criterio / observacion |
|---|---|---|---|---|---|
| Domicilios | Contador ultrasonidos DN13/15mm Q3=2.5 R800 dual LoRaWAN+wM-Bus | ud | 1 | ~168,00 | Abonado individual; incluye retirada existente + instalacion + configuracion NFC + precintado |
| Domicilios | Contador ultrasonidos DN20mm Q3=4 R800 dual LoRaWAN+wM-Bus | ud | 960 | 168,21 | Tipo mayoritario; mismo alcance |
| Domicilios | Contador ultrasonidos DN25mm Q3=6.3 R800 dual LoRaWAN+wM-Bus | ud | 5 | 172,87 | Calibre superior para consumos altos |
| Domicilios | Contador ultrasonidos DN30mm Q3=10 R800 dual LoRaWAN+wM-Bus | ud | 2 | 212,42 | Calibre superior |
| Domicilios | Contador ultrasonidos DN40mm Q3=16 R800 dual LoRaWAN+wM-Bus | ud | 1 | 305,53 | Calibre maximo; suministro municipal grande |
| Red IoT | Gateway LoRaWAN IoTib | ud | 0 | 0,00 | A cargo de IB Digital - verificar cobertura |
| Plataforma | Software gestion ARSON METERING/NETMORE o equivalente | ud | 1 | 1.710,00 | 12 anos soporte incluidos; licencia incl. en precio contador |
| Domicilios | App abonado (clave privada) | conjunto | 1 | incluido | Acceso a datos de consumo propio |

**Total ud contadores IoT: 969**

### IoT/SCADA - Telecontrol (LOTE 2)

| Zona | Partida | Unidad | Cantidad | Precio proyecto | Criterio / observacion |
|---|---|---|---|---|---|
| Pozo Son Xua | Estacion remota S4W Small 8-2-2 + GSM4 + ETH | ud | 1 | 1.369,03 | Captacion principal |
| Pozo Son Xua | Alimentacion 24VDC 90W carril | ud | 1 | 122,58 | |
| Pozo Son Xua | Bateria 12Vcc 12Ah plomo gel | ud | 1 | 46,28 | |
| Pozo Son Xua | Antena 2G-4G 0dB SMA-M 4m | ud | 1 | 46,37 | |
| Pozo Son Xua | Emisor pulsos para contador | ud | 2 | 113,45 | 2 contadores en pozo |
| Pozo Son Xua | SIM tarjeta comunicaciones (coste anual) | ud | 1 | 113,50 | |
| Pozo Son Xua | Instalacion, prog. y config. S4W en armario nuevo | ud | 1 | 490,32 | |
| Pozo Son Xua | Captador nivel CNPI 0-6m con cable 9m | ud | 1 | 251,90 | |
| Pozo Son Xua | Datalogger DL4-S LS42 FLEX | ud | 1 | 454,00 | |
| Pozo Es Revolt | Estacion remota S4W Small 8-2-2 + GSM4 + ETH | ud | 1 | 1.369,03 | Problemas terbolesa/manganeso |
| Pozo Es Revolt | Alimentacion 24VDC | ud | 1 | 122,58 | |
| Pozo Es Revolt | Bateria 12Vcc | ud | 1 | 46,28 | |
| Pozo Es Revolt | Antena 2G-4G | ud | 1 | 46,37 | |
| Pozo Es Revolt | Emisor pulsos | ud | 2 | 113,45 | |
| Pozo Es Revolt | SIM tarjeta (coste anual) | ud | 1 | 113,50 | |
| Pozo Es Revolt | Instalacion y config. S4W | ud | 1 | 490,32 | |
| Pozo Es Revolt | Ampliacion 16DI | ud | 1 | 1.069,73 | |
| Pozo Es Revolt | Captador nivel | ud | 1 | 251,90 | |
| Pozo Es Pujolet | Estacion remota S4W Small | ud | 1 | 1.369,03 | Problemas manganeso |
| Pozo Es Pujolet | Alimentacion 24VDC | ud | 1 | 122,58 | |
| Pozo Es Pujolet | Bateria 12Vcc | ud | 1 | 46,28 | |
| Pozo Es Pujolet | Antena 2G-4G | ud | 1 | 46,37 | |
| Pozo Es Pujolet | Emisor pulsos | ud | 2 | 113,45 | |
| Pozo Es Pujolet | SIM tarjeta | ud | 1 | 113,50 | |
| Pozo Es Pujolet | Captador nivel | ud | 1 | 251,90 | |
| Pozo Es Pujolet | Captador presion CPR 10bar IP68 | ud | 1 | 113,45 | |
| Pozo Es Boeret | Estacion remota S4W Small | ud | 1 | 1.369,03 | |
| Pozo Es Boeret | Alimentacion 24VDC | ud | 1 | 122,58 | |
| Pozo Es Boeret | Bateria 12Vcc | ud | 1 | 46,28 | |
| Pozo Es Boeret | Antena 2G-4G | ud | 1 | 46,37 | |
| Pozo Es Boeret | Emisor pulsos | ud | 2 | 113,45 | |
| Pozo Es Boeret | SIM tarjeta | ud | 1 | 113,50 | |
| Pozo Es Boeret | Captador nivel | ud | 1 | 251,90 | |
| Pozo Es Boeret | Ampliacion 16DI | ud | 1 | 1.061,73 | |
| Pozo Es Boeret | Captador presion | ud | 1 | 113,45 | |
| Deposito Son Xua (n1) | Captador nivel | ud | 1 | 251,90 | 400m3, cota +105 |
| Deposito Can Borras (n2) | S4W LARGE 16-4-4 1000I + GSM4 + ETH | ud | 1 | 2.131,46 | Centro de control principal |
| Deposito Can Borras (n2) | Alimentacion 24VDC | ud | 1 | 251,90 | |
| Deposito Can Borras (n2) | Bateria 12Vcc | ud | 1 | 46,28 | |
| Deposito Can Borras (n2) | Antena 2G-4G | ud | 1 | 46,37 | |
| Deposito Can Borras (n2) | Emisor pulsos | ud | 1 | 113,45 | |
| Deposito Can Borras (n2) | SIM tarjeta | ud | 1 | 113,50 | |
| Deposito Can Borras (n2) | Captador nivel | ud | 1 | 251,90 | |
| Deposito Can Borras (n2) | Captador presion | ud | 1 | 113,45 | |
| Deposito Can Borras (n2) | Pantalla tactil 7" encastrable | ud | 1 | 340,50 | |
| Deposito Can Borras (n2) | Datalogger DL4-S LS42 FLEX | ud | 1 | 1.889,84 | |
| Deposito Piruli (n3) | Captador nivel | ud | 1 | 251,90 | Elevado 50m3 |
| Deposito Piruli (n3) | Captador presion | ud | 1 | 113,45 | |
| Deposito Prefabricado (n4) | Captador nivel | ud | 1 | 251,90 | Fibra 20m3, pre-filtracion |
| Deposito Prefabricado (n4) | Captador presion | ud | 1 | 113,45 | |
| Deposito Prefabricado (n4) | Captador presion | ud | 1 | 113,45 | |
| Centro control | Ordenador telecontrol doble monitor + SAI | ud | 1 | 1.887,84 | En ayuntamiento |
| Centro control | Software Scada LX Clase 5000 + OPC UA + SG4000 VPN | ud | 1 | 17.207,84 | 10 anos mantenimiento |
| Centro control | Alta de estaciones en telecontrol central | ud | 4 | - | Pozos: definicion senales y pantallas |
| General | Formacion presencial al personal del ayuntamiento | ud | 1 | incluido | Configuracion, lectura, alarmas |

### Electricidad - Alimentacion de equipos

| Zona | Partida | Unidad | Cantidad | Observacion |
|---|---|---|---|---|
| Pozos (4) | Alimentacion S4W desde cuadro existente | punto | 4 | Los pozos ya tienen acometida electrica (transformador 65,8kW + FV 50kW) |
| Pozos (4) | Fuente alimentacion 24VDC 90W carril DIN | ud | 4 | Incluida en presupuesto S4W |
| Pozos (4) | Bateria respaldo 12Vcc 12Ah | ud | 4 | Incluida en presupuesto |
| Deposito Can Borras | Alimentacion S4W LARGE desde cuadro | punto | 1 | Cuadro existente en deposito |
| Deposito Can Borras | Fuente alimentacion 24VDC 90W | ud | 1 | Incluida |
| Deposito Can Borras | Bateria respaldo | ud | 1 | Incluida |
| Centro control | SAI para servidor/PC telecontrol | ud | 1 | Incluido en presupuesto |

### Fontaneria - Conexion de contadores

| Zona | Partida | Unidad | Cantidad | Observacion |
|---|---|---|---|---|
| Domicilios | Retirada contador existente | ud | 969 | Incluida en precio unitario |
| Domicilios | Suministro e instalacion contador ultrasonidos nuevo | ud | 969 | Incluye llaves, enlaces, juntas |
| Domicilios | Prueba estanquidad y verificacion funcionamiento | ud | 969 | Incluida |
| Domicilios | Precintado | ud | 969 | Incluido |
| Domicilios | Limpieza alojamiento tras intervencion | ud | 969 | Incluida |
| Pozos (4) | Emisor de pulsos sobre contador existente | ud | 8 | 2 por pozo para medicion de caudal |

### Resumen por disciplina

| Disciplina | Numero de partidas | Observaciones |
|---|---|---|
| IoT - Telelectura (L1) | 6 partidas + 1 plataforma | 969 contadores inteligentes con comunicacion dual |
| IoT/SCADA - Telecontrol (L2) | ~50 partidas | 5 estaciones S4W, 3 dataloggers, Scada, sensores |
| Electricidad | 10 puntos/equipos | Alimentaciones 24VDC y baterias; equipos incluidos |
| Fontaneria | 5 partidas x 969 ud | Retirada e instalacion de contadores; incluye pruebas |

## Analisis de precios unitarios

### LOTE 1 - Desglose estimado por contador (DN20mm a 168,21 EUR)

| Componente | Coste estimado (EUR) | % |
|---|---|---|
| Contador ultrasonidos SmartIO (o equivalente) | ~75-90 | 45-53% |
| Accesorios hidraulicos (llaves, enlaces, juntas, precinto) | ~10-15 | 6-9% |
| Mano de obra instalacion (1 h/ud x cuadrilla) | ~25-35 | 15-21% |
| Retirada y gestion residuo contador antiguo | ~5-8 | 3-5% |
| Configuracion NFC y pruebas | ~5-8 | 3-5% |
| Parte proporcional software gestion (12 anos) | ~8-12 | 5-7% |
| Logistica, desplazamientos, administracion | ~10-15 | 6-9% |
| **Subtotal** | **~138-183** | **82-109%** |

**Nota**: El precio de 168,21 EUR/ud es ajustado. Con los costes actuales de contadores ultrasonicos dual LoRaWAN+wM-Bus (SmartIO, Contazara, Diehl, etc.), el margen puede ser muy reducido. **Verificar precio de compra con distribuidor antes de ofertar.**

### LOTE 2 - Equipos principales

| Equipo | Precio proyecto | Estimacion mercado |
|---|---|---|
| S4W Small 8-2-2+GSM4+ETH | 1.369,03 EUR | 1.100-1.400 EUR |
| S4W LARGE 16-4-4+GSM4+ETH | 2.131,46 EUR | 1.800-2.300 EUR |
| DL4W Datalogger | 1.889,84 EUR | 1.500-2.000 EUR |
| LX Scada + OPC UA + SG4000 + 10 anos | 17.207,84 EUR | 15.000-20.000 EUR |
| Captador nivel 0-6m | 251,90 EUR | 200-300 EUR |
| Captador presion 10bar | 113,45 EUR | 100-150 EUR |

## Estrategia de oferta

### Analisis de puntuacion

El 70% del peso es economico (70 pts sobre 100). Con baja agresiva se puede ganar mucho, pero el margen es ajustado.

**Simulacion para LOTE 1 (PEC = 246.083,23 EUR):**

| Baja (%) | Precio oferta | Puntuacion economica (si el mas bajo es este) |
|---|---|---|
| 0% | 246.083 EUR | 70,0 pts |
| 5% | 233.779 EUR | 73,7 pts |
| 10% | 221.475 EUR | 77,8 pts |
| 15% | 209.171 EUR | 82,4 pts |
| 20% | 196.867 EUR | 87,5 pts |

**Resto de puntuacion:**

| Mejora | Puntos |
|---|---|
| 1 ano extra garantia | +2 pts |
| 3 anos extra garantia | +6 pts |
| 5 anos extra garantia | +10 pts |
| 15 dias menos plazo | +10 pts |
| 30 dias menos plazo | +20 pts |

### Escenarios recomendados

| Escenario | Baja economica | Mejora garantia | Mejora plazo | Puntuacion estimada |
|---|---|---|---|---|
| Conservador | 3-5% | +2 anos (4 pts) | -15 dias (10 pts) | ~77-80 pts |
| Agresivo | 8-12% | +3 anos (6 pts) | -20 dias (13 pts) | ~85-90 pts |
| Maximo | 15-18% | +5 anos (10 pts) | -30 dias (20 pts) | ~95-100 pts |

## Dudas y datos pendientes

| Duda | Impacto | Confirmacion necesaria |
|---|---|---|
| Precio real de contador SmartIO DN20 | Alto | Solicitar oferta a distribuidor (Contazara, Cohisa, Diehl) |
| Precio real SOFREL S4W + Scada | Alto | Solicitar oferta a distribuidor SOFREL |
| Cobertura IoTib en todo el nucleo urbano | Medio | Consultar con IB Digital disponibilidad en Migjorn Gran |
| Convenio Ayuntamiento-IB Digital firmado? | Medio | Solicitar copia del convenio en mesa de contratacion |
| Estado real de arquetas de contadores | Medio | Pedir muestreo visual previo (10-20 uds) |
| Horario de acceso a domicilios permitido | Medio | Consultar ordenanza municipal |
| Contadores en comunidades con bateria centralizada? | Medio | Pedir detalle del padron de abonados |
| Coste anual SIM Lote 2 a cargo de quien? | Medio | Aclarar en pliegos si es coste recurrente del ayto |
| Partida de via publica inexistente en PEM | Bajo | Confirmar si se requiere reposicion de pavimento |

## Exclusiones

- Obra civil: apertura/cierre de zanjas, reposicion de pavimento, demoliciones
- Red de distribucion enterrada (no se interviene en tuberias de la via publica)
- Instalacion electrica de los pozos (ya existente): solo se alimentan los equipos nuevos
- Grupo electrogeno, grupo de presion, valvulas reductoras, contadores sectoriales
- Legalizacion de instalaciones o boletines
- Marcas concretas: el proyecto admite equivalentes
- Estudio de seguridad y salud (lo aporta el proyecto)
- Estudio de gestion de residuos (lo aporta el proyecto)

## Checklist final

- [x] Se han separado unidades por disciplina (IoT, electricidad, fontaneria)
- [x] Se han marcado supuestos y pendientes
- [x] Se han separado equipos principales y auxiliares (S4W + accesorios)
- [x] Se ha verificado el presupuesto del proyecto contra las cantidades
- [x] Se ha identificado el riesgo de precio de material
- [x] Se ha analizado la estrategia de puntuacion
- [x] La medicion puede pasarse a presupuesto propio
- [x] Checklist skill IoT aplicado (dispositivos, gateways, alimentacion, cobertura, configuracion cloud)
