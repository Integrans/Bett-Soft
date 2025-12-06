// consultar.js

const API_BASE = "http://127.0.0.1:8000";

// Mapear id_estado -> texto y color de la etiqueta
function mapEstado(id_estado) {
  switch (id_estado) {
    case 1:
      return { texto: "Pendiente", clase: "bg-yellow-100 text-yellow-800" };
    case 2:
      return { texto: "En proceso", clase: "bg-blue-100 text-blue-800" };
    case 3:
      return { texto: "Resuelto", clase: "bg-green-100 text-green-800" };
    default:
      return { texto: "Sin estado", clase: "bg-slate-100 text-slate-600" };
  }
}

// Mapear sexo -> texto
function mapSexo(sexo) {
  if (!sexo) return "Sin especificar";

  const val = String(sexo).toLowerCase();
  if (val === "h" || val === "hombre" || val === "hombres") {
    return "Baño de hombres";
  }
  if (val === "m" || val === "mujer" || val === "mujeres") {
    return "Baño de mujeres";
  }
  if (val === "mixto") {
    return "Baño mixto";
  }
  return "Sin especificar";
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const inputFolio = document.getElementById("report-code");
  const mensajeEstado = document.getElementById("mensaje-estado");
  const contenedorResultado = document.getElementById("resultado-reporte");

  if (!form || !inputFolio || !mensajeEstado || !contenedorResultado) {
    console.error("No se encontraron elementos necesarios en consultar.html");
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // Evita recargar la página

    const folio = inputFolio.value.trim();
    if (!folio) {
      mensajeEstado.textContent =
        "Por favor ingresa un código de reporte / folio.";
      mensajeEstado.className = "text-sm text-red-600 mb-4";
      contenedorResultado.innerHTML = "";
      return;
    }

    mensajeEstado.textContent = "Buscando reporte...";
    mensajeEstado.className = "text-sm text-slate-500 mb-4";
    contenedorResultado.innerHTML = "";

    try {
      const resp = await fetch(
        `${API_BASE}/admin/reportes/${encodeURIComponent(folio)}`
      );

      if (resp.status === 404) {
        mensajeEstado.textContent =
          "No se encontró ningún reporte con ese folio.";
        mensajeEstado.className = "text-sm text-red-600 mb-4";
        contenedorResultado.innerHTML = "";
        return;
      }

      if (!resp.ok) {
        console.error("Error HTTP al consultar reporte:", resp.status);
        mensajeEstado.textContent =
          "Ocurrió un error al consultar el reporte. Intenta nuevamente.";
        mensajeEstado.className = "text-sm text-red-600 mb-4";
        return;
      }

      const data = await resp.json();
      console.log("Reporte recibido:", data);

      // ---- Tipo y ubicación ----
      const tipoTexto =
        data.tipo_reporte ||
        data.tipo ||
        data.tipo_problema ||
        "Sin especificar";

      const edificio = data.edificio || data.edificio_nombre || null;
      const ubicacionTexto = edificio
        ? `Edificio ${edificio}`
        : "Sin especificar";

      const fecha = data.fecha_creacion
        ? new Date(data.fecha_creacion).toLocaleDateString("es-MX", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
          })
        : "Sin fecha";

      const { texto: estadoTexto, clase: estadoClase } = mapEstado(
        data.id_estado
      );

      // ---- Sexo / género del baño ----
      const generoTexto = mapSexo(data.sexo);

      // ---- Pintar tarjeta ----
      mensajeEstado.textContent = "Resultado de la búsqueda:";
      mensajeEstado.className = "text-sm text-slate-600 mb-4";

      contenedorResultado.innerHTML = `
        <article class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
          <div class="p-5 sm:p-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h3 class="text-base sm:text-lg font-semibold text-slate-900">
                Reporte #${data.folio || folio}
              </h3>
              <p class="text-xs sm:text-sm text-slate-500 mt-1">
                Fecha: <span class="font-medium">${fecha}</span>
              </p>
            </div>
            <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${estadoClase}">
              ${estadoTexto}
            </span>
          </div>

          <div class="px-5 pb-5 sm:px-6 sm:pb-6 grid grid-cols-1 sm:grid-cols-3 gap-4 border-t border-slate-100">
            <div>
              <p class="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                Tipo
              </p>
              <p class="mt-1 text-sm text-slate-800">
                ${tipoTexto}
              </p>
            </div>
            <div>
              <p class="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                Ubicación
              </p>
              <p class="mt-1 text-sm text-slate-800">
                ${ubicacionTexto}
              </p>
            </div>
            <div>
              <p class="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                Género
              </p>
              <p class="mt-1 text-sm text-slate-800">
                ${generoTexto}
              </p>
            </div>
          </div>
        </article>
      `;
    } catch (err) {
      console.error("Error de conexión al servidor:", err);
      mensajeEstado.textContent =
        "No se pudo conectar con el servidor. Asegúrate de que el sistema está en funcionamiento.";
      mensajeEstado.className = "text-sm text-red-600 mb-4";
      contenedorResultado.innerHTML = "";
    }
  });
});
