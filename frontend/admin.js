// URL base del backend
const API_BASE = "http://127.0.0.1:8000";

// Referencias a los elementos del DOM
const inputFolio = document.getElementById("filtro-folio");
const selectEstado = document.getElementById("filtro-estado");
const selectEdificio = document.getElementById("filtro-edificio");
const contenedorReportes = document.getElementById("contenedor-reportes");

// Aquí guardamos todos los reportes que vengan del backend
let TODOS_LOS_REPORTES = [];

// Mapeos simples para mostrar texto bonito
const ESTADOS_MAP = {
  1: "Pendiente",
  2: "En proceso",
  3: "Resuelto",
};

const PRIORIDAD_MAP = {
  alta: "Alta",
  media: "Media",
  baja: "Baja",
};

// 🟦 1. Cargar reportes al inicio
document.addEventListener("DOMContentLoaded", async () => {
  try {
    console.log("Cargando reportes desde el backend...");

    const resp = await fetch(`${API_BASE}/admin/reportes`);
    if (!resp.ok) {
      console.error("Error al obtener reportes:", resp.status);
      contenedorReportes.innerHTML =
        "<p class='text-center text-gray-500'>Error al cargar reportes.</p>";
      return;
    }

    const data = await resp.json();
    console.log("Reportes recibidos:", data);

    TODOS_LOS_REPORTES = data || [];
    renderizarReportes(TODOS_LOS_REPORTES);
  } catch (err) {
    console.error("Error de red al cargar reportes:", err);
    contenedorReportes.innerHTML =
      "<p class='text-center text-gray-500'>No se pudo conectar con el servidor.</p>";
  }
});

// 🟦 2. Listeners de filtros
[inputFolio, selectEstado, selectEdificio].forEach((el) => {
  if (!el) return;
  el.addEventListener("input", aplicarFiltros);
  el.addEventListener("change", aplicarFiltros);
});

// 🟦 3. Aplica filtros sobre TODOS_LOS_REPORTES
function aplicarFiltros() {
  let folio = (inputFolio?.value || "").trim();
  let estadoFiltro = selectEstado?.value || "";
  let edificioFiltro = selectEdificio?.value || "";

  let filtrados = TODOS_LOS_REPORTES.filter((rep) => {
    // Filtro por folio (coincidencia parcial)
    if (folio && !String(rep.folio).includes(folio)) {
      return false;
    }

    // Filtro por estado (id_estado numérico)
    if (estadoFiltro && String(rep.id_estado) !== estadoFiltro) {
      return false;
    }

    // Filtro por edificio
    // Si en la respuesta del backend viene `edificio`, lo usamos.
    // Si no viene, este filtro simplemente no excluye nada.
    if (edificioFiltro && rep.edificio && rep.edificio !== edificioFiltro) {
      return false;
    }

    return true;
  });

  renderizarReportes(filtrados);
}

// 🟦 4. Dibuja las tarjetas en el DOM
function renderizarReportes(lista) {
  if (!contenedorReportes) {
    console.error("No se encontró el contenedor de reportes en el HTML");
    return;
  }

  contenedorReportes.innerHTML = "";

  if (!lista || lista.length === 0) {
    contenedorReportes.innerHTML =
      "<p class='text-center text-gray-500'>No hay reportes para mostrar. Ajusta los filtros o intenta de nuevo.</p>";
    return;
  }

  lista.forEach((rep) => {
    const tarjeta = document.createElement("article");
    tarjeta.className =
      "bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex flex-col gap-3";

    const estadoTexto = ESTADOS_MAP[rep.id_estado] || "Desconocido";
    const prioridadTexto = PRIORIDAD_MAP[rep.prioridad_asignada] || rep.prioridad_asignada || "—";

    tarjeta.innerHTML = `
      <header class="flex items-center justify-between gap-4">
        <div>
          <p class="text-xs uppercase tracking-wide text-gray-400">Folio</p>
          <p class="font-semibold text-gray-900">#${rep.folio}</p>
        </div>
        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium
          ${rep.id_estado === 1 ? "bg-yellow-50 text-yellow-700" : ""}
          ${rep.id_estado === 2 ? "bg-blue-50 text-blue-700" : ""}
          ${rep.id_estado === 3 ? "bg-emerald-50 text-emerald-700" : ""}">
          ${estadoTexto}
        </span>
      </header>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600">
        <div>
          <p class="text-xs text-gray-400">Número de cuenta</p>
          <p class="font-medium">${rep.numero_cuenta || "Anónimo"}</p>
        </div>

        <div>
          <p class="text-xs text-gray-400">Baño</p>
          <p class="font-medium">ID baño: ${rep.id_bano}</p>
        </div>

        <div>
          <p class="text-xs text-gray-400">Categoría</p>
          <p class="font-medium">ID categoría: ${rep.id_categoria}</p>
        </div>

        <div>
          <p class="text-xs text-gray-400">Prioridad</p>
          <p class="font-medium capitalize">${prioridadTexto}</p>
        </div>
      </div>

      <footer class="flex items-center justify-between text-xs text-gray-400 mt-2">
        <span>Creado: ${rep.fecha_creacion || "—"}</span>
        <span>ID reporte: ${rep.id_reporte}</span>
      </footer>
    `;

    contenedorReportes.appendChild(tarjeta);
  });
}
