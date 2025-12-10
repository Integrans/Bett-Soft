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

        alert("Reporte creado con folio: " + data.folio);
        return data;

    } catch (error) {
        console.error("Error:", error);
        alert("Error al enviar el reporte");
    }
}

document.getElementById("formReporte").addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    await enviarReporte(formData);
});


console.log("CARGANDO reportes.js");
