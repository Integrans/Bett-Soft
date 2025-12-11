// ======================
// CONFIG
// ======================
const API_BASE = "http://127.0.0.1:8000";

// Lista de estados (debe coincidir con tu BD)
const ESTADOS = [
  { id: 1, label: "Pendiente",  badgeClasses: "bg-amber-100 text-amber-800" },
  { id: 2, label: "En proceso", badgeClasses: "bg-blue-100 text-blue-800" },
  { id: 3, label: "Resuelto",  badgeClasses: "bg-emerald-100 text-emerald-800" },
];

// ======================
// VARIABLES GLOBALES
// ======================
let allReportes = [];

// ======================
// UTILIDADES
// ======================
function getEstadoDef(idEstado) {
  return ESTADOS.find((e) => e.id === idEstado) || ESTADOS[0];
}

function formatearFecha(isoString) {
  if (!isoString) return "Sin fecha";
  const d = new Date(isoString);
  if (Number.isNaN(d.getTime())) return isoString;
  return d.toLocaleString("es-MX", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// Mapeo simple de tipo de problema (ajusta a tus valores reales)
function mapTipoReporte(tipo) {
  if (!tipo) return "Sin especificar";

  switch (tipo) {
    case "fuga":
      return "Fuga de agua";
    case "taza_tapada":
      return "Taza tapada";
    case "orinal_tapado":
      return "Orinal tapado";
    case "falta_papel":
      return "Falta de papel";
    case "falta_jabon":
      return "Falta de jabón";
    case "otro":
      return "Otro";
    default:
      return tipo;
  }
}

// ======================
// ACTUALIZAR ESTADO EN BACKEND
// ======================
async function actualizarEstado(folio, nuevoEstado) {
  try {
    const resp = await fetch(
      `${API_BASE}/admin/reportes/${encodeURIComponent(folio)}/estado`,
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_estado: nuevoEstado }),
      }
    );

    if (!resp.ok) {
      console.error(
        "Error al actualizar estado:",
        resp.status,
        await resp.text()
      );
      showToast("No se pudo actualizar el estado del reporte. Intenta nuevamente.", "error");
      return false;
    }

    return true;
    } catch (err) {
    console.error("Error de conexión al actualizar estado:", err);
    showToast(
      "Error de conexión con el servidor al actualizar estado. Verifica el backend.",
      "error"
    );
    return false;
  }
}

// ======================
// RENDER DE TARJETAS
// ======================
function renderReportes(lista) {
  const container = document.getElementById("reports-container");
  if (!container) {
    console.error(
      "No se encontró el contenedor #reports-container en admin.html"
    );
    return;
  }

  container.innerHTML = "";

  if (!lista || lista.length === 0) {
    container.innerHTML = `
      <p class="text-center text-slate-500 text-sm py-8">
        No hay reportes para mostrar. Ajusta los filtros o intenta de nuevo.
      </p>`;
    return;
  }

  lista.forEach((reporte) => {
    const estadoDef = getEstadoDef(reporte.id_estado);

    const card = document.createElement("article");
    card.className =
      "bg-white rounded-xl shadow-sm border border-slate-200 mb-4 overflow-hidden";

    const fecha = formatearFecha(reporte.fecha_creacion);
    const numeroCuenta = reporte.numero_cuenta || "Anónimo";
    const tipoNombre = mapTipoReporte(reporte.tipo_reporte);
    const edificio = reporte.edificio || "—";
    const ubicacionTexto = `Baño #${reporte.id_bano || "—"} • Edificio ${edificio}`;

    card.innerHTML = `
      <div class="px-6 py-4 flex items-center justify-between border-b border-slate-100">
        <div>
          <p class="text-xs text-slate-500">Reporte</p>
          <p class="font-semibold text-slate-900">#${reporte.folio}</p>
        </div>
        <div class="flex items-center gap-3" data-estado-wrapper>
          <span
            class="text-xs font-semibold px-3 py-1 rounded-full ${estadoDef.badgeClasses}"
            data-estado-label
          >
            ${estadoDef.label}
          </span>
        </div>
      </div>

      <div class="px-6 py-4 grid grid-cols-1 md:grid-cols-4 gap-4 text-sm text-slate-700">
        <div>
          <p class="text-xs font-medium text-slate-500">Fecha de reporte</p>
          <p class="mt-1">${fecha}</p>
        </div>
        <div>
          <p class="text-xs font-medium text-slate-500">Número de cuenta</p>
          <p class="mt-1">${numeroCuenta}</p>
        </div>
        <div>
          <p class="text-xs font-medium text-slate-500">Tipo de problema</p>
          <p class="mt-1">${tipoNombre}</p>
        </div>
        <div>
          <p class="text-xs font-medium text-slate-500">Ubicación</p>
          <p class="mt-1">${ubicacionTexto}</p>
        </div>
      </div>
    `;

    // Crear el <select> de estado dentro del wrapper
    const estadoWrapper = card.querySelector("[data-estado-wrapper]");
    const estadoLabel = card.querySelector("[data-estado-label]");

    const select = document.createElement("select");
    select.className =
      "text-xs border border-slate-300 rounded-md px-2 py-1 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500";
    select.setAttribute("aria-label", "Cambiar estado del reporte");

    ESTADOS.forEach((est) => {
      const opt = document.createElement("option");
      opt.value = String(est.id);
      opt.textContent = est.label;
      if (est.id === reporte.id_estado) opt.selected = true;
      select.appendChild(opt);
    });

    estadoWrapper.appendChild(select);

    // Evento de cambio de estado
    select.addEventListener("change", async (e) => {
      const nuevoIdEstado = Number(e.target.value);
      const prevIdEstado = reporte.id_estado;
      const prevDef = getEstadoDef(prevIdEstado);
      const nuevoDef = getEstadoDef(nuevoIdEstado);

      const ok = await actualizarEstado(reporte.folio, nuevoIdEstado);
      if (!ok) {
        // revertir visualmente
        e.target.value = String(prevIdEstado);
        return;
      }

      // actualizar en memoria
      reporte.id_estado = nuevoIdEstado;

      // actualizar badge visualmente
      estadoLabel.textContent = nuevoDef.label;
      estadoLabel.className =
        "text-xs font-semibold px-3 py-1 rounded-full " +
        nuevoDef.badgeClasses;
    });

    container.appendChild(card);
  });
}

