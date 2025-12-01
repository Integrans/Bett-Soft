document.addEventListener("DOMContentLoaded", () => {
    console.log("reportar.js cargado");

    const form = document.getElementById("reporte-form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Obtener valores EXACTOS del HTML
        const numeroCuenta = document.querySelector('[name="numero_cuenta"]').value.trim();
        const tipoProblema = document.querySelector('[name="tipo_problema"]').value;
        const edificio = document.querySelector('[name="edificio"]').value;
        const nivel = document.querySelector('[name="nivel"]').value;
        const sexo = document.querySelector('[name="sexo"]').value;
        const tazaOOrinal = document.querySelector('[name="taza_o_orinal"]').value;
        const pasillo = document.querySelector('[name="pasillo"]').value;
        const fileUpload = document.querySelector('[name="file_upload"]').files[0];

        // Validación básica
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
                try {
                    data = await response.json(); // evita error si no viene JSON
                } catch (_) {}

                console.log("Respuesta del servidor:", data);
                alert("Reporte enviado con éxito.");
                form.reset();

            } else {
                const error = await response.text();
                console.error("Error del servidor:", error);
                alert("Error al enviar reporte:\n" + error);
            }

        } catch (err) {
            console.error("Error de conexión:", err);
            alert("No se pudo conectar con el servidor.");
        }
    });
});



