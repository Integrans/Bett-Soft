// URL base del backend (FastAPI)
const API_BASE = "http://127.0.0.1:8000";
const REPORTES_PATH = "/reportes/";

document.addEventListener("DOMContentLoaded", () => {
  const btnMenu = document.getElementById("btn-menu");
  const menuMobile = document.getElementById("menu-mobile");
  const iconOpen = document.getElementById("icon-open");
  const iconClose = document.getElementById("icon-close");

  btnMenu.addEventListener("click", () => {
    const isHidden = menuMobile.classList.contains("hidden");

    menuMobile.classList.toggle("hidden");
    iconOpen.classList.toggle("hidden");
    iconClose.classList.toggle("hidden");
  });
});


// Esperar a que el DOM esté listo
document.addEventListener("DOMContentLoaded", () => {
  console.log("reportar.js cargado ✅");

  // Obtener el formulario
  const form = document.getElementById("form-reporte");
  if (!form) {
    console.error("No se encontró el formulario #form-reporte");
    return;
  }

  // Listener de envío
  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // evita que la página se recargue
    console.log("Submit capturado ✅");

    // ---------- Obtener valores del formulario ----------
    const tipoProblema = document.getElementById("tipo_problema").value;
    const edificio = document.getElementById("edificio").value;
    const nivel = parseInt(document.getElementById("nivel").value, 10);
    const sexo = document.getElementById("sexo").value;
    const pasillo = document.getElementById("pasillo").value;

    const tazaOrOrinalInput = document.querySelector(
      'input[name="taza_or_orinal"]:checked'
    );
    const tazaOrOrinal = tazaOrOrinalInput ? tazaOrOrinalInput.value : null;

    let numeroCuenta = document.getElementById("numero_cuenta").value.trim();
    const esAnonimo = document.getElementById("es_anonimo").checked;

    // Si es anónimo o no hay número de cuenta, mandamos "ANONIMO"
    if (esAnonimo || !numeroCuenta) {
      numeroCuenta = "ANONIMO";
    }

    // ---------- Construir payload ----------
    const data = {
      tipo_problema: tipoProblema,
      edificio: edificio,
      nivel: nivel,
      sexo: sexo,
      pasillo: pasillo,
      taza_o_orinal: tazaOrOrinal,
      numero_cuenta: numeroCuenta,
      es_anonimo: esAnonimo,
    };

    console.log("Payload a enviar:", data);

    // ---------- Enviar al backend ----------
    try {
      const response = await fetch(`${API_BASE}${REPORTES_PATH}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      console.log("Status backend:", response.status);

      let respuestaJson = null;
      try {
        respuestaJson = await response.json();
      } catch (_) {
        // por si el backend devuelve texto plano
      }
      console.log("Respuesta backend:", respuestaJson);

      if (!response.ok) {
      let mensajeError = "Error al enviar el reporte. Revisa la consola.";

      if (respuestaJson && respuestaJson.detail) {
        const detalle =
          typeof respuestaJson.detail === "string"
            ? respuestaJson.detail
            : JSON.stringify(respuestaJson.detail);

        if (detalle.toLowerCase().includes("baño no válido") ||
            detalle.toLowerCase().includes("baño no valido")) {
          mensajeError = "Baño no válido. Verifica el edificio y el baño seleccionados.";
        } else {
          mensajeError = detalle;
        }
      }

      showToast(mensajeError, "error");
      return;
    }


      const folio = respuestaJson?.folio || "SIN_FOLIO";
      showToast(`Reporte enviado correctamente. Folio: ${folio}`, "success");

      // Limpiar formulario
      form.reset();
    } catch (error) {
      console.error("Error de conexión:", error);
      showToast(
        "No se pudo conectar con el servidor. ¿Está corriendo en 127.0.0.1:8000?",
        "error"
      );
    }
  });
});
