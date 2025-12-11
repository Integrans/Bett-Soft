// URL del backend
const API_URL = "http://127.0.0.1:8000/reportes/";

async function enviarReporte(formData) {
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Error al enviar el reporte");
        }

        showToast("Reporte creado. Folio: " + data.folio, "success");
        return data;

    } catch (error) {
        console.error("Error:", error);
        showToast("No se pudo enviar el reporte.", "error");
    }
}

document.getElementById("formReporte").addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    await enviarReporte(formData);
});


console.log("CARGANDO reportes.js");
