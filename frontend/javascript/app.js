// URL base del backend FastAPI
const BASE_URL = "http://127.0.0.1:8000";

// Función helper para enviar POST
async function apiPost(endpoint, data) {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    return response.json();
}

// Función helper para enviar GET
async function apiGet(endpoint) {
    const response = await fetch(`${BASE_URL}${endpoint}`);
    return response.json();
}
