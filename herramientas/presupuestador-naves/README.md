# Configurador y Presupuestador de Naves Industriales y Agrícolas

Aplicación web interactiva desarrollada para presupuestar naves prefabricadas a dos aguas en tiempo real, replicando y modernizando la lógica de ingeniería de [PATEC](https://www.patec.org/presupuesto.php).

---

## Características Principales

1. **Cálculo Reactivo Instantáneo:**
   - Modulación automática de vanos ($Longitud / 6.0\text{ m}$).
   - Cálculo de pórticos centrales, testeros y líneas de correas (cubierta, laterales, frontales).
   - Estimación paramétrica de peso de acero estructural ($kg/m^2$) según luz, altura y sobrecarga de viento.
   - Cubicaciones completas de cimentación (zapatas, riostras, hormigón de limpieza, acero B500S) y solera (zahorra, lámina PE, mallazo, hormigón pulido H25).
2. **Las 23 Partidas del Presupuesto (PATEC Match):**
   - Desglose exhaustivo en 4 capítulos con mediciones, unidades, precios unitarios e importes.
3. **Visor 3D Paramétrico (Three.js):**
   - Renderiza en 3D en tiempo real la nave a medida que se mueven los controles de luz, longitud y altura.
   - Controles orbitales para rotar, hacer zoom y desplazar la cámara.
   - Botones para alternar visibilidad de estructura metálica, cerramientos de fachada y cubierta.
4. **Exportación e Impresión:**
   - Modo de impresión optimizado para generar PDF técnico y comercial.
   - Exportación de mediciones y datos en formato JSON para conexión con ERP / FactuSOL.

---

## Archivos del Módulo

- [`index.html`](file:///c:/Users/grupo/Documents/Presupuestador/herramientas/presupuestador-naves/index.html): Interfaz web con Tailwind CSS.
- [`calculo_naves.js`](file:///c:/Users/grupo/Documents/Presupuestador/herramientas/presupuestador-naves/calculo_naves.js): Motor de dimensionamiento geométrico y escandallos.
- [`visor3d.js`](file:///c:/Users/grupo/Documents/Presupuestador/herramientas/presupuestador-naves/visor3d.js): Motor 3D con Three.js.
- [`provincias.js`](file:///c:/Users/grupo/Documents/Presupuestador/herramientas/presupuestador-naves/provincias.js): Base de datos de provincias y cargas CTE.
- [`abrir-presupuestador.ps1`](file:///c:/Users/grupo/Documents/Presupuestador/herramientas/presupuestador-naves/abrir-presupuestador.ps1): Script PowerShell para abrir la herramienta con un clic.

---

## Cómo Ejecutar

Basta con hacer doble clic en `abrir-presupuestador.ps1` o abrir directamente [`index.html`](file:///c:/Users/grupo/Documents/Presupuestador/herramientas/presupuestador-naves/index.html) en cualquier navegador moderno (Chrome, Edge, Firefox).
