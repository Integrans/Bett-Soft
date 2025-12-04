const API_BASE = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ consultar.js cargado");

  const form = document.querySelector("form"); // tu form no tiene id
  const inputFolio = document.getElementById("report-code");
  const mensaje = document.getElementById("mensaje-estado");
  const contenedor = document.getElementById("resultado-reporte");

  if (!form || !inputFolio) {
    console.error("❌ No se encontró el formulario o el input");
    return;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const folio = inputFolio.value.trim();
    console.log("🔍 Folio ingresado:", folio);

    if (!folio) {
      mensaje.textContent = "Ingresa un folio válido.";
      contenedor.innerHTML = "";
      return;
    }

    mensaje.textContent = "Buscando reporte...";
    contenedor.innerHTML = "";

    try {
      const response = await fetch(`${API_BASE}/admin/reportes/${folio}`);
      console.log("📡 Status:", response.status);

      if (!response.ok) {
        mensaje.textContent = "Folio no encontrado.";
        return;
      }

      const data = await response.json();
      console.log("✅ Datos recibidos:", data);

      const estadoTexto =
        data.id_estado === 1 ? "Pendiente" :
        data.id_estado === 2 ? "En proceso" :
        "Resuelto";

      const ubicacion = `
        Edificio ${data.edificio || "-"},
        Piso ${data.nivel || "-"},
        ${data.sexo === "H" ? "Hombres" : data.sexo === "M" ? "Mujeres" : "Mixto"},
        ${data.pasillo || ""}
      `;

      contenedor.innerHTML = `
        <article class="bg-white rounded-xl p-6 shadow-md border border-slate-200">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-bold text-slate-800">
              Reporte #${data.folio}
            </h3>
            <span class="px-3 py-1 rounded-full text-sm bg-yellow-100 text-yellow-800">
              ${estadoTexto}
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm text-slate-700">
            <div>
              <strong>Fecha:</strong><br>
              ${data.fecha_creacion?.split("T")[0] || "-"}
            </div>
            <div>
              <strong>Tipo:</strong><br>
              ${data.tipo_reporte || "Sin especificar"}
            </div>
            <div>
              <strong>Ubicación:</strong><br>
              ${ubicacion}
            </div>
          </div>
        </article>
      `;

      mensaje.textContent = "Resultado de la búsqueda:";
    } catch (error) {
      console.error("❌ Error de conexión:", error);
      mensaje.textContent = "Error al conectar con el servidor.";
    }
  });
});
