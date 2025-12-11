document.addEventListener("DOMContentLoaded", () => {
    console.log("login.js cargado");

    const form = document.querySelector("form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const data = {
            email: email,
            password: password
        };

        try {
            const response = await fetch(apiConfig.endpoint('/login'), {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const err = await response.json();
                showToast("Error de inicio de sesión: " + (err.detail || ""), "error");
                return;
            }

            const result = await response.json();
            console.log(result);

            showToast(result.mensaje || "Inicio de sesión exitoso", "success");

            // Redirigir al panel de admin
            window.location.href = "./admin.html";

        } catch (error) {
            console.error("Error al conectar:", error);
            showToast("No se pudo conectar con el servidor.", "error");
        }
    });
});
