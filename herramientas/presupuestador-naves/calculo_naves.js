/**
 * calculo_naves.js
 * Motor de cálculo y dimensionamiento paramétrico para presupuestación de naves.
 * Desarrollado según la normativa de edificación CTE DB-SE-AE.
 */
const PRECIOS_DEFECTO = {
    // Capítulo 1: Estructura y Cerramientos
    precio_acero_kg: 3.45,              // €/kg acero S275JR laminado, soldado, granallado e imprimado
    precio_chapa_cubierta_m2: 22.00,     // €/m2 chapa grecada 0.6mm (cubierta o fachada)
    precio_panel_30_m2: 42.00,          // €/m2 panel sándwich 30mm PUR/PIR
    precio_panel_35_m2: 44.00,          // €/m2 panel sándwich 35mm fachada
    precio_panel_40_m2: 46.00,          // €/m2 panel sándwich 40mm
    precio_panel_50_m2: 49.00,          // €/m2 panel sándwich 50mm
    precio_panel_60_m2: 52.00,          // €/m2 panel sándwich 60mm
    precio_panel_70_m2: 56.00,          // €/m2 panel sándwich 70mm
    precio_panel_80_m2: 60.00,          // €/m2 panel sándwich 80mm
    precio_panel_90_m2: 64.00,          // €/m2 panel sándwich 90mm
    precio_panel_100_m2: 68.00,         // €/m2 panel sándwich 100mm
    precio_panel_pural_m2: 48.00,       // €/m2 sándwich + PURAL agropecuario
    precio_panel_teja_m2: 46.00,        // €/m2 panel sándwich 30mm imitación teja
    precio_placa_alveolar_m2: 48.00,    // €/m2 placa alveolar pretensada 150mm (suministro)
    precio_bloque_hormigon_m2: 38.00,   // €/m2 bloque hormigón 20x20x40 / termoarcilla (suministro)
    precio_lucernario_m2: 45.00,        // €/m2 policarbonato celular / poliéster
    precio_falso_techo_m2: 50.00,       // €/m2 falso techo PURAL 30mm
    precio_remate_cumbrera_ml: 20.00,   // €/ml chapa plegada 620mm
    precio_remate_lateral_ml: 20.00,    // €/ml remate hastial
    precio_remate_esquina_ml: 18.00,    // €/ml remate de esquinas
    precio_remate_vierteaguas_ml: 16.00, // €/ml remate vierteaguas coronación muro/zócalo
    precio_canalon_exterior_ml: 24.00,  // €/ml canalón exterior lacado con bajantes en aleros
    precio_canalon_interior_ml: 28.00,  // €/ml canalón interior oculto estanco detras de peto
    precio_puerta_grande_ud: 3350.00,   // €/ud puerta 5x5m basculante/corredera
    precio_puerta_peatonal_ud: 850.00,  // €/ud puerta 1x2.10m
    precio_tornillo_ud: 1.20,           // €/ud tornillería 8.8

    // Capítulo 2: Cimentación
    precio_explanacion_m3: 7.50,        // €/m3 explanación y desbroce
    precio_excavacion_m3: 14.00,        // €/m3 excavación de zapatas y zanjas
    precio_hormigon_limpieza_m3: 95.00, // €/m3 hormigón H10
    precio_acero_corrugado_kg: 2.10,    // €/kg acero B500S colocado
    precio_placa_anclaje_ud: 95.00,     // €/ud placa anclaje con pernos y encamillado
    precio_hormigon_h25_cimen_m3: 140.00,// €/m3 hormigón armado H25 en zapatas/riostras

    // Capítulo 3: Solera
    precio_zahorra_m3: 35.00,           // €/m3 zahorra artificial extendida y compactada
    precio_lamina_pe_m2: 2.20,          // €/m2 lámina PE 100 micras
    precio_mallazo_m2: 7.50,            // €/m2 mallazo electrosoldado #150x150x6
    precio_solera_h25_m3: 165.00,       // €/m3 hormigón H25 + extendido + fratasado pulido

    // Capítulo 4: Montaje Desglosado por Elemento
    precio_montaje_acero_kg: 0.65,          // €/kg montaje estructura con grúa
    precio_montaje_cubierta_m2: 8.50,       // €/m2 montaje cubierta
    precio_montaje_fachada_m2: 9.50,        // €/m2 montaje cerramiento lateral y hastiales (chapa/panel)
    precio_montaje_placa_alveolar_m2: 16.00,// €/m2 montaje y colocación de placas alveolares
    precio_montaje_bloque_m2: 28.00,        // €/m2 albañilería y ejecución muro de bloque
    precio_montaje_lucernarios_m2: 9.50,    // €/m2 montaje lucernarios
    precio_montaje_falso_techo_m2: 7.50,    // €/m2 montaje falso techo
    precio_montaje_remates_ml: 4.50,        // €/ml montaje y sellado de remates plegados
    precio_montaje_canalon_exterior_ml: 5.50, // €/ml montaje de canalón exterior lacado con bajantes
    precio_montaje_canalon_interior_ml: 7.50, // €/ml montaje y sellado estanco de canalón interior oculto
    precio_montaje_puerta_grande_ud: 550.0, // €/ud montaje puerta 5x5m
    precio_montaje_puerta_peatonal_ud: 140.0,// €/ud montaje puerta peatonal
    precio_alquiler_medios_aux_dia: 280.0,  // €/día plataformas elevadoras tijera y grúa

    // Capítulo 5: Portes y Transportes a Obra (Menorca)
    precio_porte_trailer_viaje: 480.00,     // €/viaje camión plataforma/grúa insular en Menorca

    // Capítulo 6: Proyecto Técnico y Cálculo Estructural
    precio_proyecto_tecnico: 3000.00        // € redacción proyecto técnico y cálculo de estructura visado
};

