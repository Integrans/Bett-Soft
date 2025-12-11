// javascript/reportar.js
document.addEventListener("DOMContentLoaded", () => {
    console.log("reportar.js cargado correctamente");

    const tipoSelect = document.getElementById("select-tipo");
    const edificioSelect = document.getElementById("select-edificio");
    const nivelSelect = document.getElementById("select-nivel");
    const sexoSelect = document.getElementById("select-sexo");
    const form = document.getElementById("reporte-form");

    // Cámara / preview elements (según tu reportar.html)
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const btnStart = document.getElementById("btn-start");
    const btnTake = document.getElementById("btn-take");
    const btnRetake = document.getElementById("btn-retake");
    const btnConfirm = document.getElementById("btn-confirm");
    const fileFallback = document.getElementById("file-fallback"); // input name="file_upload"

    // Estado de la cámara
    let stream = null;
    let currentPhotoBlob = null; // Blob de la foto confirmada (si la hay)

    // reglas de edificios -> qué sexo hay en cada nivel
    const reglas = {
        "A1-A2": { niveles: { 1: "M", 2: "H" } },
        "A3-A4": { niveles: { 1: "M", 2: "H" } },
        "A5-A6": { niveles: { 1: "M", 2: "H" } },
        "A7-A8": { niveles: { 1: "M", 2: "Mixto" } },
        "A9-A10": { niveles: { 1: "M", 2: "H" } },
        "A11-A12": { niveles: { 1: "M", 2: "H" } },
        "Idiomas": { niveles: { 1: "Ambos", 2: "Ambos" } },
        "A15": { niveles: { 0: "Ambos", 1: "Ambos", 2: "Ambos" } },
        "CEDETEC": { niveles: { 1: "Ambos" } },
        "Posgrado": { niveles: { 1: "Ambos" } },
        "CEMM": { niveles: { 1: "Ambos" } }
    };

    function esMingitorioSegunTipo(tipoProblema) {
        return tipoProblema && tipoProblema.toLowerCase().includes("orinal");
    }

    function nivelValidoParaMingitorio(edificio, nivel) {
        const regla = reglas[edificio];
        if (!regla) return false;
        if (edificio === "Idiomas" || edificio === "A15") return true;
        const tipo = regla.niveles[nivel];
        return tipo === "H" || tipo === "Mixto" || tipo === "Ambos";
    }

    function poblarNiveles() {
        const edificio = edificioSelect.value;
        const tipoProblema = tipoSelect.value;
        const mingitorio = esMingitorioSegunTipo(tipoProblema);

        nivelSelect.innerHTML = `<option value="">Seleccione nivel</option>`;
        sexoSelect.innerHTML = `<option value="">Seleccione sexo</option>`;

        if (!edificio || !reglas[edificio]) return;

        const niveles = reglas[edificio].niveles;

        Object.keys(niveles).forEach(n => {
            if (mingitorio) {
                if (nivelValidoParaMingitorio(edificio, n)) {
                    nivelSelect.innerHTML += `<option value="${n}">Nivel ${n}</option>`;
                }
            } else {
                nivelSelect.innerHTML += `<option value="${n}">Nivel ${n}</option>`;
            }
        });
    }

    function poblarSexoSegunNivel() {
        const edificio = edificioSelect.value;
        const nivel = nivelSelect.value;
        const tipoProblema = tipoSelect.value;
        const mingitorio = esMingitorioSegunTipo(tipoProblema);

        sexoSelect.innerHTML = `<option value="">Seleccione sexo</option>`;

        if (!edificio || !nivel || !reglas[edificio]) return;

        const tipo = reglas[edificio].niveles[nivel];

        if (mingitorio) {
            if (!nivelValidoParaMingitorio(edificio, nivel)) {
                sexoSelect.innerHTML = `<option value="">No válido para mingitorio</option>`;
                return;
            }
            if (tipo === "H") sexoSelect.innerHTML = `<option value="H">Hombres</option>`;
            else if (tipo === "Mixto") sexoSelect.innerHTML = `
                <option value="H">Hombres</option>
                <option value="Mixto">Mixto</option>`;
            else if (tipo === "Ambos") sexoSelect.innerHTML = `
                <option value="H">Hombres</option>
                <option value="Mixto">Mixto</option>`;
            return;
        }

        if (tipo === "M") sexoSelect.innerHTML = `<option value="M">Mujeres</option>`;
        else if (tipo === "H") sexoSelect.innerHTML = `<option value="H">Hombres</option>`;
        else if (tipo === "Mixto") sexoSelect.innerHTML = `
            <option value="M">Mujeres</option>
            <option value="H">Hombres</option>
            <option value="Mixto">Mixto</option>`;
        else if (tipo === "Ambos") sexoSelect.innerHTML = `
            <option value="M">Mujeres</option>
            <option value="H">Hombres</option>`;
    }

    // listeners de selects
    tipoSelect.addEventListener("change", () => {
        poblarNiveles();
        poblarSexoSegunNivel();
    });
    edificioSelect.addEventListener("change", () => {
        poblarNiveles();
        poblarSexoSegunNivel();
    });
    nivelSelect.addEventListener("change", () => {
        poblarSexoSegunNivel();
    });

    // ---------- Cámara: helpers ----------
    function showVideoUI() {
        if (video) video.classList.remove("hidden");
        if (canvas) canvas.classList.add("hidden");
        if (btnTake) btnTake.classList.remove("hidden");
        if (btnConfirm) btnConfirm.classList.add("hidden");
        if (btnRetake) btnRetake.classList.add("hidden");
    }

    function showPreviewUI() {
        if (video) video.classList.add("hidden");
        if (canvas) canvas.classList.remove("hidden");
        if (btnTake) btnTake.classList.add("hidden");
        if (btnConfirm) btnConfirm.classList.remove("hidden");
        if (btnRetake) btnRetake.classList.remove("hidden");
    }

    // Inicia stream desde cámara (permite cámara trasera con facingMode 'environment')
    async function startCamera() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            console.warn("getUserMedia no soportado en este navegador");
            if (fileFallback) fileFallback.parentElement.classList.remove("hidden");
            return;
        }
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: { ideal: "environment" } },
                audio: false
            });
            if (video) {
                video.srcObject = stream;
                video.play().catch(()=>{});
                showVideoUI();
            }
        } catch (err) {
            console.error("Error al abrir cámara:", err);
            if (fileFallback) fileFallback.parentElement.classList.remove("hidden");
        }
    }

    // Detener stream cuando ya no sea necesario
    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(t => t.stop());
            stream = null;
        }
    }

    // Toma foto del video al canvas
    function takePhotoToCanvas() {
        if (!video || !canvas) return;
        const w = video.videoWidth || 1280;
        const h = video.videoHeight || 720;
        canvas.width = w;
        canvas.height = h;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, w, h);
        showPreviewUI();
    }

    // Convierte canvas a blob (jpeg)
    function canvasToBlobPromise(canvasEl, quality = 0.85) {
        return new Promise((resolve) => {
            canvasEl.toBlob((blob) => {
                resolve(blob);
            }, "image/jpeg", quality);
        });
    }

    // ---------- Wiring de botones (si existen en DOM) ----------
    if (btnStart) {
        btnStart.addEventListener("click", async () => {
            await startCamera();
        });
    }

    if (btnTake) {
        btnTake.addEventListener("click", () => {
            takePhotoToCanvas();
        });
    }

    if (btnRetake) {
        btnRetake.addEventListener("click", () => {
            // volver a cámara, borrar foto previa
            currentPhotoBlob = null;
            if (canvas) {
                const ctx = canvas.getContext && canvas.getContext("2d");
                if (ctx) ctx.clearRect(0, 0, canvas.width, canvas.height);
            }
            showVideoUI();
        });
    }

    if (btnConfirm) {
        btnConfirm.addEventListener("click", async () => {
            if (!canvas) return;
            // convertir canvas a blob y guardarlo
            const blob = await canvasToBlobPromise(canvas);
            if (blob) {
                // crear nombre de archivo simple
                const filename = `foto_incidente.jpg`;
                currentPhotoBlob = new File([blob], filename, { type: blob.type });
                // ya no necesitamos el video abierto
                stopCamera();
            }
            // UI: dejar canvas visible como preview y ocultar controles
            if (btnTake) btnTake.classList.add("hidden");
            if (btnConfirm) btnConfirm.classList.add("hidden");
            if (btnRetake) btnRetake.classList.remove("hidden");
        });
    }

    // Si el usuario usa el fallback file input (por ejemplo navegador que no permite getUserMedia)
    if (fileFallback) {
        // Aseguramos atributos para forzar cámara en mobile si es posible
        fileFallback.setAttribute("accept", "image/*");
        fileFallback.setAttribute("capture", "environment");

        fileFallback.addEventListener("change", () => {
            const f = fileFallback.files && fileFallback.files[0];
            if (!f) return;
            currentPhotoBlob = f; // usaremos este file al enviar
            // mostrar canvas preview con la imagen seleccionada (opcional)
            const reader = new FileReader();
            reader.onload = function (ev) {
                if (!canvas) return;
                const img = new Image();
                img.onload = function () {
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext("2d");
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                    // mostrar canvas como preview
                    canvas.classList.remove("hidden");
                    if (video) video.classList.add("hidden");
                    if (btnRetake) btnRetake.classList.remove("hidden");
                    if (btnConfirm) btnConfirm.classList.add("hidden");
                    if (btnTake) btnTake.classList.add("hidden");
                };
                img.src = ev.target.result;
            };
            reader.readAsDataURL(f);
        });
    }

    // ================================
    //       ENVÍO DEL FORMULARIO
    // ================================
    if (!form) {
        console.error("No se encontró el formulario con id 'reporte-form'");
        return;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Recolectar campos
        const numeroCuenta = (document.querySelector('[name="numero_cuenta"]') || {}).value || "";
        const tipoProblema = tipoSelect.value;
        const edificio = edificioSelect.value;
        const nivel = nivelSelect.value;
        const sexo = sexoSelect.value;
        const pasillo = (document.querySelector('[name="pasillo"]') || {}).value || "";
        const esAnonimoChecked = (document.querySelector('[name="es_anonimo"]') || {}).checked || false;

        // Validación mínima (backend también valida)
        if (!tipoProblema || !edificio || nivel === "" || !sexo) {
            showToast("Por favor llena todos los campos obligatorios.", "error");
            return;
        }

        // preparar formdata exactamente con las claves que espera el backend
        const formData = new FormData();
        formData.append("numero_cuenta", numeroCuenta);
        formData.append("tipo_problema", tipoProblema);
        formData.append("edificio", edificio);
        formData.append("nivel", nivel); // backend convertirá a int
        formData.append("sexo", sexo);
        formData.append("taza_o_orinal", esMingitorioSegunTipo(tipoProblema) ? "orinal" : "taza");
        formData.append("pasillo", pasillo);
        // FastAPI parsea "true"/"false" para booleans; enviamos string "true" o "false"
        formData.append("es_anonimo", esAnonimoChecked ? "true" : "false");

        // adjuntar foto confirmada (preferir currentPhotoBlob > fallback file input)
        if (currentPhotoBlob) {
            formData.append("file_upload", currentPhotoBlob, currentPhotoBlob.name || "foto_incidente.jpg");
        } else {
            // si no hay currentPhotoBlob, revisar fallback (por si usuario seleccionó archivo)
            if (fileFallback && fileFallback.files && fileFallback.files[0]) {
                formData.append("file_upload", fileFallback.files[0], fileFallback.files[0].name);
            }
            // Si tampoco hay file, no se agrega (imagen es opcional)
        }

        try {
            const resp = await fetch("http://127.0.0.1:8000/reportes/", {
                method: "POST",
                body: formData
            });

            if (resp.ok) {
                showToast("Reporte enviado con éxito.", "success");
                // limpiar estado UI
                form.reset();
                currentPhotoBlob = null;
                if (canvas) {
                    const ctx = canvas.getContext && canvas.getContext("2d");
                    if (ctx) ctx.clearRect(0, 0, canvas.width, canvas.height);
                    canvas.classList.add("hidden");
                }
                if (video) {
                    video.pause();
                    video.srcObject = null;
                    video.classList.add("hidden");
                }
                stopCamera();
                // reset selects UI
                nivelSelect.innerHTML = `<option value="">Seleccione nivel</option>`;
                sexoSelect.innerHTML = `<option value="">Seleccione sexo</option>`;
            } else {
                const txt = await resp.text().catch(()=>null);
                console.error("Error del servidor:", txt || resp.status);
                showToast("Error al enviar reporte. Revisa la consola para más detalle.", "error");
            }
        } catch (err) {
            console.error("Error al enviar:", err);
            showToast("No se pudo conectar con el servidor.", "error");
        }
    });

    // Inicializar estados UI: esconder canvas si existe
    if (canvas) canvas.classList.add("hidden");
    if (video) video.classList.add("hidden");
    // show fallback file input hidden by default (HTML already hides fallback)
    // listo
    poblarNiveles();
});
