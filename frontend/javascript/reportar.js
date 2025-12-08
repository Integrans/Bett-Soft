document.addEventListener("DOMContentLoaded", () => {
    console.log("reportar.js cargado correctamente");

    const tipoSelect = document.getElementById("select-tipo");
    const edificioSelect = document.getElementById("select-edificio");
    const nivelSelect = document.getElementById("select-nivel");
    const sexoSelect = document.getElementById("select-sexo");

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

    // Listeners
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

    // =======================================================
    //     📸 CONFIGURACIÓN PARA FORZAR CÁMARA + PREVIEW
    // =======================================================

    const inputCamara = document.querySelector('[name="file_upload"]');
    const preview = document.getElementById("preview-foto");
    const btnRepetir = document.getElementById("repetir-foto");

    // Forzar cámara siempre
    inputCamara.setAttribute("accept", "image/*");
    inputCamara.setAttribute("capture", "environment");

    // Mostrar previsualización
    inputCamara.addEventListener("change", () => {
        const file = inputCamara.files[0];
        if (!file) return;

        const url = URL.createObjectURL(file);
        preview.src = url;
        preview.classList.remove("hidden");
        btnRepetir.classList.remove("hidden");
    });

    // Repetir foto
    btnRepetir.addEventListener("click", () => {
        inputCamara.value = "";
        preview.src = "";
        preview.classList.add("hidden");
        btnRepetir.classList.add("hidden");
    });

    // ================================
    //       ENVÍO DEL FORMULARIO
    // ================================
    const form = document.getElementById("reporte-form");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const numeroCuenta = document.querySelector('[name="numero_cuenta"]').value.trim();
        const tipoProblema = tipoSelect.value;
        const edificio = edificioSelect.value;
        const nivel = nivelSelect.value;
        const sexo = sexoSelect.value;
        const pasillo = document.querySelector('[name="pasillo"]').value;
        const esAnonimo = document.querySelector('[name="es_anonimo"]').checked;
        const fileUpload = document.querySelector('[name="file_upload"]').files[0];

        if (!tipoProblema || !edificio || !nivel || !sexo) {
            alert("Por favor llena todos los campos obligatorios.");
            return;
        }

        const taza_o_orinal = esMingitorioSegunTipo(tipoProblema) ? "orinal" : "taza";

        const formData = new FormData();
        formData.append("numero_cuenta", numeroCuenta);
        formData.append("tipo_problema", tipoProblema);
        formData.append("edificio", edificio);
        formData.append("nivel", nivel);
        formData.append("sexo", sexo);
        formData.append("taza_o_orinal", taza_o_orinal);
        formData.append("pasillo", pasillo);
        formData.append("es_anonimo", esAnonimo);

        if (fileUpload) formData.append("file_upload", fileUpload);

        try {
            const response = await fetch("http://127.0.0.1:8000/reportes/", {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                alert("Reporte enviado con éxito.");
                form.reset();
                preview.src = "";
                preview.classList.add("hidden");
                btnRepetir.classList.add("hidden");
                nivelSelect.innerHTML = `<option value="">Seleccione nivel</option>`;
                sexoSelect.innerHTML = `<option value="">Seleccione sexo</option>`;
            } else {
                const t = await response.text().catch(()=>null);
                console.error("Error del servidor:", t);
                alert("Error al enviar reporte.");
            }
        } catch (err) {
            alert("No se pudo conectar con el servidor.");
            console.error(err);
        }
    });

    poblarNiveles();
});