// ======================
// FILTROS
// ======================
function aplicarFiltros() {
  const inputFolio = document.getElementById("buscar-folio");
  const selectEstado = document.getElementById("filtro-estado");
  const selectEdificio = document.getElementById("filtro-edificio");

  const folioTerm = (inputFolio?.value || "").trim().toLowerCase();
  const estadoTerm = selectEstado?.value || "todos";
  const edificioTerm = (selectEdificio?.value || "todos").toLowerCase();

  let lista = [...allReportes];

  if (folioTerm !== "") {
    lista = lista.filter((r) =>
      (r.folio || "").toLowerCase().includes(folioTerm)
    );
  }

  if (estadoTerm !== "todos") {
    const idEstado = Number(estadoTerm);
    lista = lista.filter((r) => r.id_estado === idEstado);
  }

  if (edificioTerm !== "todos") {
    lista = lista.filter(
      (r) => (r.edificio || "").toLowerCase() === edificioTerm
    );
  }

  renderReportes(lista);
}

// ======================
// CARGA INICIAL
// ======================
async function cargarReportes() {
  try {
    const resp = await fetch(`${API_BASE}/admin/reportes`);
      if (!resp.ok) {
      console.error("Error al cargar reportes:", resp.status, await resp.text());
      showToast("Ocurrió un error al cargar los reportes.", "error");
      return;
    }

    const data = await resp.json();
    allReportes = Array.isArray(data) ? data : [];

    aplicarFiltros();
    } catch (err) {
    console.error("Error de conexión al cargar reportes:", err);
    showToast(
      "No se pudo conectar con el servidor al cargar reportes. Verifica que el backend esté encendido.",
      "error"
    );
  }
}

// ======================
// INIT
// ======================
document.addEventListener("DOMContentLoaded", () => {
  // Filtros
  const inputFolio = document.getElementById("buscar-folio");
  const selectEstado = document.getElementById("filtro-estado");
  const selectEdificio = document.getElementById("filtro-edificio");
  const btnLimpiar = document.getElementById("btn-limpiar");

  if (inputFolio) {
    inputFolio.addEventListener("input", aplicarFiltros);
  }
  if (selectEstado) {
    selectEstado.addEventListener("change", aplicarFiltros);
  }
  if (selectEdificio) {
    selectEdificio.addEventListener("change", aplicarFiltros);
  }
  if (btnLimpiar) {
    btnLimpiar.addEventListener("click", () => {
      if (inputFolio) inputFolio.value = "";
      if (selectEstado) selectEstado.value = "todos";
      if (selectEdificio) selectEdificio.value = "todos";
      aplicarFiltros();
    });
  }

  // Cargar reportes del backend
  cargarReportes();
});
