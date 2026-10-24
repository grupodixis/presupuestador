const http = require('http');
const fs = require('fs');
const path = require('path');
const nodemailer = require('nodemailer');

const PORT = 3006;
const PRECIOS_FILE = path.join(__dirname, 'precios_guardados.json');
const SOLICITUDES_FILE = path.join(__dirname, 'solicitudes_presupuesto.json');

// Nodemailer SMTP Transporter (IONOS Mail)
const transporter = nodemailer.createTransport({
    host: 'smtp.ionos.es',
    port: 587,
    secure: false, // STARTTLS
    auth: {
        user: process.env.SMTP_USER || 'info@dixisweb.com',
        pass: process.env.SMTP_PASS || ''
    }
});

// DNI/CIF/NIE Validation Helper
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

function setCors(res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
}

async function enviarEmailsSolicitud(solicitud) {
    const { id, nombre, cif, email, telefono, municipio, naveConfig } = solicitud;
    const dim = (naveConfig && naveConfig.dimensiones) || {};
    const tot = (naveConfig && naveConfig.totales) || {};

    const htmlCliente = `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; background: #ffffff;">
        <div style="background-color: #0f172a; padding: 24px; text-align: center;">
            <h1 style="color: #38bdf8; margin: 0; font-size: 22px; font-weight: 800;">HAM ESTRUCTURAS Y COBERTURAS</h1>
            <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 13px;">Confirmación de Solicitud de Presupuesto Formal</p>
        </div>
        <div style="padding: 24px; color: #334155; line-height: 1.6;">
            <h2 style="color: #1e293b; font-size: 18px; margin-top: 0;">Estimado/a ${nombre},</h2>
            <p>Hemos recibido correctamente tu solicitud de presupuesto para el suministro y montaje de nave industrial en <strong>${municipio} (Menorca)</strong>.</p>
            
            <div style="background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 16px; margin: 20px 0; border-radius: 4px;">
                <p style="margin: 0 0 8px 0; font-weight: bold; color: #0369a1;">Nº de Referencia: ${id}</p>
                <p style="margin: 0; font-size: 14px;"><strong>Cliente / Empresa:</strong> ${nombre} (${cif})</p>
                <p style="margin: 4px 0 0 0; font-size: 14px;"><strong>Contacto:</strong> ${email} | Tel: ${telefono || 'No indicado'}</p>
            </div>

            <h3 style="color: #0f172a; font-size: 15px; border-bottom: 2px solid #f1f5f9; padding-bottom: 6px;">Resumen de la Nave Configurada:</h3>
            <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 16px;">
                <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px 0; color: #64748b;">Dimensiones Principales:</td><td style="padding: 6px 0; font-weight: bold; text-align: right;">${dim.luz || '-'}m (Luz) x ${dim.longitud || '-'}m (Longitud) x ${dim.altura || '-'}m (Altura)</td></tr>
                <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px 0; color: #64748b;">Superficie Construida:</td><td style="padding: 6px 0; font-weight: bold; text-align: right;">${dim.supConstruida || '-'} m²</td></tr>
                <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px 0; color: #64748b;">Pendiente Cubierta:</td><td style="padding: 6px 0; font-weight: bold; text-align: right;">${dim.pendiente || '-'}%</td></tr>
                <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px 0; color: #64748b;">Peso Estructura de Acero:</td><td style="padding: 6px 0; font-weight: bold; text-align: right;">${(dim.kgAceroTotal || 0).toLocaleString('es-ES')} kg (${dim.ratioAceroKgM2 || 0} kg/m²)</td></tr>
                <tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 6px 0; color: #64748b;">Presupuesto Estimado Sin IVA:</td><td style="padding: 6px 0; font-weight: bold; text-align: right; color: #0284c7; font-size: 15px;">${(tot.totalSinIva || 0).toLocaleString('es-ES')} €</td></tr>
                <tr><td style="padding: 6px 0; color: #64748b;">Total Estimado Con IVA (21%):</td><td style="padding: 6px 0; font-weight: bold; text-align: right; color: #16a34a; font-size: 15px;">${(tot.totalConIva || 0).toLocaleString('es-ES')} €</td></tr>
            </table>

            <p style="font-size: 13px; color: #475569;">Un técnico o comercial de <strong>HAM Estructuras Menorca</strong> revisará los datos de carga según el CTE DB-SE-AE para la zona de Tramuntana y se pondrá en contacto contigo a la brevedad.</p>
        </div>
        <div style="background-color: #f1f5f9; padding: 16px; text-align: center; font-size: 12px; color: #64748b;">
            <p style="margin: 0;">HAM Estructuras y Coberturas S.L. · Menorca, Islas Baleares</p>
        </div>
    </div>
    `;

    const htmlAdmin = `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; background: #ffffff;">
        <div style="background-color: #0284c7; padding: 20px; text-align: center;">
            <h1 style="color: #ffffff; margin: 0; font-size: 20px;">🚨 NUEVA SOLICITUD DE PRESUPUESTO</h1>
            <p style="color: #e0f2fe; margin: 4px 0 0 0; font-size: 13px;">Ref: ${id}</p>
        </div>
        <div style="padding: 24px; color: #334155; font-size: 14px; line-height: 1.6;">
            <p>Se ha recibido una nueva solicitud de presupuesto desde el presupuestador web:</p>
            <ul>
                <li><strong>Empresa / Cliente:</strong> ${nombre}</li>
                <li><strong>CIF / NIF / DNI:</strong> ${cif}</li>
                <li><strong>Email:</strong> ${email}</li>
                <li><strong>Teléfono:</strong> ${telefono || 'No facilitado'}</li>
                <li><strong>Municipio Obra:</strong> ${municipio}</li>
                <li><strong>Dimensiones:</strong> ${dim.luz || '-'}x${dim.longitud || '-'}x${dim.altura || '-'}m (${dim.supConstruida || '-'} m²)</li>
                <li><strong>Importe Estimado Sin IVA:</strong> ${(tot.totalSinIva || 0).toLocaleString('es-ES')} €</li>
                <li><strong>Importe Con IVA:</strong> ${(tot.totalConIva || 0).toLocaleString('es-ES')} €</li>
            </ul>
        </div>
    </div>
    `;

    // Send to Client
    await transporter.sendMail({
        from: '"HAM Estructuras" <info@dixisweb.com>',
        to: email,
        subject: `Presupuesto de Nave Industrial - HAM Estructuras (Ref: ${id})`,
        html: htmlCliente
    });

    // Send to Admin Team
    await transporter.sendMail({
        from: '"HAM Presupuestador API" <info@dixisweb.com>',
        to: 'grupodixis@gmail.com, pablo@dixis.es, info@dixisweb.com',
        subject: `🚨 NUEVA SOLICITUD: ${nombre} (${cif}) - Nave ${dim.luz || '-'}x${dim.longitud || '-'}m`,
        html: htmlAdmin
    });
}

