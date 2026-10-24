/**
 * provincias.js
 * Ámbito Geográfico Exclusivo: Isla de Menorca (Illes Balears)
 * Normativa CTE DB-SE-AE: Toda la isla de Menorca se encuentra en la Zona Eólica C (vb = 29 m/s)
 * Especialmente condicionada por vientos de Tramuntana y ambiente salino litoral.
 */

const MUNICIPIOS_MENORCA = [
    { id: 1, nombre: "Maó (Mahón)", zonaViento: "C", altitudMedia: 45, descripcion: "Puerto y Polígono Industrial" },
    { id: 2, nombre: "Ciutadella de Menorca", zonaViento: "C", altitudMedia: 25, descripcion: "Poniente y Polígono Industrial" },
    { id: 3, nombre: "Alaior", zonaViento: "C", altitudMedia: 130, descripcion: "Centro y Polígono Alaior" },
    { id: 4, nombre: "Es Mercadal", zonaViento: "C", altitudMedia: 70, descripcion: "Centro - Faldas Monte Toro" },
    { id: 5, nombre: "Ferreries", zonaViento: "C", altitudMedia: 140, descripcion: "Centro-Oeste" },
    { id: 6, nombre: "Es Castell", zonaViento: "C", altitudMedia: 32, descripcion: "Levante" },
    { id: 7, nombre: "Sant Lluís", zonaViento: "C", altitudMedia: 60, descripcion: "Polígono Industrial Sant Lluís (Taller HAM)" },
    { id: 8, nombre: "Es Migjorn Gran", zonaViento: "C", altitudMedia: 115, descripcion: "Sur" }
];

// Alias para mantener compatibilidad con el motor
const PROVINCIAS_ESPANA = MUNICIPIOS_MENORCA;

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MUNICIPIOS_MENORCA, PROVINCIAS_ESPANA };
}
