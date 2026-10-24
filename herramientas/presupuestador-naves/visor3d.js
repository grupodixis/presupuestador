/**
 * visor3d.js
 * Visualizador 3D interactivo para naves industriales y agrícolas con Three.js.
 * Genera paramétricamente en tiempo real la geometría de pórticos, correas, cerramientos y puertas.
 */

class VisorNave3D {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;

        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.naveGroup = new THREE.Group();
        this.grupoPersonas = new THREE.Group();
        this.grupoVehiculos = new THREE.Group();

        this.verEstructura = true;
        this.verCerramientos = true;
        this.verCubierta = true;
        this.verPersonas = true;
        this.verVehiculos = true;
        this.autoRotar = false;

        this.init();
    }

    init() {
        const width = this.container.clientWidth || 600;
        const height = this.container.clientHeight || 450;

        // Escena
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xf0f4f8);
        this.scene.fog = new THREE.FogExp2(0xf0f4f8, 0.007);

        // Cámara
        this.camera = new THREE.PerspectiveCamera(45, width / height, 0.5, 1000);
        this.camera.position.set(35, 25, 45);

        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(width, height);
        this.renderer.setPixelRatio(window.devicePixelRatio || 1);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);

        // Controles de órbita
        if (typeof THREE.OrbitControls !== 'undefined') {
            this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
            this.controls.enableDamping = true;
            this.controls.dampingFactor = 0.05;
            this.controls.maxPolarAngle = Math.PI / 2 - 0.02; // No descender bajo el suelo
            this.controls.minDistance = 5;
            this.controls.maxDistance = 250;
        }

        // Luces
        this.setupLights();

        // Suelo y cuadrícula
        this.setupGround();

        // Grupos en la escena
        this.scene.add(this.naveGroup);
        this.scene.add(this.grupoPersonas);
        this.scene.add(this.grupoVehiculos);

        // Eventos
        window.addEventListener('resize', () => this.onWindowResize());

        // Bucle de animación
        this.animate();
    }

    setupLights() {
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.65);
        this.scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xfff8eb, 0.85);
        dirLight.position.set(45, 60, 35);
        dirLight.castShadow = true;
        dirLight.shadow.mapSize.width = 2048;
        dirLight.shadow.mapSize.height = 2048;
        dirLight.shadow.camera.near = 10;
        dirLight.shadow.camera.far = 200;
        const d = 50;
        dirLight.shadow.camera.left = -d;
        dirLight.shadow.camera.right = d;
        dirLight.shadow.camera.top = d;
        dirLight.shadow.camera.bottom = -d;
        this.scene.add(dirLight);

        const fillLight = new THREE.DirectionalLight(0xd4e4f7, 0.35);
        fillLight.position.set(-40, 30, -30);
        this.scene.add(fillLight);
    }

    setupGround() {
        // Suelo receptor de sombras
        const groundGeo = new THREE.PlaneGeometry(300, 300);
        const groundMat = new THREE.MeshStandardMaterial({
            color: 0xe2e8f0,
            roughness: 0.85,
            metalness: 0.1
        });
        const ground = new THREE.Mesh(groundGeo, groundMat);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -0.05;
        ground.receiveShadow = true;
        this.scene.add(ground);

        // Grid
        const gridHelper = new THREE.GridHelper(200, 40, 0x94a3b8, 0xcbd5e1);
        gridHelper.position.y = 0;
        this.scene.add(gridHelper);
    }

    actualizarNave(params) {
        // Limpiar nave anterior
        while (this.naveGroup.children.length > 0) {
            const obj = this.naveGroup.children[0];
            this.naveGroup.remove(obj);
        }

        const luz = parseFloat(params.luz) || 15;
        const longitud = parseFloat(params.longitud) || 30;
        const altura = parseFloat(params.altura) || 6;
        const pendiente = (parseFloat(params.pendiente) || 15) / 100.0;
        const flecha = (luz / 2.0) * pendiente;
        const hCumbrera = altura + flecha;
        const nVanos = Math.max(2, Math.round(longitud / 6.0));
        const intereje = longitud / nVanos;

        // Materiales 3D
        const matAcero = new THREE.MeshStandardMaterial({
            color: 0x2b4c6f, // Azul acero industrial
            roughness: 0.4,
            metalness: 0.7
        });

        const matCorreas = new THREE.MeshStandardMaterial({
            color: 0xa0aec0, // Galvanizado claro
            roughness: 0.5,
            metalness: 0.6
        });

        const matSolera = new THREE.MeshStandardMaterial({
            color: 0x9ca3af,
            roughness: 0.7,
            metalness: 0.1
        });

        const tipoCubierta = params.tipoCubierta || 'panel30';
        const tipoFachada = params.tipoFachada || 'panel35';

        // Color de cubierta dinámico según material
        let colorCubierta = 0x334155; // Antracita por defecto (panel sándwich)
        if (tipoCubierta === 'teja') {
            colorCubierta = 0xb44a2d; // Rojo teja envejecida / terracota
        } else if (tipoCubierta === 'chapa') {
            colorCubierta = 0x64748b; // Chapa grecada galvanizada
        } else if (tipoCubierta === 'pural') {
            colorCubierta = 0x475569;
        }

        const matCubierta = new THREE.MeshStandardMaterial({
            color: colorCubierta,
            roughness: tipoCubierta === 'teja' ? 0.75 : 0.5,
            metalness: tipoCubierta === 'teja' ? 0.05 : 0.25,
            side: THREE.DoubleSide,
            transparent: true,
            opacity: this.verCubierta ? 0.92 : 0.0
        });

        const matLucernario = new THREE.MeshStandardMaterial({
            color: 0xbae6fd,
            roughness: 0.1,
            metalness: 0.1,
            transparent: true,
            opacity: 0.6,
            side: THREE.DoubleSide
        });

        // Configuración de materiales para cerramientos y zócalos
        const esMuroAlveolar = tipoFachada.includes('alveolar');
        const esMuroBloque = tipoFachada.includes('bloque');
        const esChapaSuperior = tipoFachada.includes('chapa') || tipoFachada === 'chapa';

        // Material para zócalo o muro de hormigón
        const matMuro = new THREE.MeshStandardMaterial({
            color: esMuroAlveolar ? 0xcbd5e1 : 0x94a3b8, // Alveolar liso o Bloque visto
            roughness: 0.9,
            metalness: 0.05,
            side: THREE.DoubleSide,
            transparent: true,
            opacity: this.verCerramientos ? 0.95 : 0.0
        });

        // Material para cerramiento superior (panel o chapa)
        const matFachada = new THREE.MeshStandardMaterial({
            color: esChapaSuperior ? 0x94a3b8 : 0xf1f5f9, // Chapa grecada o Blanco Pirineo panel
            roughness: esChapaSuperior ? 0.45 : 0.6,
            metalness: esChapaSuperior ? 0.4 : 0.15,
            side: THREE.DoubleSide,
            transparent: true,
            opacity: this.verCerramientos ? 0.90 : 0.0
        });

        const matVierteaguas = new THREE.MeshStandardMaterial({
            color: 0x1e293b,
            roughness: 0.4,
            metalness: 0.6
        });

        const matPuerta = new THREE.MeshStandardMaterial({
            color: 0xd97706, // Ámbar / naranja señalización industrial
            roughness: 0.4,
            metalness: 0.4
        });

        // 1. Solera de hormigón
        const soleraGeo = new THREE.BoxGeometry(luz, 0.15, longitud);
        const solera = new THREE.Mesh(soleraGeo, matSolera);
        solera.position.set(0, 0.075, 0);
        solera.receiveShadow = true;
        this.naveGroup.add(solera);

        // 2. Pórticos (Pilares + Dinteles)
        const perfilAncho = 0.25;
        const perfilFondo = 0.16;

        for (let i = 0; i <= nVanos; i++) {
            const z = -longitud / 2 + (i * intereje);
            const esTestero = (i === 0 || i === nVanos);

            if (this.verEstructura) {
                // Pilar Izquierdo
                const pilarIzq = new THREE.Mesh(new THREE.BoxGeometry(perfilAncho, altura, perfilFondo), matAcero);
                pilarIzq.position.set(-luz / 2 + perfilAncho / 2, altura / 2, z);
                pilarIzq.castShadow = true;
                pilarIzq.receiveShadow = true;
                this.naveGroup.add(pilarIzq);

                // Pilar Derecho
                const pilarDer = new THREE.Mesh(new THREE.BoxGeometry(perfilAncho, altura, perfilFondo), matAcero);
                pilarDer.position.set(luz / 2 - perfilAncho / 2, altura / 2, z);
                pilarDer.castShadow = true;
                pilarDer.receiveShadow = true;
                this.naveGroup.add(pilarDer);

                // Dintel Izquierdo
                const longFaldon = Math.sqrt(Math.pow(luz / 2, 2) + Math.pow(flecha, 2));
                const angulo = Math.atan2(flecha, luz / 2);

                const dintelIzq = new THREE.Mesh(new THREE.BoxGeometry(longFaldon, perfilAncho, perfilFondo), matAcero);
                dintelIzq.position.set(-luz / 4, altura + flecha / 2, z);
                dintelIzq.rotation.z = angulo;
                dintelIzq.castShadow = true;
                this.naveGroup.add(dintelIzq);

                // Dintel Derecho
                const dintelDer = new THREE.Mesh(new THREE.BoxGeometry(longFaldon, perfilAncho, perfilFondo), matAcero);
                dintelDer.position.set(luz / 4, altura + flecha / 2, z);
                dintelDer.rotation.z = -angulo;
                dintelDer.castShadow = true;
                this.naveGroup.add(dintelDer);

                // Si es testero, añadir pilares hastiales intermedios
                if (esTestero && luz >= 12) {
                    const nPilaresHastial = Math.floor(luz / 6);
                    const pasoX = luz / (nPilaresHastial + 1);
                    for (let p = 1; p <= nPilaresHastial; p++) {
                        const px = -luz / 2 + p * pasoX;
                        const distCentro = Math.abs(px);
                        const altHastial = altura + ((luz / 2 - distCentro) * pendiente);
                        const pilarHastial = new THREE.Mesh(new THREE.BoxGeometry(0.20, altHastial, 0.15), matAcero);
                        pilarHastial.position.set(px, altHastial / 2, z);
                        pilarHastial.castShadow = true;
                        this.naveGroup.add(pilarHastial);
                    }
                }
            }
        }

        // 3. Correas longitudinales
        if (this.verEstructura) {
            const longFaldon = Math.sqrt(Math.pow(luz / 2, 2) + Math.pow(flecha, 2));
            const nLineasFaldon = Math.ceil(longFaldon / 1.50) + 1;

            for (let f = 0; f < nLineasFaldon; f++) {
                const frac = f / (nLineasFaldon - 1);
                // Faldón izquierdo
                const xIzq = -luz / 2 + frac * (luz / 2);
                const yIzq = altura + frac * flecha + 0.12;
                const correaIzq = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.12, longitud), matCorreas);
                correaIzq.position.set(xIzq, yIzq, 0);
                this.naveGroup.add(correaIzq);

                // Faldón derecho
                const xDer = luz / 2 - frac * (luz / 2);
                const yDer = altura + frac * flecha + 0.12;
                const correaDer = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.12, longitud), matCorreas);
                correaDer.position.set(xDer, yDer, 0);
                this.naveGroup.add(correaDer);
            }
        }

        // 4. Cubiertas (Placas a dos aguas con espesor real)
        if (this.verCubierta) {
            const longFaldon = Math.sqrt(Math.pow(luz / 2, 2) + Math.pow(flecha, 2));
            const angulo = Math.atan2(flecha, luz / 2);
            const espesorPanel = 0.06; // 60 mm de espesor de panel

            // Faldón izquierdo (sube desde el alero x = -luz/2 hacia la cumbrera x = 0)
            const geoFaldonIzq = new THREE.BoxGeometry(longFaldon + 0.25, espesorPanel, longitud + 0.3);
            const cubiertaIzq = new THREE.Mesh(geoFaldonIzq, matCubierta);
            cubiertaIzq.position.set(-luz / 4, altura + flecha / 2 + 0.16, 0);
            cubiertaIzq.rotation.z = angulo;
            cubiertaIzq.castShadow = true;
            cubiertaIzq.receiveShadow = true;
            this.naveGroup.add(cubiertaIzq);

            // Faldón derecho (baja desde la cumbrera x = 0 hacia el alero x = luz/2)
            const geoFaldonDer = new THREE.BoxGeometry(longFaldon + 0.25, espesorPanel, longitud + 0.3);
            const cubiertaDer = new THREE.Mesh(geoFaldonDer, matCubierta);
            cubiertaDer.position.set(luz / 4, altura + flecha / 2 + 0.16, 0);
            cubiertaDer.rotation.z = -angulo;
            cubiertaDer.castShadow = true;
            cubiertaDer.receiveShadow = true;
            this.naveGroup.add(cubiertaDer);

            // Remate de Cumbrera (caballete en el vértice superior)
            const cumbreraGeo = new THREE.BoxGeometry(0.35, 0.08, longitud + 0.35);
            const matCumbrera = new THREE.MeshStandardMaterial({
                color: 0x1e293b,
                roughness: 0.4,
                metalness: 0.5
            });
            const cumbreraMesh = new THREE.Mesh(cumbreraGeo, matCumbrera);
            cumbreraMesh.position.set(0, hCumbrera + 0.20, 0);
            this.naveGroup.add(cumbreraMesh);
        }

        // 5. Cerramientos de Fachada (Zócalos de hormigón + paneles/chapas superiores)
        const esNada = tipoFachada === 'nada';
        if (this.verCerramientos && !esNada) {
            // Calcular altura de muro inferior (zócalo o total)
            let hMuro = 0;
            if (tipoFachada === 'bloque_total' || tipoFachada === 'alveolar_total') {
                hMuro = altura;
            } else if (tipoFachada.startsWith('alveolar_')) {
                if (tipoFachada.startsWith('alveolar_12')) hMuro = 1.2;
                else if (tipoFachada.startsWith('alveolar_24')) hMuro = 2.4;
                else if (tipoFachada.startsWith('alveolar_36')) hMuro = 3.6;
            } else if (tipoFachada.startsWith('bloque_')) {
                if (tipoFachada.startsWith('bloque_1')) hMuro = 1.0;
                else if (tipoFachada.startsWith('bloque_2')) hMuro = 2.0;
                else if (tipoFachada.startsWith('bloque_3')) hMuro = 3.0;
            }
            hMuro = Math.min(hMuro, altura);

            const tieneMuro = hMuro > 0;
            const tieneSuperior = hMuro < altura;
            const hSuperior = altura - hMuro;

            // A. Renderizar Muro / Zócalo Inferior (Bloque o Placa Alveolar)
            if (tieneMuro) {
                const espesorMuro = 0.16;
                // Muro Lateral Izquierdo
                const muroIzq = new THREE.Mesh(new THREE.BoxGeometry(espesorMuro, hMuro, longitud), matMuro);
                muroIzq.position.set(-luz / 2, hMuro / 2, 0);
                muroIzq.castShadow = true;
                muroIzq.receiveShadow = true;
                this.naveGroup.add(muroIzq);

                // Muro Lateral Derecho
                const muroDer = new THREE.Mesh(new THREE.BoxGeometry(espesorMuro, hMuro, longitud), matMuro);
                muroDer.position.set(luz / 2, hMuro / 2, 0);
                muroDer.castShadow = true;
                muroDer.receiveShadow = true;
                this.naveGroup.add(muroDer);

                // Muro Hastial Frontal (inferior)
                const muroFrontal = new THREE.Mesh(new THREE.BoxGeometry(luz, hMuro, espesorMuro), matMuro);
                muroFrontal.position.set(0, hMuro / 2, longitud / 2);
                muroFrontal.castShadow = true;
                muroFrontal.receiveShadow = true;
                this.naveGroup.add(muroFrontal);

                // Muro Hastial Trasero (inferior)
                const muroTrasero = new THREE.Mesh(new THREE.BoxGeometry(luz, hMuro, espesorMuro), matMuro);
                muroTrasero.position.set(0, hMuro / 2, -longitud / 2);
                muroTrasero.castShadow = true;
                muroTrasero.receiveShadow = true;
                this.naveGroup.add(muroTrasero);

                // Remate vierteaguas en coronación de zócalo si hay cerramiento superior
                if (tieneSuperior) {
                    const vierteaguasGeo = new THREE.BoxGeometry(0.24, 0.05, longitud + 0.1);
                    const vierteaguasIzq = new THREE.Mesh(vierteaguasGeo, matVierteaguas);
                    vierteaguasIzq.position.set(-luz / 2, hMuro + 0.025, 0);
                    this.naveGroup.add(vierteaguasIzq);

                    const vierteaguasDer = new THREE.Mesh(vierteaguasGeo, matVierteaguas);
                    vierteaguasDer.position.set(luz / 2, hMuro + 0.025, 0);
                    this.naveGroup.add(vierteaguasDer);
                }
            }

            // Cálculo de Peto Perimetral (Cubierta Oculta)
            const conPeto = !!params.conPeto;
            let hPeto = 0;
            if (conPeto) {
                if (params.alturaPeto === 'auto' || !params.alturaPeto) {
                    hPeto = Math.max(0.80, flecha + 0.20);
                } else {
                    hPeto = parseFloat(params.alturaPeto) || 1.0;
                }
            }

            const hSuperiorEfectiva = hSuperior + (conPeto ? hPeto : 0);

            // B. Renderizar Cerramiento Superior (Panel Sándwich o Chapa)
            if (tieneSuperior || conPeto) {
                const yCentroSuperior = hMuro + (hSuperiorEfectiva / 2);

                // Fachada Superior Izquierda
                const fachadaSupIzq = new THREE.Mesh(new THREE.PlaneGeometry(longitud, hSuperiorEfectiva), matFachada);
                fachadaSupIzq.position.set(-luz / 2, yCentroSuperior, 0);
                fachadaSupIzq.rotation.y = Math.PI / 2;
                fachadaSupIzq.receiveShadow = true;
                this.naveGroup.add(fachadaSupIzq);

                // Fachada Superior Derecha
                const fachadaSupDer = new THREE.Mesh(new THREE.PlaneGeometry(longitud, hSuperiorEfectiva), matFachada);
                fachadaSupDer.position.set(luz / 2, yCentroSuperior, 0);
                fachadaSupDer.rotation.y = -Math.PI / 2;
                fachadaSupDer.receiveShadow = true;
                this.naveGroup.add(fachadaSupDer);

                // Hastiales Superiores (Desde hMuro hasta alero/peto y cumbrera)
                const crearHastialShape = () => {
                    const shape = new THREE.Shape();
                    shape.moveTo(-luz / 2, hMuro);
                    shape.lineTo(luz / 2, hMuro);
                    if (conPeto) {
                        const yPeto = altura + hPeto;
                        shape.lineTo(luz / 2, yPeto);
                        shape.lineTo(-luz / 2, yPeto);
                    } else {
                        shape.lineTo(luz / 2, altura);
                        shape.lineTo(0, hCumbrera);
                        shape.lineTo(-luz / 2, altura);
                    }
                    shape.closePath();
                    return shape;
                };

                const hastialGeo = new THREE.ShapeGeometry(crearHastialShape());
                const hastialFrontal = new THREE.Mesh(hastialGeo, matFachada);
                hastialFrontal.position.set(0, 0, longitud / 2);
                this.naveGroup.add(hastialFrontal);

                const hastialTrasero = new THREE.Mesh(hastialGeo, matFachada);
                hastialTrasero.position.set(0, 0, -longitud / 2);
                hastialTrasero.rotation.y = Math.PI;
                this.naveGroup.add(hastialTrasero);

                // Albardilla de Coronación y Revestimiento Interior de Peto (Si está activado)
                if (conPeto) {
                    const acabadoIntPeto = params.acabadoInteriorPeto || 'chapa';
                    const colorIntPeto = acabadoIntPeto === 'panel' ? 0xf8fafc : 0x94a3b8;
                    const matIntPeto = new THREE.MeshStandardMaterial({
                        color: colorIntPeto,
                        roughness: acabadoIntPeto === 'panel' ? 0.6 : 0.45,
                        metalness: acabadoIntPeto === 'panel' ? 0.15 : 0.4,
                        side: THREE.DoubleSide
                    });

                    const yCentroPetoInt = altura + (hPeto / 2);

                    // Revestimiento interior lateral izquierdo
                    const petoIntIzq = new THREE.Mesh(new THREE.PlaneGeometry(longitud, hPeto), matIntPeto);
                    petoIntIzq.position.set(-luz / 2 + 0.05, yCentroPetoInt, 0);
                    petoIntIzq.rotation.y = -Math.PI / 2;
                    this.naveGroup.add(petoIntIzq);

                    // Revestimiento interior lateral derecho
                    const petoIntDer = new THREE.Mesh(new THREE.PlaneGeometry(longitud, hPeto), matIntPeto);
                    petoIntDer.position.set(luz / 2 - 0.05, yCentroPetoInt, 0);
                    petoIntDer.rotation.y = Math.PI / 2;
                    this.naveGroup.add(petoIntDer);

                    // Revestimiento interior frontal
                    const petoIntFront = new THREE.Mesh(new THREE.PlaneGeometry(luz, hPeto), matIntPeto);
                    petoIntFront.position.set(0, yCentroPetoInt, longitud / 2 - 0.05);
                    petoIntFront.rotation.y = Math.PI;
                    this.naveGroup.add(petoIntFront);

                    // Revestimiento interior trasero
                    const petoIntTras = new THREE.Mesh(new THREE.PlaneGeometry(luz, hPeto), matIntPeto);
                    petoIntTras.position.set(0, yCentroPetoInt, -longitud / 2 + 0.05);
                    this.naveGroup.add(petoIntTras);

                    const yTopPeto = altura + hPeto + 0.04;
                    const espesorAlbardilla = 0.22;
                    const altoAlbardilla = 0.06;

                    // Lateral Izquierdo
                    const albIzq = new THREE.Mesh(new THREE.BoxGeometry(espesorAlbardilla, altoAlbardilla, longitud + 0.2), matVierteaguas);
                    albIzq.position.set(-luz / 2, yTopPeto, 0);
                    this.naveGroup.add(albIzq);

                    // Lateral Derecho
                    const albDer = new THREE.Mesh(new THREE.BoxGeometry(espesorAlbardilla, altoAlbardilla, longitud + 0.2), matVierteaguas);
                    albDer.position.set(luz / 2, yTopPeto, 0);
                    this.naveGroup.add(albDer);

                    // Frontal
                    const albFront = new THREE.Mesh(new THREE.BoxGeometry(luz + 0.2, altoAlbardilla, espesorAlbardilla), matVierteaguas);
                    albFront.position.set(0, yTopPeto, longitud / 2);
                    this.naveGroup.add(albFront);

                    // Trasero
                    const albTras = new THREE.Mesh(new THREE.BoxGeometry(luz + 0.2, altoAlbardilla, espesorAlbardilla), matVierteaguas);
                    albTras.position.set(0, yTopPeto, -longitud / 2);
                    this.naveGroup.add(albTras);
                }
            }

            // Puerta Principal en el Testero Frontal
            const nPuertasGrandes = params.numPuertasGrandes !== undefined ? parseInt(params.numPuertasGrandes) : 1;
            if (nPuertasGrandes > 0) {
                const puertaAncho = Math.min(5.0, luz * 0.4);
                const puertaAlto = Math.min(4.8, altura * 0.8);
                const puertaMesh = new THREE.Mesh(new THREE.BoxGeometry(puertaAncho, puertaAlto, 0.12), matPuerta);
                puertaMesh.position.set(0, puertaAlto / 2, longitud / 2 + 0.08);
                this.naveGroup.add(puertaMesh);
            }

            // Puerta Peatonal Lateral
            const nPuertasPeatonales = params.numPuertasPeatonales !== undefined ? parseInt(params.numPuertasPeatonales) : 1;
            if (nPuertasPeatonales > 0) {
                const peatonalMesh = new THREE.Mesh(new THREE.BoxGeometry(0.12, 2.10, 1.00), matPuerta);
                peatonalMesh.position.set(-luz / 2 - 0.06, 1.05, longitud / 4);
                this.naveGroup.add(peatonalMesh);
            }
        }

        // 6. Canalones de Recogida de Aguas Pluviales y Bajantes
        const tipoCanalon = params.tipoCanalon || (conPeto ? 'interior' : 'exterior');
        if (tipoCanalon !== 'sin') {
            const matCanalon = new THREE.MeshStandardMaterial({
                color: 0x334155, // Antracita metálico / zinc
                roughness: 0.4,
                metalness: 0.6
            });
            const matBajante = new THREE.MeshStandardMaterial({
                color: 0x475569, // Gris chapa bajante
                roughness: 0.5,
                metalness: 0.5
            });

            if (tipoCanalon === 'exterior') {
                // Canalón exterior en aleros laterales (x = -luz/2 y x = luz/2 a la altura de alero)
                const yAlero = altura + 0.05;
                const canalonGeo = new THREE.BoxGeometry(0.18, 0.16, longitud + 0.35);

                const canalonIzq = new THREE.Mesh(canalonGeo, matCanalon);
                canalonIzq.position.set(-luz / 2 - 0.09, yAlero, 0);
                canalonIzq.castShadow = true;
                this.naveGroup.add(canalonIzq);

                const canalonDer = new THREE.Mesh(canalonGeo, matCanalon);
                canalonDer.position.set(luz / 2 + 0.09, yAlero, 0);
                canalonDer.castShadow = true;
                this.naveGroup.add(canalonDer);

                // 4 Bajantes pluviales en las esquinas hasta cota cero
                const bajanteGeo = new THREE.CylinderGeometry(0.06, 0.06, altura, 12);
                const posBajantes = [
                    { x: -luz / 2 - 0.12, z: -longitud / 2 + 0.15 },
                    { x: -luz / 2 - 0.12, z: longitud / 2 - 0.15 },
                    { x: luz / 2 + 0.12, z: -longitud / 2 + 0.15 },
                    { x: luz / 2 + 0.12, z: longitud / 2 - 0.15 }
                ];
                posBajantes.forEach(pos => {
                    const bajante = new THREE.Mesh(bajanteGeo, matBajante);
                    bajante.position.set(pos.x, altura / 2, pos.z);
                    bajante.castShadow = true;
                    this.naveGroup.add(bajante);
                });
            } else if (tipoCanalon === 'interior') {
                // Canalón interior oculto detrás de peto (x = -luz/2 + 0.14 y x = luz/2 - 0.14)
                const yAlero = altura + 0.05;
                const canalonIntGeo = new THREE.BoxGeometry(0.24, 0.14, longitud);

                const canalonIntIzq = new THREE.Mesh(canalonIntGeo, matCanalon);
                canalonIntIzq.position.set(-luz / 2 + 0.14, yAlero, 0);
                this.naveGroup.add(canalonIntIzq);

                const canalonIntDer = new THREE.Mesh(canalonIntGeo, matCanalon);
                canalonIntDer.position.set(luz / 2 - 0.14, yAlero, 0);
                this.naveGroup.add(canalonIntDer);
            }
        }

        // --- Elementos exteriores de referencia de escala (Personas y Vehículo) ---
        while (this.grupoPersonas.children.length > 0) {
            this.grupoPersonas.remove(this.grupoPersonas.children[0]);
        }
        while (this.grupoVehiculos.children.length > 0) {
            this.grupoVehiculos.remove(this.grupoVehiculos.children[0]);
        }

        // 1. Figura humana a escala real (1,80 m): Ingeniero junto a la puerta frontal
        const p1 = this.crearFiguraHumana(Math.min(3.2, luz * 0.32), longitud / 2 + 1.8, Math.PI * 0.95, true, 0x2563eb);
        this.grupoPersonas.add(p1);

        // Figura humana 2: Operario de obra junto al acceso lateral
        const p2 = this.crearFiguraHumana(-luz / 2 - 1.6, longitud / 4 + 0.5, Math.PI * 0.45, true, 0x0284c7);
        this.grupoPersonas.add(p2);

        this.grupoPersonas.visible = this.verPersonas;

        // 2. Vehículo a escala real (4,40m x 1,85m x 1,55m): Estacionado en la explanada exterior
        const posXAuto = Math.max(3.8, luz * 0.35 + 2.2);
        const posZAuto = longitud / 2 + 4.8;
        const coche = this.crearVehiculo(posXAuto, posZAuto, -Math.PI / 10);
        this.grupoVehiculos.add(coche);

        this.grupoVehiculos.visible = this.verVehiculos;

        // Ajustar posición del objetivo de la cámara al centroide de la nave
        if (this.controls) {
            this.controls.target.set(0, hCumbrera / 2, 0);
            this.camera.position.set(luz * 1.5, hCumbrera * 2.2, longitud * 1.1);
        }
    }

    crearFiguraHumana(x, z, rotY, tieneCasco = true, colorRopa = 0x2563eb) {
        const grupo = new THREE.Group();
        grupo.position.set(x, 0, z);
        grupo.rotation.y = rotY;

        // Materiales
        const matPiel = new THREE.MeshStandardMaterial({ color: 0xfbcfe8, roughness: 0.6 });
        const matRopa = new THREE.MeshStandardMaterial({ color: colorRopa, roughness: 0.7 });
        const matPantalon = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.8 });
        const matZapatos = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.9 });
        const matCasco = new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.3, metalness: 0.2 });
        const matChaleco = new THREE.MeshStandardMaterial({ color: 0xf97316, roughness: 0.5 });

        // Calzado (h: 0.08m)
        const zapatoGeo = new THREE.BoxGeometry(0.12, 0.08, 0.24);
        const zapatoIzq = new THREE.Mesh(zapatoGeo, matZapatos);
        zapatoIzq.position.set(-0.11, 0.04, 0.02);
        zapatoIzq.castShadow = true;
        grupo.add(zapatoIzq);

        const zapatoDer = new THREE.Mesh(zapatoGeo, matZapatos);
        zapatoDer.position.set(0.11, 0.04, 0.02);
        zapatoDer.castShadow = true;
        grupo.add(zapatoDer);

        // Piernas (h: 0.80m)
        const piernaGeo = new THREE.CylinderGeometry(0.065, 0.055, 0.80, 8);
        const piernaIzq = new THREE.Mesh(piernaGeo, matPantalon);
        piernaIzq.position.set(-0.11, 0.48, 0);
        piernaIzq.castShadow = true;
        grupo.add(piernaIzq);

        const piernaDer = new THREE.Mesh(piernaGeo, matPantalon);
        piernaDer.position.set(0.11, 0.48, 0);
        piernaDer.castShadow = true;
        grupo.add(piernaDer);

        // Torso / Cuerpo (h: 0.58m, hasta y=1.46m)
        const torsoGeo = new THREE.BoxGeometry(0.38, 0.58, 0.22);
        const torso = new THREE.Mesh(torsoGeo, tieneCasco ? matChaleco : matRopa);
        torso.position.set(0, 1.17, 0);
        torso.castShadow = true;
        grupo.add(torso);

        // Banda reflectante en chaleco de seguridad
        if (tieneCasco) {
            const bandaMat = new THREE.MeshStandardMaterial({ color: 0xfef08a, roughness: 0.2, metalness: 0.4 });
            const banda = new THREE.Mesh(new THREE.BoxGeometry(0.39, 0.06, 0.23), bandaMat);
            banda.position.set(0, 1.15, 0);
            grupo.add(banda);
        }

        // Brazos (h: 0.50m)
        const brazoGeo = new THREE.CylinderGeometry(0.045, 0.04, 0.50, 8);
        const brazoIzq = new THREE.Mesh(brazoGeo, matRopa);
        brazoIzq.position.set(-0.24, 1.16, 0);
        brazoIzq.castShadow = true;
        grupo.add(brazoIzq);

        const brazoDer = new THREE.Mesh(brazoGeo, matRopa);
        brazoDer.position.set(0.24, 1.16, 0);
        brazoDer.castShadow = true;
        grupo.add(brazoDer);

        // Cabeza (altura cumbre: 1.76 - 1.80m)
        const cabezaGeo = new THREE.SphereGeometry(0.11, 12, 12);
        const cabeza = new THREE.Mesh(cabezaGeo, matPiel);
        cabeza.position.set(0, 1.58, 0);
        cabeza.castShadow = true;
        grupo.add(cabeza);

        // Casco de seguridad reglamentario
        if (tieneCasco) {
            const cascoGeo = new THREE.SphereGeometry(0.125, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2);
            const casco = new THREE.Mesh(cascoGeo, matCasco);
            casco.position.set(0, 1.62, 0);
            grupo.add(casco);

            const viseraCasco = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.02, 12, 1, false, 0, Math.PI), matCasco);
            viseraCasco.rotation.y = -Math.PI / 2;
            viseraCasco.position.set(0, 1.61, 0.04);
            grupo.add(viseraCasco);
        }

        return grupo;
    }

    crearVehiculo(x, z, rotY) {
        const car = new THREE.Group();
        car.position.set(x, 0, z);
        car.rotation.y = rotY;

        // Proporciones estándar vehículo turismo / SUV (L: 4.40m, W: 1.85m, H: 1.55m)
        const carLength = 4.40;
        const carWidth = 1.85;

        // Materiales
        const matChasis = new THREE.MeshStandardMaterial({
            color: 0x1e3a8a, // Azul marino metalizado
            roughness: 0.35,
            metalness: 0.75
        });
        const matBajos = new THREE.MeshStandardMaterial({
            color: 0x0f172a,
            roughness: 0.85
        });
        const matCristales = new THREE.MeshStandardMaterial({
            color: 0x0284c7,
            roughness: 0.1,
            metalness: 0.9,
            transparent: true,
            opacity: 0.7
        });
        const matRuedas = new THREE.MeshStandardMaterial({
            color: 0x18181b,
            roughness: 0.9
        });
        const matLlantas = new THREE.MeshStandardMaterial({
            color: 0xe2e8f0,
            roughness: 0.3,
            metalness: 0.85
        });
        const matFaros = new THREE.MeshStandardMaterial({
            color: 0xffffff,
            roughness: 0.1,
            emissive: 0xe0f2fe,
            emissiveIntensity: 0.7
        });
        const matPilotos = new THREE.MeshStandardMaterial({
            color: 0xdc2626,
            roughness: 0.2,
            emissive: 0xef4444,
            emissiveIntensity: 0.6
        });

        // 1. Carrocería inferior principal (de y=0.25 a y=0.85, h=0.60m)
        const bodyGeo = new THREE.BoxGeometry(carWidth, 0.60, carLength);
        const bodyMesh = new THREE.Mesh(bodyGeo, matChasis);
        bodyMesh.position.set(0, 0.55, 0);
        bodyMesh.castShadow = true;
        bodyMesh.receiveShadow = true;
        car.add(bodyMesh);

        // Paragolpes y bajos
        const bajosGeo = new THREE.BoxGeometry(carWidth + 0.02, 0.18, carLength + 0.04);
        const bajosMesh = new THREE.Mesh(bajosGeo, matBajos);
        bajosMesh.position.set(0, 0.26, 0);
        car.add(bajosMesh);

        // 2. Cabina superior / Habitáculo acristalado (de y=0.85 a y=1.45, h=0.60m)
        const cabinGeo = new THREE.BoxGeometry(carWidth * 0.86, 0.60, 2.30);
        const cabinMesh = new THREE.Mesh(cabinGeo, matCristales);
        cabinMesh.position.set(0, 1.15, -0.20);
        cabinMesh.castShadow = true;
        car.add(cabinMesh);

        // Techo de chapa
        const roofGeo = new THREE.BoxGeometry(carWidth * 0.84, 0.05, 2.20);
        const roofMesh = new THREE.Mesh(roofGeo, matChasis);
        roofMesh.position.set(0, 1.45, -0.20);
        roofMesh.castShadow = true;
        car.add(roofMesh);

        // 3. Faros delanteros (+Z frontal) y Pilotos traseros (-Z)
        const faroGeo = new THREE.BoxGeometry(0.35, 0.12, 0.08);
        const faroIzq = new THREE.Mesh(faroGeo, matFaros);
        faroIzq.position.set(-carWidth / 2 + 0.28, 0.60, carLength / 2 + 0.02);
        car.add(faroIzq);

        const faroDer = new THREE.Mesh(faroGeo, matFaros);
        faroDer.position.set(carWidth / 2 - 0.28, 0.60, carLength / 2 + 0.02);
        car.add(faroDer);

        const pilotoGeo = new THREE.BoxGeometry(0.35, 0.12, 0.08);
        const pilotoIzq = new THREE.Mesh(pilotoGeo, matPilotos);
        pilotoIzq.position.set(-carWidth / 2 + 0.28, 0.65, -carLength / 2 - 0.02);
        car.add(pilotoIzq);

        const pilotoDer = new THREE.Mesh(pilotoGeo, matPilotos);
        pilotoDer.position.set(carWidth / 2 - 0.28, 0.65, -carLength / 2 - 0.02);
        car.add(pilotoDer);

        // 4. Ruedas (4 unidades completas con llantas)
        const ruedaGeo = new THREE.CylinderGeometry(0.34, 0.34, 0.24, 16);
        const llantaGeo = new THREE.CylinderGeometry(0.20, 0.20, 0.245, 12);

        const posicionesRuedas = [
            { x: -carWidth / 2 - 0.02, z: 1.35 },  // Delantera Izq
            { x: carWidth / 2 + 0.02, z: 1.35 },   // Delantera Der
            { x: -carWidth / 2 - 0.02, z: -1.35 }, // Trasera Izq
            { x: carWidth / 2 + 0.02, z: -1.35 }   // Trasera Der
        ];

        posicionesRuedas.forEach(pos => {
            const ruedaGroup = new THREE.Group();
            ruedaGroup.position.set(pos.x, 0.34, pos.z);
            ruedaGroup.rotation.z = Math.PI / 2;

            const rueda = new THREE.Mesh(ruedaGeo, matRuedas);
            rueda.castShadow = true;
            ruedaGroup.add(rueda);

            const llanta = new THREE.Mesh(llantaGeo, matLlantas);
            ruedaGroup.add(llanta);

            car.add(ruedaGroup);
        });

        // Retrovisores laterales
        const retroGeo = new THREE.BoxGeometry(0.18, 0.10, 0.12);
        const retroIzq = new THREE.Mesh(retroGeo, matChasis);
        retroIzq.position.set(-carWidth / 2 - 0.10, 0.92, 0.70);
        car.add(retroIzq);

        const retroDer = new THREE.Mesh(retroGeo, matChasis);
        retroDer.position.set(carWidth / 2 + 0.10, 0.92, 0.70);
        car.add(retroDer);

        return car;
    }

    togglePersonas(visible) {
        if (visible !== undefined) this.verPersonas = visible;
        else this.verPersonas = !this.verPersonas;
        this.grupoPersonas.visible = this.verPersonas;
        return this.verPersonas;
    }

    toggleVehiculos(visible) {
        if (visible !== undefined) this.verVehiculos = visible;
        else this.verVehiculos = !this.verVehiculos;
        this.grupoVehiculos.visible = this.verVehiculos;
        return this.verVehiculos;
    }

    setVisibilidad(estructura, cerramientos, cubierta) {
        this.verEstructura = estructura;
        this.verCerramientos = cerramientos;
        this.verCubierta = cubierta;
    }

    onWindowResize() {
        if (!this.container || !this.renderer || !this.camera) return;
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        if (this.autoRotar && this.controls) {
            this.controls.autoRotate = true;
            this.controls.autoRotateSpeed = 1.2;
        } else if (this.controls) {
            this.controls.autoRotate = false;
        }
        if (this.controls) this.controls.update();
        if (this.renderer && this.scene && this.camera) {
            this.renderer.render(this.scene, this.camera);
        }
    }
}