// Funciones de gestión de precios en localStorage / memoria
function obtenerPreciosConfigurados() {
    if (typeof localStorage !== 'undefined') {
        try {
            const guardados = localStorage.getItem('precios_presupuestador_naves');
            if (guardados) {
                return Object.assign({}, PRECIOS_DEFECTO, JSON.parse(guardados));
            }
        } catch (e) {
            console.error("Error al leer precios de localStorage:", e);
        }
    }
    return Object.assign({}, PRECIOS_DEFECTO);
}

function guardarPreciosConfigurados(nuevosPrecios) {
    if (typeof localStorage !== 'undefined') {
        try {
            localStorage.setItem('precios_presupuestador_naves', JSON.stringify(nuevosPrecios));
        } catch (e) {
            console.error("Error al guardar precios en localStorage:", e);
        }
    }
}

function restablecerPreciosConfigurados() {
    if (typeof localStorage !== 'undefined') {
        try {
            localStorage.removeItem('precios_presupuestador_naves');
        } catch (e) {
            console.error("Error al restablecer precios en localStorage:", e);
        }
    }
    return Object.assign({}, PRECIOS_DEFECTO);
}

/**
 * Calcula todas las mediciones, modulaciones y presupuesto desglosado
 */
function calcularPresupuestoNave(params) {
    const P = Object.assign({}, obtenerPreciosConfigurados(), params.precios || {});

    const luz = Math.max(6, parseFloat(params.luz) || 15);
    const longitud = Math.max(8, parseFloat(params.longitud) || 30);
    const altura = Math.max(3, parseFloat(params.altura) || 6);
    const pendiente = Math.max(5, parseFloat(params.pendiente) || 15);
    const tipoCubierta = params.tipoCubierta || 'chapa';
    const tipoFachada = params.tipoFachada || 'chapa';
    const pctLucernarios = Math.max(0, Math.min(30, parseFloat(params.pctLucernarios) || 0));
    const falsoTecho = !!params.falsoTecho;
    const conMontaje = true; // Venta exclusiva con montaje en obra en Menorca
    const numPuertasGrandes = params.numPuertasGrandes !== undefined ? parseInt(params.numPuertasGrandes) : 1;
    const numPuertasPeatonales = params.numPuertasPeatonales !== undefined ? parseInt(params.numPuertasPeatonales) : 1;
    const sobrecargaViento = parseFloat(params.sobrecargaViento) || 1.0; // Factor viento 1 a 5
    const tensionAdmisible = parseFloat(params.tensionAdmisible) || 1.5;

    // --- 1. Geometría y Modulación ---
    const supConstruida = luz * longitud;
    const nVanos = Math.max(2, Math.round(longitud / 6.0));
    const intereje = longitud / nVanos;
    const nPorticosTestero = 2;
    const nPorticosIntermedios = nVanos - 1;
    const totalPorticos = nVanos + 1;

    // Alturas
    const pendienteDecimal = pendiente / 100.0;
    const flechaCumbrera = (luz / 2.0) * pendienteDecimal;
    const alturaCumbrera = altura + flechaCumbrera;
    const longitudFaldon = Math.sqrt(Math.pow(luz / 2.0, 2) + Math.pow(flechaCumbrera, 2));

    // Superficies
    const supCubiertaReal = 2.0 * longitudFaldon * longitud;
    const supLucernarios = supCubiertaReal * (pctLucernarios / 100.0);
    const supCubiertaOpaca = supCubiertaReal - supLucernarios;

    // Superficies y Geometría de Fachada
    const supFachadasLaterales = 2.0 * longitud * altura;
    const supHastialIndividual = (luz * altura) + (luz * flechaCumbrera / 2.0);
    const supHastiales = 2.0 * supHastialIndividual;
    const supCerramientoTotal = supFachadasLaterales + supHastiales;
    const perimetroNave = 2.0 * (longitud + luz);

    // Detección del tipo de fachada y zócalo inferior
    let hMuro = 0;
    let tipoMuro = 'ninguno'; // 'bloque', 'alveolar', 'ninguno'
    let tipoSuperior = 'chapa'; // 'chapa', 'panel', 'ninguno'
    let espesorPanelFachada = 35;

    if (tipoFachada === 'nada') {
        tipoSuperior = 'ninguno';
        tipoMuro = 'ninguno';
        hMuro = 0;
    } else if (tipoFachada === 'bloque_total') {
        tipoMuro = 'bloque';
        tipoSuperior = 'ninguno';
        hMuro = altura;
    } else if (tipoFachada === 'alveolar_total') {
        tipoMuro = 'alveolar';
        tipoSuperior = 'ninguno';
        hMuro = altura;
    } else if (tipoFachada.startsWith('alveolar_')) {
        tipoMuro = 'alveolar';
        if (tipoFachada.startsWith('alveolar_12')) hMuro = 1.2;
        else if (tipoFachada.startsWith('alveolar_24')) hMuro = 2.4;
        else if (tipoFachada.startsWith('alveolar_36')) hMuro = 3.6;
        hMuro = Math.min(hMuro, altura);
        tipoSuperior = tipoFachada.endsWith('_panel') ? 'panel' : 'chapa';
    } else if (tipoFachada.startsWith('bloque_')) {
        tipoMuro = 'bloque';
        if (tipoFachada.startsWith('bloque_1')) hMuro = 1.0;
        else if (tipoFachada.startsWith('bloque_2')) hMuro = 2.0;
        else if (tipoFachada.startsWith('bloque_3')) hMuro = 3.0;
        hMuro = Math.min(hMuro, altura);
        tipoSuperior = tipoFachada.endsWith('_panel') ? 'panel' : 'chapa';
    } else if (tipoFachada === 'chapa') {
        tipoSuperior = 'chapa';
        tipoMuro = 'ninguno';
        hMuro = 0;
    } else {
        // Paneles sándwich continuos (panel35, panel40, etc.)
        tipoSuperior = 'panel';
        tipoMuro = 'ninguno';
        hMuro = 0;
        const matchEsp = tipoFachada.match(/\d+/);
        if (matchEsp) espesorPanelFachada = parseInt(matchEsp[0]);
    }

    // Peto Perimetral (Cubierta Oculta / Estética Cúbica)
    const conPeto = !!params.conPeto;
    let hPetoCalculada = 0;
    if (conPeto) {
        if (params.alturaPeto === 'auto' || !params.alturaPeto) {
            hPetoCalculada = Math.round((flechaCumbrera + 0.20) * 100) / 100;
            if (hPetoCalculada < 0.80) hPetoCalculada = 0.80;
        } else {
            hPetoCalculada = parseFloat(params.alturaPeto) || 1.0;
        }
    }
    const supPeto = conPeto ? (perimetroNave * hPetoCalculada) : 0;

    // Mediciones de muro y cerramiento superior
    const supMuro = (hMuro > 0 && tipoMuro !== 'ninguno') ? Math.min(supCerramientoTotal, perimetroNave * hMuro) : 0;
    const supMuroBloque = tipoMuro === 'bloque' ? Math.round(supMuro * 10) / 10 : 0;
    const supMuroAlveolar = tipoMuro === 'alveolar' ? Math.round(supMuro * 10) / 10 : 0;

    const supSuperiorBase = (tipoSuperior !== 'ninguno') ? Math.max(0, supCerramientoTotal - supMuro) : 0;
    const supSuperiorTotal = supSuperiorBase + supPeto;
    const supFachadaChapa = tipoSuperior === 'chapa' ? Math.round(supSuperiorTotal * 10) / 10 : (conPeto && tipoSuperior === 'ninguno' ? 0 : 0);
    const supFachadaPanel = (tipoSuperior === 'panel' || (conPeto && tipoSuperior === 'ninguno')) ? Math.round(supSuperiorTotal * 10) / 10 : 0;

    // Correas de cubierta y fachada
    const lineasCorreasCubiertaFaldon = Math.ceil(longitudFaldon / 1.50) + 1;
    const totalLineasCorreasCubierta = lineasCorreasCubiertaFaldon * 2;
    const mlCorreasCubierta = totalLineasCorreasCubierta * longitud;

    const hSuperior = Math.max(0, altura - hMuro) + (conPeto ? hPetoCalculada : 0);
    const lineasCorreasFachada = (tipoSuperior !== 'ninguno' && hSuperior > 0) ? Math.ceil(hSuperior / 1.60) : 0;
    const mlCorreasLaterales = 2 * lineasCorreasFachada * longitud;
    const lineasCorreasTestero = (tipoSuperior !== 'ninguno' && (hSuperior + flechaCumbrera / 2) > 0) ? Math.ceil((hSuperior + flechaCumbrera / 2) / 1.60) : 0;
    const mlCorreasTestero = 2 * lineasCorreasTestero * luz;

    // Remates y Canalones
    const mlCumbrera = longitud;
    const mlRemateHastiales = 4.0 * longitudFaldon;
    const mlRemateEsquinas = (tipoSuperior !== 'ninguno' && hSuperior > 0) ? 4.0 * hSuperior : 0;
    const mlVierteaguasZocalo = (hMuro > 0 && hMuro < altura && tipoSuperior !== 'ninguno') ? perimetroNave : 0;
    const mlRematePeto = conPeto ? perimetroNave : 0;

    const tipoCanalon = params.tipoCanalon || (conPeto ? 'interior' : 'exterior');
    const mlCanalon = (tipoCanalon !== 'sin') ? Math.round(2 * longitud * 10) / 10 : 0;

    // --- 2. Estimación de Acero Estructural ---
    // Ratio base kg/m2 según luz
    let ratioAceroKgM2 = 18.0;
    if (luz <= 12) ratioAceroKgM2 = 18.0;
    else if (luz <= 18) ratioAceroKgM2 = 22.0 + ((luz - 12) * 0.8);
    else if (luz <= 25) ratioAceroKgM2 = 27.0 + ((luz - 18) * 1.0);
    else if (luz <= 32) ratioAceroKgM2 = 34.0 + ((luz - 25) * 1.2);
    else ratioAceroKgM2 = 42.0;

    // Ajuste por altura (si altura > 6m)
    if (altura > 6.0) {
        ratioAceroKgM2 += (altura - 6.0) * 1.2;
    }
    // Ajuste por viento/zona
    ratioAceroKgM2 *= (0.95 + (sobrecargaViento * 0.05));

    const kgAceroTotal = Math.round(supConstruida * ratioAceroKgM2);
    const numTornillosTotal = Math.round(totalPorticos * 48 + (mlCorreasCubierta / 1.5) * 2);

    // --- 3. Cimentación y Solera ---
    const nPilaresTotales = totalPorticos * 2 + (luz > 15 ? 4 : 2); // Pilares hastiales extras
    const volZapataCentral = (luz <= 15 ? 1.60 * 1.60 * 0.70 : 2.00 * 2.00 * 0.80) * (1.5 / tensionAdmisible);
    const volZapataTestero = (luz <= 15 ? 1.30 * 1.30 * 0.60 : 1.60 * 1.60 * 0.70) * (1.5 / tensionAdmisible);

    const m3Zapatas = (nPorticosIntermedios * 2 * volZapataCentral) + (nPorticosTestero * 2 * volZapataTestero);
    const mlRiostras = (2 * longitud) + (totalPorticos * luz);
    const m3Riostras = mlRiostras * 0.40 * 0.50; // Sección 40x50 cm
    const m3HormigonCimen = Math.round((m3Zapatas + m3Riostras) * 10) / 10;
    const m3HormigonLimpieza = Math.round(((m3Zapatas / 0.75) * 0.10) * 10) / 10;
    const kgAceroCimentacion = Math.round(m3HormigonCimen * 40.0); // 40 kg/m3

    const m3Explanacion = Math.round(supConstruida * 0.25);
    const m3ExcavacionZapatas = Math.round((m3HormigonCimen + m3HormigonLimpieza) * 1.15);

    // Solera
    const espesorSoleraM = 0.15;
    const m3Solera = Math.round(supConstruida * espesorSoleraM * 10) / 10;
    const m3Zahorra = Math.round(supConstruida * 0.15 * 10) / 10;
    const m2LaminaPE = Math.round(supConstruida * 1.12);
    const m2Mallazo = Math.round(supConstruida * 1.15);

    // --- 4. Selección de Precios según Material ---
    let puCubierta = P.precio_chapa_cubierta_m2;
    let descCubierta = 'Chapa simple grecada 0.6 mm';
    if (tipoCubierta === 'panel30') { puCubierta = P.precio_panel_30_m2; descCubierta = 'Panel sándwich 30 mm'; }
    else if (tipoCubierta === 'panel40') { puCubierta = P.precio_panel_40_m2; descCubierta = 'Panel sándwich 40 mm'; }
    else if (tipoCubierta === 'panel50') { puCubierta = P.precio_panel_50_m2; descCubierta = 'Panel sándwich 50 mm'; }
    else if (tipoCubierta === 'panel60') { puCubierta = P.precio_panel_60_m2; descCubierta = 'Panel sándwich 60 mm'; }
    else if (tipoCubierta === 'panel70') { puCubierta = P.precio_panel_70_m2; descCubierta = 'Panel sándwich 70 mm'; }
    else if (tipoCubierta === 'panel80') { puCubierta = P.precio_panel_80_m2; descCubierta = 'Panel sándwich 80 mm'; }
    else if (tipoCubierta === 'panel90') { puCubierta = P.precio_panel_90_m2; descCubierta = 'Panel sándwich 90 mm'; }
    else if (tipoCubierta === 'panel100') { puCubierta = P.precio_panel_100_m2; descCubierta = 'Panel sándwich 100 mm'; }
    else if (tipoCubierta === 'pural') { puCubierta = P.precio_panel_pural_m2; descCubierta = 'Panel sándwich 30 mm + falso techo PURAL 30'; }
    else if (tipoCubierta === 'teja') { puCubierta = P.precio_panel_teja_m2; descCubierta = 'Panel sándwich 30 mm imitación teja'; }

    let puPanelFachada = P.precio_panel_35_m2;
    let descPanelFachada = `Panel sándwich ${espesorPanelFachada} mm`;
    if (espesorPanelFachada === 40) puPanelFachada = P.precio_panel_40_m2;
    else if (espesorPanelFachada === 50) puPanelFachada = P.precio_panel_50_m2;
    else if (espesorPanelFachada === 60) puPanelFachada = P.precio_panel_60_m2;
    else if (espesorPanelFachada === 70) puPanelFachada = P.precio_panel_70_m2;
    else if (espesorPanelFachada === 80) puPanelFachada = P.precio_panel_80_m2;
    else if (espesorPanelFachada === 90) puPanelFachada = P.precio_panel_90_m2;
    else if (espesorPanelFachada === 100) puPanelFachada = P.precio_panel_100_m2;

    // Cálculo logístico de transportes y montaje
    const viajesAcero = Math.max(1, Math.ceil(kgAceroTotal / 24000.0));
    const supPanelesTotal = supCubiertaOpaca + supFachadaChapa + supFachadaPanel;
    const viajesPaneles = supPanelesTotal > 0 ? Math.max(1, Math.ceil(supPanelesTotal / 600.0)) : 0;
    const viajesAlveolares = supMuroAlveolar > 0 ? Math.max(1, Math.ceil(supMuroAlveolar / 140.0)) : 0;
    const viajesTrailerTotal = viajesAcero + viajesPaneles + viajesAlveolares;
    const diasMontajeEstimados = Math.max(3, Math.ceil(supConstruida / 70.0));
    const mlRematesTotales = Math.round((mlCumbrera + mlRemateHastiales + mlRemateEsquinas + mlVierteaguasZocalo) * 10) / 10;

    // --- 5. Desglose Detallado de Partidas ---
    const partidas = [];

    // Cap 1: Estructura y Cerramientos (Suministro)
    if (kgAceroTotal > 0) {
        partidas.push({ cap: 1, cod: 'EST-01', desc: 'Perfiles de acero laminado soldado de vigas, pilares y correas S275JR', med: kgAceroTotal, ud: 'kg', pu: P.precio_acero_kg });
    }
    if (supCubiertaOpaca > 0) {
        partidas.push({ cap: 1, cod: 'CUB-01', desc: `Cubierta (${descCubierta})`, med: Math.round(supCubiertaOpaca * 10) / 10, ud: 'm²', pu: puCubierta });
    }
    if (pctLucernarios > 0 && supLucernarios > 0) {
        partidas.push({ cap: 1, cod: 'LUC-01', desc: `Lucernarios translúcidos de policarbonato / poliéster (${pctLucernarios}% cubierta)`, med: Math.round(supLucernarios * 10) / 10, ud: 'm²', pu: P.precio_lucernario_m2 });
    }
    if ((falsoTecho || tipoCubierta === 'pural') && supCubiertaReal > 0) {
        partidas.push({ cap: 1, cod: 'AIS-01', desc: 'Falso techo aislante tipo PURAL (lavable agropecuario)', med: Math.round(supCubiertaReal * 10) / 10, ud: 'm²', pu: P.precio_falso_techo_m2 });
    }
    if (supMuroBloque > 0) {
        partidas.push({ cap: 1, cod: 'CER-BLQ', desc: `Fábrica de bloque de hormigón / termoarcilla 20cm en cerramiento (zócalo h=${hMuro.toFixed(1)}m)`, med: supMuroBloque, ud: 'm²', pu: P.precio_bloque_hormigon_m2 });
    }
    if (supMuroAlveolar > 0) {
        partidas.push({ cap: 1, cod: 'CER-ALV', desc: `Placas alveolares de hormigón pretensado e=150mm machihembradas (zócalo h=${hMuro.toFixed(1)}m)`, med: supMuroAlveolar, ud: 'm²', pu: P.precio_placa_alveolar_m2 });
    }
    if (supFachadaChapa > 0) {
        partidas.push({ cap: 1, cod: 'CER-CHP', desc: `Cerramiento ${hMuro > 0 ? 'superior ' : ''}de fachadas y hastiales en chapa grecada 0.6 mm`, med: supFachadaChapa, ud: 'm²', pu: P.precio_chapa_cubierta_m2 });
    }
    if (supFachadaPanel > 0) {
        partidas.push({ cap: 1, cod: 'CER-PNL', desc: `Cerramiento ${hMuro > 0 ? 'superior ' : ''}de fachadas y hastiales en ${descPanelFachada}`, med: supFachadaPanel, ud: 'm²', pu: puPanelFachada });
    }
    if (mlVierteaguasZocalo > 0) {
        partidas.push({ cap: 1, cod: 'REM-VIE', desc: 'Remate vierteaguas / babero de chapa plegada sobre coronación de zócalo', med: Math.round(mlVierteaguasZocalo * 10) / 10, ud: 'ml', pu: P.precio_remate_vierteaguas_ml });
    }
    if (mlCumbrera > 0) {
        partidas.push({ cap: 1, cod: 'REM-01', desc: 'Remate del cumbrero con chapa prelacada plegada de 620 mm desarrollo', med: Math.round(mlCumbrera * 10) / 10, ud: 'ml', pu: P.precio_remate_cumbrera_ml });
    }
    if (mlRemateHastiales > 0) {
        partidas.push({ cap: 1, cod: 'REM-02', desc: 'Remate de cubierta con hastiales (goterón lateral)', med: Math.round(mlRemateHastiales * 10) / 10, ud: 'ml', pu: P.precio_remate_lateral_ml });
    }
    if (mlRemateEsquinas > 0) {
        partidas.push({ cap: 1, cod: 'REM-03', desc: 'Remate de esquinas de fachadas con cantonera plegada', med: Math.round(mlRemateEsquinas * 10) / 10, ud: 'ml', pu: P.precio_remate_esquina_ml });
    }
    if (conPeto && mlRematePeto > 0) {
        partidas.push({ cap: 1, cod: 'REM-PET', desc: `Albardilla vierteaguas de coronación de peto perimetral en chapa prelacada (h=${hPetoCalculada.toFixed(2)}m)`, med: Math.round(mlRematePeto * 10) / 10, ud: 'ml', pu: P.precio_remate_vierteaguas_ml });
        const acabadoInteriorPeto = params.acabadoInteriorPeto || 'chapa';
        const puIntPeto = acabadoInteriorPeto === 'panel' ? (P.precio_panel_30_m2 || 42.00) : (P.precio_chapa_cubierta_m2 || 22.00);
        const descIntPeto = acabadoInteriorPeto === 'panel' 
            ? `Forro interior de peto perimetral en panel sándwich aislante 30 mm (h=${hPetoCalculada.toFixed(2)}m)`
            : `Forro interior de peto perimetral en chapa prelacada grecada 0.6 mm (h=${hPetoCalculada.toFixed(2)}m)`;
        partidas.push({ cap: 1, cod: 'PET-INT', desc: descIntPeto, med: Math.round(supPeto * 10) / 10, ud: 'm²', pu: puIntPeto });
    }
    if (tipoCanalon === 'exterior' && mlCanalon > 0) {
        partidas.push({ cap: 1, cod: 'CAN-EXT', desc: 'Canalón exterior de chapa prelacada/aluminio en aleros laterales con bajantes pluviales hasta cota cero', med: mlCanalon, ud: 'ml', pu: P.precio_canalon_exterior_ml || 24.00 });
    } else if (tipoCanalon === 'interior' && mlCanalon > 0) {
        partidas.push({ cap: 1, cod: 'CAN-INT', desc: 'Canalón interior oculto estanco detrás de peto con embudos y bajantes pluviales', med: mlCanalon, ud: 'ml', pu: P.precio_canalon_interior_ml || 28.00 });
    }
    if (numPuertasGrandes > 0) {
        partidas.push({ cap: 1, cod: 'PUE-01', desc: 'Puerta principal para maquinaria/camiones abatible o corredera 5x5 m', med: numPuertasGrandes, ud: 'ud', pu: P.precio_puerta_grande_ud });
    }
    if (numPuertasPeatonales > 0) {
        partidas.push({ cap: 1, cod: 'PUE-02', desc: 'Puerta peatonal metálica con premarco y maneta 1x2.10 m', med: numPuertasPeatonales, ud: 'ud', pu: P.precio_puerta_peatonal_ud });
    }
    if (numTornillosTotal > 0) {
        partidas.push({ cap: 1, cod: 'TOR-01', desc: 'Tornillos y tuercas estructurales M12/M16 calidad 8.8 cincados', med: numTornillosTotal, ud: 'ud', pu: P.precio_tornillo_ud });
    }

    // Cap 2: Cimentación (Obra Civil)
    partidas.push(
        { cap: 2, cod: 'MOV-01', desc: 'Explanación y nivelación de la parcela con retroexcavadora', med: m3Explanacion, ud: 'm³', pu: P.precio_explanacion_m3 },
        { cap: 2, cod: 'MOV-02', desc: 'Excavación de pozos de zapatas y zanjas de riostras', med: m3ExcavacionZapatas, ud: 'm³', pu: P.precio_excavacion_m3 },
        { cap: 2, cod: 'CIM-01', desc: 'Hormigón de limpieza H10 de 10 cm de espesor en fondo de pozos', med: m3HormigonLimpieza, ud: 'm³', pu: P.precio_hormigon_limpieza_m3 },
        { cap: 2, cod: 'CIM-02', desc: 'Acero corrugado B500S en parrillas de zapatas y jaulas de riostras', med: kgAceroCimentacion, ud: 'kg', pu: P.precio_acero_corrugado_kg },
        { cap: 2, cod: 'CIM-03', desc: 'Placas de anclaje de pilares con pernos roscados y encamillado', med: nPilaresTotales, ud: 'ud', pu: P.precio_placa_anclaje_ud },
        { cap: 2, cod: 'CIM-04', desc: 'Hormigón para armar H25 vertido y vibrado en cimentación', med: m3HormigonCimen, ud: 'm³', pu: P.precio_hormigon_h25_cimen_m3 },

        // Cap 3: Solera Industrial
        { cap: 3, cod: 'SOL-01', desc: 'Encachado de zahorra artificial de regularización y reparto de cargas', med: m3Zahorra, ud: 'm³', pu: P.precio_zahorra_m3 },
        { cap: 3, cod: 'SOL-02', desc: 'Lámina impermeabilizante de polietileno PE 100 micras solapada', med: m2LaminaPE, ud: 'm²', pu: P.precio_lamina_pe_m2 },
        { cap: 3, cod: 'SOL-03', desc: 'Mallazo electrosoldado de acero corrugado B500T (#150x150x6 mm)', med: m2Mallazo, ud: 'm²', pu: P.precio_mallazo_m2 },
        { cap: 3, cod: 'SOL-04', desc: 'Hormigón H25 en solera extendido, fratasado mecánico y pulido', med: m3Solera, ud: 'm³', pu: P.precio_solera_h25_m3 }
    );

    // Cap 4: Montaje e Instalación Desglosada en Obra
    if (conMontaje) {
        if (kgAceroTotal > 0) {
            partidas.push({ cap: 4, cod: 'MON-01', desc: 'Montaje de estructura metálica principal y correas con autogrúa de izado', med: kgAceroTotal, ud: 'kg', pu: P.precio_montaje_acero_kg });
        }
        if (supCubiertaOpaca > 0) {
            partidas.push({ cap: 4, cod: 'MON-02', desc: 'Instalación y fijación estanca de cubierta con tornillería autotaladrante', med: Math.round(supCubiertaOpaca * 10) / 10, ud: 'm²', pu: P.precio_montaje_cubierta_m2 });
        }
        if (pctLucernarios > 0 && supLucernarios > 0) {
            partidas.push({ cap: 4, cod: 'MON-03', desc: 'Montaje de lucernarios translúcidos de policarbonato', med: Math.round(supLucernarios * 10) / 10, ud: 'm²', pu: P.precio_montaje_lucernarios_m2 });
        }
        if ((falsoTecho || tipoCubierta === 'pural') && supCubiertaReal > 0) {
            partidas.push({ cap: 4, cod: 'MON-04', desc: 'Montaje de falso techo aislante tipo PURAL', med: Math.round(supCubiertaReal * 10) / 10, ud: 'm²', pu: P.precio_montaje_falso_techo_m2 });
        }
        if (supMuroBloque > 0) {
            partidas.push({ cap: 4, cod: 'MON-BLQ', desc: 'Albañilería y ejecución de muro de bloque con mortero M-5 y tendeles armados', med: supMuroBloque, ud: 'm²', pu: P.precio_montaje_bloque_m2 });
        }
        if (supMuroAlveolar > 0) {
            partidas.push({ cap: 4, cod: 'MON-ALV', desc: 'Montaje y colocación de placas alveolares de hormigón con autogrúa de gran tonelaje', med: supMuroAlveolar, ud: 'm²', pu: P.precio_montaje_placa_alveolar_m2 });
        }
        if ((supFachadaChapa + supFachadaPanel) > 0) {
            partidas.push({ cap: 4, cod: 'MON-05', desc: 'Montaje, aplomado y fijación estanca de cerramientos de fachadas y hastiales', med: Math.round((supFachadaChapa + supFachadaPanel) * 10) / 10, ud: 'm²', pu: P.precio_montaje_fachada_m2 });
        }
        if (mlRematesTotales > 0) {
            partidas.push({ cap: 4, cod: 'MON-06', desc: 'Colocación, sellado y remachado de remates de cumbrera, goterones, zócalo y esquinas', med: mlRematesTotales, ud: 'ml', pu: P.precio_montaje_remates_ml });
        }
        if (tipoCanalon === 'exterior' && mlCanalon > 0) {
            partidas.push({ cap: 4, cod: 'MON-CANEXT', desc: 'Montaje, nivelación e instalación de canalón exterior lacado con bajantes pluviales hasta cota cero', med: mlCanalon, ud: 'ml', pu: P.precio_montaje_canalon_exterior_ml || 5.50 });
        } else if (tipoCanalon === 'interior' && mlCanalon > 0) {
            partidas.push({ cap: 4, cod: 'MON-CANINT', desc: 'Montaje, ajuste, embudos y sellado estanco de canalón interior oculto detrás de peto', med: mlCanalon, ud: 'ml', pu: P.precio_montaje_canalon_interior_ml || 7.50 });
        }
        if ((numPuertasGrandes + numPuertasPeatonales) > 0) {
            partidas.push({ cap: 4, cod: 'MON-07', desc: 'Montaje, ajuste y aplomado de puerta principal y peatonales', med: (numPuertasGrandes + numPuertasPeatonales), ud: 'ud', pu: P.precio_montaje_puerta_grande_ud });
        }
        if (diasMontajeEstimados > 0) {
            partidas.push({ cap: 4, cod: 'MON-08', desc: 'Alquiler de medios auxiliares (plataformas de tijera elevadora y camión grúa)', med: diasMontajeEstimados, ud: 'días', pu: P.precio_alquiler_medios_aux_dia });
        }
    }

    // Cap 5: Portes y Transportes a Obra (Logística en Menorca)
    if (viajesTrailerTotal > 0) {
        partidas.push({ cap: 5, cod: 'TRA-01', desc: `Transporte insular y descarga en obra en Menorca (${viajesAcero} viaje acero + ${viajesPaneles} cerramientos${viajesAlveolares > 0 ? ' + ' + viajesAlveolares + ' alveolar' : ''})`, med: viajesTrailerTotal, ud: 'viajes', pu: P.precio_porte_trailer_viaje });
    }

    // Cap 6: Proyecto Técnico y Cálculo Estructural
    if (P.precio_proyecto_tecnico > 0) {
        partidas.push({ cap: 6, cod: 'PRY-01', desc: 'Proyecto técnico de cálculo tridimensional de estructura y cimentación conforme a CTE DB-SE-AE, planos constructivos y visado colegial', med: 1, ud: 'ud', pu: P.precio_proyecto_tecnico });
    }

    // Filtrar partidas activas (excluir cualquier elemento cuya medición sea 0)
    const partidasActivas = partidas.filter(p => p.med > 0);

    // Asignar ID correlativo
    partidasActivas.forEach((p, idx) => { p.id = idx + 1; });

    // Exclusiones selectivas por partida / capítulo
    const excluidasSet = new Set(
        Array.isArray(params.partidasExcluidas) ? params.partidasExcluidas : 
        (params.partidasExcluidas ? Array.from(params.partidasExcluidas) : [])
    );

    // Cálculo de importes y totales por capítulo
    let totalCap1 = 0; // Estructura y cerramientos
    let totalCap2 = 0; // Cimentación
    let totalCap3 = 0; // Solera
    let totalCap4 = 0; // Montaje
    let totalCap5 = 0; // Portes y transportes
    let totalCap6 = 0; // Proyecto técnico de cálculo

    let baseCap1 = 0;
    let baseCap2 = 0;
    let baseCap3 = 0;
    let baseCap4 = 0;
    let baseCap5 = 0;
    let baseCap6 = 0;

    let totalPartidasIncluidas = 0;

    partidasActivas.forEach(p => {
        p.importe = Math.round(p.med * p.pu * 100) / 100;
        p.incluida = !excluidasSet.has(p.cod);
        p.importeEfectivo = p.incluida ? p.importe : 0;

        if (p.incluida) totalPartidasIncluidas++;

        if (p.cap === 1) {
            baseCap1 += p.importe;
            totalCap1 += p.importeEfectivo;
        } else if (p.cap === 2) {
            baseCap2 += p.importe;
            totalCap2 += p.importeEfectivo;
        } else if (p.cap === 3) {
            baseCap3 += p.importe;
            totalCap3 += p.importeEfectivo;
        } else if (p.cap === 4) {
            baseCap4 += p.importe;
            totalCap4 += p.importeEfectivo;
        } else if (p.cap === 5) {
            baseCap5 += p.importe;
            totalCap5 += p.importeEfectivo;
        } else if (p.cap === 6) {
            baseCap6 += p.importe;
            totalCap6 += p.importeEfectivo;
        }
    });

    const totalSinIva = totalCap1 + totalCap2 + totalCap3 + totalCap4 + totalCap5 + totalCap6;
    const totalBaseSinIva = baseCap1 + baseCap2 + baseCap3 + baseCap4 + baseCap5 + baseCap6;
    const ratioTotalM2 = Math.round((totalSinIva / supConstruida) * 100) / 100;
    const ratioEstructuraCerramientoM2 = Math.round((totalCap1 / supConstruida) * 100) / 100;
    const ratioCimentacionSoleraM2 = Math.round(((totalCap2 + totalCap3) / supConstruida) * 100) / 100;
    const ratioMontajeM2 = Math.round((totalCap4 / supConstruida) * 100) / 100;
    const ratioPortesM2 = Math.round((totalCap5 / supConstruida) * 100) / 100;
    const ratioProyectoM2 = Math.round((totalCap6 / supConstruida) * 100) / 100;

    return {
        dimensiones: {
            luz,
            longitud,
            altura,
            pendiente,
            flechaCumbrera: Math.round(flechaCumbrera * 100) / 100,
            alturaCumbrera: Math.round(alturaCumbrera * 100) / 100,
            longitudFaldon: Math.round(longitudFaldon * 100) / 100,
            supConstruida,
            volumenUtil: Math.round(supConstruida * (altura + flechaCumbrera / 2.0)),
            nVanos,
            intereje: Math.round(intereje * 100) / 100,
            nPorticosTestero,
            nPorticosIntermedios,
            totalPorticos,
            nPilaresTotales,
            kgAceroTotal,
            ratioAceroKgM2: Math.round(ratioAceroKgM2 * 10) / 10,
            hMuro,
            tipoMuro,
            tipoSuperior,
            supMuro,
            supSuperior: supSuperiorTotal,
            conPeto,
            hPeto: Math.round(hPetoCalculada * 100) / 100,
            supPeto: Math.round(supPeto * 10) / 10,
            acabadoInteriorPeto: params.acabadoInteriorPeto || 'chapa',
            tipoCanalon,
            mlCanalon,
            descCubierta
        },
        partidas: partidasActivas,
        totales: {
            cap1_estructura_cerramientos: Math.round(totalCap1 * 100) / 100,
            cap2_cimentacion: Math.round(totalCap2 * 100) / 100,
            cap3_solera: Math.round(totalCap3 * 100) / 100,
            cap4_montaje: Math.round(totalCap4 * 100) / 100,
            cap5_portes: Math.round(totalCap5 * 100) / 100,
            cap6_proyecto: Math.round(totalCap6 * 100) / 100,
            base_cap1: Math.round(baseCap1 * 100) / 100,
            base_cap2: Math.round(baseCap2 * 100) / 100,
            base_cap3: Math.round(baseCap3 * 100) / 100,
            base_cap4: Math.round(baseCap4 * 100) / 100,
            base_cap5: Math.round(baseCap5 * 100) / 100,
            base_cap6: Math.round(baseCap6 * 100) / 100,
            totalBaseSinIva: Math.round(totalBaseSinIva * 100) / 100,
            totalSinIva: Math.round(totalSinIva * 100) / 100,
            iva21: Math.round(totalSinIva * 0.21 * 100) / 100,
            totalConIva: Math.round(totalSinIva * 1.21 * 100) / 100,
            totalPartidasIncluidas,
            totalPartidasTotales: partidasActivas.length,
            ratioTotalM2,
            ratioEstructuraCerramientoM2,
            ratioCimentacionSoleraM2,
            ratioMontajeM2,
            ratioPortesM2,
            ratioProyectoM2
        }
    };
}

