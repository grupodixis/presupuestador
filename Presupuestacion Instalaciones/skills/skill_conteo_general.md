# Skill: Conteo General de Instalaciones

## Cuándo usar esta skill

Cuando se necesite convertir planos, fotos, croquis, memorias o descripciones en una medicion de unidades de instalacion.

## Datos minimos necesarios

- Tipo de inmueble: vivienda, local, nave, oficina, comunidad, exterior.
- Alcance: obra nueva, reforma parcial, ampliacion o sustitucion.
- Disciplinas incluidas: electricidad, domotica, IoT, fontaneria.
- Planos, croquis o descripcion por estancias.
- Nivel de detalle esperado: conteo rapido, medicion preliminar o medicion para presupuesto.

## Metodo de trabajo

1. Dividir la obra por zonas: planta, estancia, fachada, sala tecnica, cuarto humedo o area exterior.
2. Identificar simbolos y leyendas antes de contar.
3. Contar elementos terminales visibles.
4. Contar equipos principales y elementos de control.
5. Medir o estimar recorridos lineales solo si hay escala, cotas o referencia fiable.
6. Agrupar por unidad de medicion: ud, punto, ml, conjunto, cuadro, equipo.
7. Separar elementos empotrados, vistos, exteriores, estancos y especiales.
8. Registrar supuestos y dudas en la misma medicion.

## Reglas comunes

- Si no hay escala, no inventar metros lineales exactos; usar `pendiente_de_medicion` o rango razonado.
- Si un simbolo no esta claro, contarlo como partida dudosa y pedir confirmacion.
- Si un elemento tiene dos funciones, contar ambas solo si requieren material o mano de obra diferenciada.
- Si el plano muestra preinstalacion, no contar equipo final salvo que el alcance lo incluya.
- Si hay varias plantas repetidas, contar una planta tipo y multiplicar indicando el factor.

## Errores frecuentes

- Contar interruptores como puntos de luz sin separar mando y luminaria.
- Olvidar cajas de registro, colectores, cuadros o gateways.
- Medir canalizacion dos veces: una dentro del punto y otra como ml separado.
- No separar zonas humedas o exteriores, que cambian material y proteccion.
- Presuponer marcas, protocolos o gamas no indicadas.

## Formato de salida

La salida debe incluir:

1. Alcance interpretado.
2. Criterio de conteo usado.
3. Tabla de medicion por disciplina y zona.
4. Dudas y datos pendientes.
5. Exclusiones.
6. Checklist final.
