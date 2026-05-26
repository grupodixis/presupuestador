# Skill: Conteo de IoT

## Cuándo usar esta skill

Para instalaciones de dispositivos conectados, sensorizacion, telemetria, monitorizacion, gateways, redes, control remoto y automatismos ligeros en vivienda, local, nave, exterior o comunidad.

## Unidades habituales

| Elemento | Unidad | Criterio de conteo |
|---|---:|---|
| Sensor IoT | ud | Cada dispositivo de medicion o deteccion |
| Actuador IoT | ud | Cada rele, valvula, cerradura, sirena o control fisico |
| Gateway / concentrador | ud | Cada pasarela de comunicaciones |
| Nodo repetidor | ud | Cada repetidor o router mesh |
| Punto de red RJ45 | ud | Cada toma terminal cableada |
| Punto WiFi / AP | ud | Cada punto de acceso |
| Alimentacion electrica | punto | Cada alimentacion dedicada a dispositivo |
| SIM / conectividad | ud | Cada linea o servicio necesario |
| Cuadro o caja de control | ud | Cada envolvente con electronica |
| Integracion cloud / app | conjunto | Configuracion por plataforma o sistema |

## Datos a extraer

- Caso de uso: medicion, alarma, control, eficiencia, mantenimiento, seguridad.
- Ubicacion de dispositivos: interior, exterior, sala tecnica, cubierta, arqueta.
- Protocolo: WiFi, Ethernet, LoRaWAN, NB-IoT, Zigbee, BLE, 4G/5G, Modbus, MQTT.
- Alimentacion: red, PoE, bateria, solar.
- Necesidad de cobertura, repetidores o antenas.
- Plataforma cloud o servidor local.
- Retencion de datos, alarmas y usuarios.

## Criterios especificos

- Contar el dispositivo fisico y su punto de alimentacion por separado si ambos requieren instalacion.
- Separar sensores cableados de sensores a bateria.
- En exterior, marcar grado IP, soporte, antena y proteccion frente a intemperie.
- Si hay comunicaciones criticas, contar pruebas de cobertura y configuracion.
- No asumir que WiFi existente es suficiente; marcar validacion de cobertura.
- Separar alta/configuracion de plataforma de la instalacion fisica.

## Checklist

- [ ] Dispositivos por tipo contados.
- [ ] Gateways y repetidores contados.
- [ ] Alimentaciones o PoE identificados.
- [ ] Cobertura y protocolo documentados.
- [ ] Configuracion cloud/app incluida o excluida.
- [ ] Soportes, cajas y proteccion exterior considerados.
- [ ] Pruebas de comunicacion previstas.