// --- DNI / NIE / CIF & Email Validation Algorithms ---
function validarDniCifNie(value) {
    if (!value) return false;
    const str = value.toString().trim().toUpperCase().replace(/[\s\-]/g, '');
    if (str.length < 8 || str.length > 9) return false;

    const dniRegex = /^(\d{8})([A-Z])$/;
    const nieRegex = /^([XYZ])(\d{7})([A-Z])$/;
    const cifRegex = /^([ABCDEFGHJNPQRSUVW])(\d{7})([A-J0-9])$/;
    const letrasDni = 'TRWAGMYFPDXBNJZSQVHLCKE';

    if (dniRegex.test(str)) {
        const match = str.match(dniRegex);
        const num = parseInt(match[1], 10);
        return letrasDni.charAt(num % 23) === match[2];
    }
    if (nieRegex.test(str)) {
        const match = str.match(nieRegex);
        const prefixNum = match[1] === 'X' ? '0' : (match[1] === 'Y' ? '1' : '2');
        const fullNum = parseInt(prefixNum + match[2], 10);
        return letrasDni.charAt(fullNum % 23) === match[3];
    }
    if (cifRegex.test(str)) {
        const match = str.match(cifRegex);
        const letter = match[1];
        const digits = match[2];
        const control = match[3];

        let sumaPar = 0;
        let sumaImpar = 0;
        for (let i = 0; i < digits.length; i++) {
            const n = parseInt(digits.charAt(i), 10);
            if (i % 2 === 1) sumaPar += n;
            else {
                const double = n * 2;
                sumaImpar += (double > 9 ? double - 9 : double);
            }
        }
        const sumaTotal = sumaPar + sumaImpar;
        const unidad = sumaTotal % 10;
        const digitoControl = unidad === 0 ? 0 : 10 - unidad;
        const letrasControl = 'JABCDEFGHI';

        const controlNum = digitoControl.toString();
        const controlLetra = letrasControl.charAt(digitoControl);

        if ('PQRSNW'.indexOf(letter) !== -1) return control === controlLetra;
        if ('ABEH'.indexOf(letter) !== -1) return control === controlNum;
        return control === controlNum || control === controlLetra;
    }
    return false;
}

function validarEmail(email) {
    if (!email) return false;
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

async function cargarPreciosServidor() {
    try {
        const res = await fetch('/naves/api/precios');
        if (res.ok) {
            const data = await res.json();
            if (data && typeof data === 'object' && !data.status) {
                return data;
            }
        }
    } catch (e) {
        console.warn('No se pudo conectar con el API de precios, usando local/defecto:', e);
    }
    return null;
}

async function guardarPreciosServidor(adminUser, adminPass, preciosObj) {
    const res = await fetch('/naves/api/precios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user: adminUser,
            password: adminPass,
            precios: preciosObj
        })
    });
    return await res.json();
}

async function enviarSolicitudPresupuesto(solicitudData) {
    const res = await fetch('/naves/api/solicitud', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(solicitudData)
    });
    return await res.json();
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { calcularPresupuestoNave, PRECIOS_DEFECTO, validarDniCifNie, validarEmail };
}

