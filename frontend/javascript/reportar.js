document.addEventListener("DOMContentLoaded", () => {
    console.log("reportar.js cargado");

    // ---------------------------------------------------------
    // 1. LÓGICA DE FILTRADO (D-01) - ¡Esto va primero!
    // ---------------------------------------------------------
    const selectSexo = document.getElementById("sexo");
    const selectProblema = document.getElementById("tipo_problema");
    const selectMueble = document.getElementById("taza_orinal");

    function filtrarOpciones() {
        // Validación de seguridad por si no encuentra los elementos
        if (!selectSexo || !selectProblema || !selectMueble) return;

        const sexoSeleccionado = selectSexo.value;
        const opcionOrinalProblema = selectProblema.querySelector('option[value="orinal_tapado"]');
        const opcionOrinalMueble = selectMueble.querySelector('option[value="orinal"]');

        if (sexoSeleccionado === "M") {
            // --- CASO MUJERES: OCULTAR ORINAL ---
            if (opcionOrinalProblema) opcionOrinalProblema.style.display = "none";
            if (opcionOrinalMueble) opcionOrinalMueble.style.display = "none";

            // Resetear valores si estaban en orinal
            if (selectProblema.value === "orinal_tapado") selectProblema.value = "taza_tapada";
            if (selectMueble.value === "orinal") selectMueble.value = "taza";

        } else {
            // --- CASO HOMBRES O MIXTO: MOSTRAR TODO ---
            if (opcionOrinalProblema) opcionOrinalProblema.style.display = "block";
            if (opcionOrinalMueble) opcionOrinalMueble.style.display = "block";
        }
    }

    // Activar listeners del filtro (si existen los elementos)
    if (selectSexo) {
        selectSexo.addEventListener("change", filtrarOpciones);
        filtrarOpciones(); // Ejecutar al inicio
    }


    // ---------------------------------------------------------
    // 2. LÓGICA DE ENVÍO (SUBMIT)
    // ---------------------------------------------------------
    const form = document.getElementById("reporte-form");

    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            // Obtener valores
            const numeroCuenta = document.querySelector('[name="numero_cuenta"]').value.trim();
            const tipoProblema = document.querySelector('[name="tipo_problema"]').value;
            const edificio = document.querySelector('[name="edificio"]').value;
            const nivel = document.querySelector('[name="nivel"]').value;
            const sexo = document.querySelector('[name="sexo"]').value;
            const tazaOOrinal = document.querySelector('[name="taza_o_orinal"]').value;
            const pasillo = document.querySelector('[name="pasillo"]').value;
            
            // Manejo seguro del input file
            const fileInput = document.querySelector('[name="file_upload"]');
            const fileUpload = fileInput ? fileInput.files[0] : null;

            // Validación
            if (!numeroCuenta || !tipoProblema || !edificio || !nivel || !sexo || !tazaOOrinal || !pasillo) {
                alert("Por favor llena todos los campos antes de enviar.");
                return;
            }

            // Crear FormData
            const formData = new FormData();
            formData.append("numero_cuenta", numeroCuenta);
            formData.append("tipo_problema", tipoProblema);
            formData.append("edificio", edificio);
            formData.append("nivel", nivel);
            formData.append("sexo", sexo);
            formData.append("taza_o_orinal", tazaOOrinal);
            formData.append("pasillo", pasillo);

            if (fileUpload) {
                formData.append("file_upload", fileUpload);
            }

            try {
                const response = await fetch("http://127.0.0.1:8000/reportes/", {
                    method: "POST",
                    body: formData
                });

                if (response.ok) {
                    let data = {};
                    try { data = await response.json(); } catch (_) {}
                    
                    console.log("Respuesta:", data);
                    alert("Reporte enviado con éxito.");
                    form.reset();
                    
                    // IMPORTANTE: Volver a ejecutar el filtro tras el reset del formulario
                    filtrarOpciones(); 

                } else {
                    const errorText = await response.text();
                    alert("Error al enviar reporte:\n" + errorText);
                }

            } catch (err) {
                console.error("Error de conexión:", err);
                alert("No se pudo conectar con el servidor.");
            }
        });
    }
});