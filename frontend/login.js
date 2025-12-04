const API_BASE = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const email = document.getElementById("email");
  const password = document.getElementById("password");
  const errorMsg = document.getElementById("error-msg");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorMsg.textContent = "";

    const data = {
      email: email.value.trim(),
      password: password.value.trim()
    };

    try {
      const response = await fetch(`${API_BASE}/admin/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        errorMsg.textContent = "Correo o contraseña incorrectos";
        return;
      }

      // ✅ Login correcto → ir al panel
      window.location.href = "admin.html";

    } catch (error) {
      console.error(error);
      errorMsg.textContent = "Error de conexión con el servidor";
    }
  });
});
