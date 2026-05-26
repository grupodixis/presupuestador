# Entorno de Conteo de Instalaciones

Base documental para que un agente IA mida y cuente instalaciones de domotica, IoT, electricidad y fontaneria a partir de planos, memorias, fotos o descripciones de obra.

El objetivo no es calcular el precio final, sino producir una medicion clara y auditable que despues pueda usarse en presupuestacion.

## Ambito

- Instalaciones electricas de baja tension.
- Instalaciones de domotica residencial o terciaria.
- Instalaciones IoT, sensorizacion, comunicaciones y control.
- Instalaciones de fontaneria, ACS, saneamiento y riego basico.

## Estructura

```text
/
├── README.md
├── skills/                 # Instrucciones por tipo de instalacion
├── reglas-conteo/          # Criterios para transformar planos en unidades
├── plantillas/             # Tablas de salida y checklists
├── ejemplos/               # Ejemplos de medicion
└── glosario/               # Terminos especificos de conteo
```

## Flujo de trabajo del agente

1. Identificar la disciplina: electricidad, domotica, IoT o fontaneria.
2. Separar el alcance por estancia, zona, planta o cuadro/equipo.
3. Contar puntos terminales: enchufes, interruptores, luminarias, tomas de agua, sensores, actuadores, etc.
4. Contar equipos principales: cuadros, gateways, routers, colectores, termos, bombas, valvulas.
5. Estimar tramos lineales cuando el plano lo permita: canalizacion, cable, tubo, saneamiento.
6. Anotar partidas auxiliares obligatorias: cajas, mecanismos, protecciones, pruebas, certificados.
7. Marcar dudas, exclusiones y supuestos.
8. Entregar una tabla de medicion con unidades, cantidades y criterio de conteo.

## Principios de conteo

- Contar por punto cuando la instalacion termina en un elemento utilizable.
- Contar por metro lineal cuando el coste depende principalmente del recorrido.
- Contar por unidad los equipos, cuadros, llaves, sensores, actuadores y terminales.
- No mezclar puntos de uso distinto aunque compartan caja o canalizacion.
- No duplicar cableado o tuberia si ya esta incluido dentro de un punto tipo; si se mide aparte, indicarlo.
- Separar obra nueva, reforma, visto, empotrado, exterior y zona humeda.
- Registrar siempre los supuestos usados cuando falten planos o medidas.

## Salida recomendada

Usar `plantillas/plantilla-medicion-instalaciones.md` para generar:

- Resumen de alcance.
- Tabla de mediciones por disciplina.
- Tabla de dudas y datos pendientes.
- Exclusiones.
- Checklist final.