const server = http.createServer((req, res) => {
    setCors(res);
    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    const urlPath = req.url.split('?')[0];

    // GET /naves/api/precios
    if (req.method === 'GET' && (urlPath === '/naves/api/precios' || urlPath === '/api/precios')) {
        if (fs.existsSync(PRECIOS_FILE)) {
            try {
                const data = fs.readFileSync(PRECIOS_FILE, 'utf8');
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(data);
                return;
            } catch (err) {
                console.error('Error al leer precios:', err);
            }
        }
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'default', precios: null }));
        return;
    }

    // POST /naves/api/precios (Save admin prices)
    if (req.method === 'POST' && (urlPath === '/naves/api/precios' || urlPath === '/api/precios')) {
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', () => {
            try {
                const payload = JSON.parse(body);
                const { user, password, precios } = payload;
                if (user !== 'admin' || password !== 'admin') {
                    res.writeHead(401, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ status: 'error', message: 'Credenciales inválidas (admin/admin)' }));
                    return;
                }

                fs.writeFileSync(PRECIOS_FILE, JSON.stringify(precios, null, 2), 'utf8');
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'success', message: 'Precios guardados correctamente en el servidor' }));
            } catch (err) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'error', message: err.message }));
            }
        });
        return;
    }

    // POST /naves/api/solicitud (Save client budget request lead & send email)
    if (req.method === 'POST' && (urlPath === '/naves/api/solicitud' || urlPath === '/api/solicitud')) {
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', async () => {
            try {
                const lead = JSON.parse(body);
                const { nombre, cif, email, telefono, municipio, naveConfig } = lead;

                if (!nombre || !nombre.trim()) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ status: 'error', message: 'El nombre / razón social es obligatorio' }));
                    return;
                }
                if (!validarDniCifNie(cif)) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ status: 'error', message: 'El DNI / NIF / CIF introducido no es válido' }));
                    return;
                }
                if (!validarEmail(email)) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ status: 'error', message: 'El correo electrónico introducido no es válido' }));
                    return;
                }

                let solicitudes = [];
                if (fs.existsSync(SOLICITUDES_FILE)) {
                    try {
                        solicitudes = JSON.parse(fs.readFileSync(SOLICITUDES_FILE, 'utf8'));
                    } catch (e) {}
                }

                const nuevaSolicitud = {
                    id: 'SOL-' + Date.now(),
                    fecha: new Date().toISOString(),
                    nombre: nombre.trim(),
                    cif: cif.trim().toUpperCase(),
                    email: email.trim().toLowerCase(),
                    telefono: (telefono || '').trim(),
                    municipio: municipio || 'Menorca',
                    naveConfig: naveConfig || {},
                };

                solicitudes.push(nuevaSolicitud);
                fs.writeFileSync(SOLICITUDES_FILE, JSON.stringify(solicitudes, null, 2), 'utf8');

                // Enviar correos electrónicos
                let emailEnviado = false;
                try {
                    await enviarEmailsSolicitud(nuevaSolicitud);
                    emailEnviado = true;
                    console.log(`[EMAIL SUCCESS] Correos enviados para solicitud ${nuevaSolicitud.id}`);
                } catch (emailErr) {
                    console.error(`[EMAIL ERROR] Error enviando correo para solicitud ${nuevaSolicitud.id}:`, emailErr);
                }

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    status: 'success',
                    message: emailEnviado ? 'Solicitud registrada y presupuesto enviado a tu correo electrónico' : 'Solicitud registrada correctamente',
                    id: nuevaSolicitud.id,
                    emailEnviado
                }));
            } catch (err) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'error', message: err.message }));
            }
        });
        return;
    }

    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'error', message: 'Ruta no encontrada' }));
});

server.listen(PORT, () => {
    console.log(`Servidor API Presupuestador Naves escuchando en http://127.0.0.1:${PORT}`);
});
