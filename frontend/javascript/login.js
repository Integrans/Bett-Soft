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
            const response = await fetch("http://127.0.0.1:8000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const err = await response.json();
                alert("Error de inicio de sesión:\n" + err.detail);
                return;
            }

            const result = await response.json();
            console.log(result);

            alert(result.mensaje);

            // Redirigir al panel de admin
            window.location.href = "./admin.html";

        } catch (error) {
            console.error("Error al conectar:", error);
            alert("No se pudo conectar con el servidor.");
        }
    });
});
