# Skill: Presupuestación de Naves Industriales, Agrícolas y Ganaderas

## 1. Propósito

Esta skill permite al agente razonar y calcular presupuestos técnicos y comerciales completos para la construcción y suministro de **naves prefabricadas a dos aguas**, reproduciendo y perfeccionando la lógica paramétrica de ingeniería (inspirada en la ingeniería inversa de Patec y el Código Técnico de la Edificación CTE).

---

## 2. Parámetros Clave de Entrada

1. **Luz ($L$):** Ancho libre entre pilares exteriores (8 m a 45 m).
2. **Longitud ($S$):** Fondo de la nave (12 m a 150 m).
3. **Altura de pilares ($H$):** Altura útil de pilares hasta el alero (3.5 m a 12 m).
4. **Pendiente de cubierta:** 10% a 25% (típico 15% para panel sándwich y chapa grecada).
5. **Ubicación y Entorno:**
   - Rugosidad del viento (Grados I a V según CTE DB-SE-AE).
   - Zona de nieve (según altitud de la localidad).
   - Tensión admisible del terreno (por defecto $\sigma_{adm} = 1.50 \text{ kg/cm}^2$).
6. **Uso Previsto:**
   - Agrícola (maquinaria/grano).
   - Ganadera (porcina, avícola, vacuno, etc. — requiere valorar falso techo PURAL y resistencia a amoníacos).
   - Industrial / Logística / Almacén / Deportiva.
7. **Modalidad:**
   - Solo Suministro ("Kit mecano prefabricado" listo para montar).
   - Suministro y Montaje completo (incluye grúas, elevadores y montaje en obra).

---

## 3. Fórmulas de Modulación y Geometría

### 3.1 Vanos y Pórticos
$$\text{Número de vanos } N_{vanos} = \max\left(2, \text{round}\left(\frac{\text{Longitud}}{6.0}\right)\right)$$
$$\text{Separación entre pórticos } d = \frac{\text{Longitud}}{N_{vanos}}$$
$$\text{Pórticos tipo intermedios } = N_{vanos} - 1$$
$$\text{Pórticos testeros (frontales) } = 2$$
$$\text{Total de pórticos } = N_{vanos} + 1$$

### 3.2 Superficies y Altura de Cumbrera
$$\text{Altura en cumbrera } H_{cumbrera} = H + \left(\frac{L}{2} \times \frac{\text{Pendiente \%}}{100}\right)$$
$$\text{Longitud de cada faldón inclinado } L_{faldon} = \sqrt{\left(\frac{L}{2}\right)^2 + (H_{cumbrera} - H)^2}$$
$$\text{Superficie de cubierta total } = 2 \times L_{faldon} \times \text{Longitud}$$
$$\text{Superficie de fachadas laterales } = 2 \times \text{Longitud} \times H$$
$$\text{Superficie de hastiales frontales } = 2 \times \left[(L \times H) + \frac{L \times (H_{cumbrera} - H)}{2}\right]$$
$$\text{Superficie total de cerramiento vertical } = \text{Fachadas laterales} + \text{Hastiales}$$

### 3.3 Correas de Cubierta y Cerramiento
- **Correas de cubierta (CorreaC):**
  $$\text{Líneas por faldón} = \text{ceil}\left(\frac{L_{faldon}}{1.50}\right) + 1$$
  $$\text{Metros lineales de correas de cubierta} = 2 \times \text{Líneas} \times \text{Longitud}$$
- **Correas laterales (CorreaL):**
  $$\text{Líneas por fachada} = \text{ceil}\left(\frac{H}{1.60}\right)$$
- **Correas de testero (CorreaT):**
  $$\text{Líneas por hastial} = \text{ceil}\left(\frac{H_{medio}}{1.60}\right)$$

---

## 4. Estimación de Acero y Cimentación

### 4.1 Peso de Acero Estructural ($kg/m^2$)
El ratio de acero estructural ($R_{acero}$) en $\text{kg/m}^2$ de superficie construida varía en función de la luz y la altura:
- Luces de 10 a 15 m: $18 \text{ a } 24 \text{ kg/m}^2$
- Luces de 16 a 22 m: $24 \text{ a } 30 \text{ kg/m}^2$
- Luces de 23 a 32 m: $30 \text{ a } 38 \text{ kg/m}^2$
- Ajuste por viento/nieve severos o costa: $+15\%$

$$\text{Kilos totales de acero} = \text{Superficie construida} \times R_{acero}$$

### 4.2 Cimentación y Solera
1. **Zapatas:**
   - Volumen de zapata intermedia típica: $1.80 \times 1.80 \times 0.80 \text{ m} \approx 2.59 \text{ m}^3$.
   - Volumen de zapata de testero típica: $1.40 \times 1.40 \times 0.70 \text{ m} \approx 1.37 \text{ m}^3$.
   - Riostras de atado: sección $0.40 \times 0.50 \text{ m}$ a lo largo de todo el perímetro y pórticos.
2. **Hormigón armado total:** Suma de zapatas + riostras.
3. **Acero corrugado B500S:** Entre 35 y 45 kg de acero por $\text{m}^3$ de hormigón en cimentación.
4. **Solera de hormigón:**
   - Espesor típico: 15 cm a 20 cm.
   - Volumen solera: $\text{Superficie construida} \times \text{Espesor}$.
   - Zahorra compactada: $\text{Superficie} \times 0.15 \text{ m}^3$.
   - Mallazo electrosoldado: $\text{Superficie} \times 1.15$ (15% solapes y mermas).

---

## 5. Criterios de Costes y Precios de Mercado Base

*Valores de referencia editables en el presupuestador:*
- **Acero laminado soldado (fabricación + imprimación + placas):** $2.10 \text{ €/kg}$ a $2.80 \text{ €/kg}$.
- **Chapa grecada 0.6 mm prelacada:** $12.50 \text{ €/m}^2$.
- **Panel sándwich 30-40 mm:** $19.50 \text{ a } 23.00 \text{ €/m}^2$.
- **Panel sándwich 50-60 mm:** $24.00 \text{ a } 28.50 \text{ €/m}^2$.
- **Panel sándwich 80-100 mm:** $30.00 \text{ a } 36.00 \text{ €/m}^2$.
- **Lucernarios de policarbonato:** $28.00 \text{ €/m}^2$.
- **Remates de cumbrera / esquinas / goterones:** $12.00 \text{ a } 15.00 \text{ €/ml}$.
- **Puerta corredera / abatible 5x5 m:** $2,800 \text{ a } 3,600 \text{ €/ud}$.
- **Puerta peatonal con premarco:** $350 \text{ a } 450 \text{ €/ud}$.
- **Excavación de zapatas y riostras:** $8.50 \text{ €/m}^3$.
- **Hormigón H25 en cimentación:** $95.00 \text{ €/m}^3$.
- **Acero corrugado B500S:** $1.35 \text{ €/kg}$ colocado.
- **Solera de hormigón fratasada (incluye hormigón + extendido + pulido cuarzo):** $22.00 \text{ a } 28.00 \text{ €/m}^2$.
- **Montaje en obra (con grúa y tijera elevadora):** $12.00 \text{ a } 18.00 \text{ €/m}^2$ construido.
