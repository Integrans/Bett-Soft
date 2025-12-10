document.addEventListener("DOMContentLoaded", () => {
  // =============================
  //   MAPEOS Y UTILIDADES
  // =============================

  const mapEdificioNombre = {
  "A1-A2": "Edificio A-1 / A-2",
  "A3-A4": "Edificio A-3 / A-4",
  "A5-A6": "Edificio A-5 / A-6",
  "A7-A8": "Edificio A-7 / A-8",
  "A9-A10": "Edificio A-9 / A-10",
  "A11-A12": "Edificio A-11 / A-12",
  Idiomas: "Idiomas (A-13 / A-14)",
  A15: "Edificio A-15",
  CEDETEC: "CEDETEC",
  Posgrado: "Posgrado",
  CEMM: "CEMM",
};

const prioridadLegible = {
    "PrioridadEnum.baja": "Baja",
    "PrioridadEnum.media": "Media",
    "PrioridadEnum.alta": "Alta"
};

function mostrarEdificio(code) {
  if (!code) return "-";
  return mapEdificioNombre[code] || code;
}

  // id_estado → texto
  const mappingTextoNum = {
    //1: "Pendiente",
    1: "En proceso",
    2: "Resuelto",
    3: "Descartado",
  };

  // Texto de estado → clases de Tailwind
  const clasesEstado = {
    Pendiente: "bg-slate-100 text-slate-800",
    "En proceso": "bg-yellow-100 text-yellow-800",
    Resuelto: "bg-green-100 text-green-800",
    Descartado: "bg-slate-300 text-slate-800",
  };

  // id_estado → valor del select
  function valorSelectEstado(id_estado) {
    switch (id_estado) {
      case 1:
        return "en_proceso";
      case 2:
        return "resuelto";
      case 3:
        return "descartado";
      default:
        return ""; // pendiente no tiene opción en el select
    }
  }

  // Tipo de problema “bonito”
  function mapTipoProblema(code) {
    if (!code) return "-";

    const map = {
      no_papel: "Falta de papel",
      taza_tapada: "WC tapado",
      fuga: "Fuga de agua",
      sanitario_sucio: "Sanitario sucio",
      orinal_tapado: "Mingitorio tapado",
      no_jabon: "Falta de jabón",
    };

    if (map[code]) return map[code];

    // fallback: "taza_tapada" → "Taza Tapada"
    return code
      .replace(/_/g, " ")
      .replace(/\b\w/g, (c) => c.toUpperCase());
  }

  function formatearFecha(fechaStr) {
    const f = new Date(fechaStr);
    return f.toLocaleDateString("es-ES");
  }

  function formatearHora(fechaStr) {
    const f = new Date(fechaStr);
    return f.toLocaleTimeString("es-ES", {
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  // Array con TODOS los reportes traídos del backend
  let todosReportes = [];

  // =============================
  //   RENDER DE TARJETAS
  // =============================
  function renderReportes(lista) {
    const contenedor = document.getElementById("lista-reportes");
    if (!contenedor) return;

    contenedor.innerHTML = "";

    if (!lista || lista.length === 0) {
      contenedor.innerHTML =
        '<p class="text-center text-slate-500 text-sm">No hay reportes para mostrar con los filtros actuales.</p>';
      return;
    }

    lista.forEach((rep) => {
      const estadoTexto = mappingTextoNum[rep.id_estado] || "Pendiente";
      const estadoClase = clasesEstado[estadoTexto];
      const tipoProblemaLegible = mapTipoProblema(rep.tipo_reporte);
      const valorSelect = valorSelectEstado(rep.id_estado);

      const item = `
        <article class="rounded-xl border border-slate-200 bg-white px-6 py-4 shadow-sm mb-4">
          <div class="flex flex-col gap-3">
            
            <!-- Fila superior: título + estado + dropdown -->
            <div class="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
              <div>
                <h2 class="text-base font-semibold text-slate-900">
                  Reporte #${rep.folio}
                </h2>
                <p class="text-xs text-slate-500">ID interno: ${rep.id_reporte}</p>
              </div>

              <div class="flex items-center gap-3 self-start md:self-auto">
                <span
                  class="inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ${estadoClase}"
                >
                  ${estadoTexto}
                </span>

                <!-- Select para cambiar estado -->
                <select
                  class="estado-select block w-28 rounded-full border border-slate-300 px-3 py-1 text-xs focus:border-blue-500 focus:ring-blue-500"
                  onchange="cambiarEstado(${rep.id_reporte}, this.value)"
                >
                  <option value="">Cambiar…</option>
                  <option value="en_proceso" ${
                    valorSelect === "en_proceso" ? "selected" : ""
                  }>En proceso</option>
                  <option value="resuelto" ${
                    valorSelect === "resuelto" ? "selected" : ""
                  }>Resuelto</option>
                  <option value="descartado" ${
                    valorSelect === "descartado" ? "selected" : ""
                  }>Descartado</option>
                </select>
              </div>
            </div>

            <!-- Detalles del reporte -->
            <div class="mt-2 grid gap-4 text-sm md:grid-cols-3">
              <div>
                <p class="font-medium text-slate-700">Fecha</p>
                <p class="text-slate-600">
                  ${formatearFecha(rep.fecha_creacion)} — ${formatearHora(
        rep.fecha_creacion
      )}
                </p>

                <p class="mt-3 font-medium text-slate-700">Prioridad</p>
                <p class="text-slate-600 capitalize">
                    ${prioridadLegible[rep.prioridad_asignada] || "-"}
                </p>

              </div>

              <div>
                <p class="font-medium text-slate-700">Tipo de problema</p>
                <p class="text-slate-600">${tipoProblemaLegible}</p>

                <p class="mt-3 font-medium text-slate-700">Número de cuenta</p>
                <p class="text-slate-600">${rep.numero_cuenta || "-"}</p>
              </div>

              <div>
                <p class="font-medium text-slate-700">Ubicación</p>
                <p class="text-slate-600">
                    ${mostrarEdificio(rep.edificio)}<br />
                    Género: ${rep.sexo || "-"}
                </p>


            <!-- Botón de ver detalles -->
            <div class="pt-3 flex justify-end">
              <button
                class="text-xs font-medium text-primary hover:underline"
                onclick="verDetalles('${rep.folio}')"
              >
                Ver detalles
              </button>
            </div>
          </div>
        </article>
      `;

      contenedor.innerHTML += item;
    });
  }

  // =============================
  //   FILTROS (folio/estado/edificio/fecha)
  // =============================
  function aplicarFiltros() {
    if (!todosReportes.length) {
      renderReportes([]);
      return;
    }

    const inputFolio = document.getElementById("search-folio");
    const selectEstado = document.getElementById("filter-estado");
    const selectEdificio = document.getElementById("filter-edificio");
    const selectFecha = document.getElementById("filter-fecha");

    const folioValue = inputFolio ? inputFolio.value.trim().toLowerCase() : "";
    const estadoValue = selectEstado ? selectEstado.value : "todos";
    const edificioValue = selectEdificio ? selectEdificio.value : "todos";
    const fechaValue = selectFecha ? selectFecha.value : "todas";

    // calculamos "desde" según la opción de fecha
    let desde = null;
    if (fechaValue === "hoy") {
      const hoy = new Date();
      hoy.setHours(0, 0, 0, 0);
      desde = hoy;
    } else if (fechaValue === "ultima_semana") {
      const d = new Date();
      d.setDate(d.getDate() - 7);
      d.setHours(0, 0, 0, 0);
      desde = d;
    } else if (fechaValue === "ultimo_mes") {
      const d = new Date();
      d.setMonth(d.getMonth() - 1);
      d.setHours(0, 0, 0, 0);
      desde = d;
    }

    let filtrados = todosReportes.filter((r) => {
      // folio
      if (folioValue && !r.folio.toLowerCase().includes(folioValue)) {
        return false;
      }

      // estado
      if (estadoValue !== "todos" && r.id_estado !== Number(estadoValue)) {
        return false;
      }

      // edificio
      if (edificioValue !== "todos" && r.edificio !== edificioValue) {
        return false;
      }

      // fecha mínima
      if (desde) {
        const fechaRep = new Date(r.fecha_creacion);
        if (fechaRep < desde) return false;
      }

      return true;
    });

    // ordenar del más reciente al más antiguo
    filtrados.sort(
      (a, b) =>
        new Date(b.fecha_creacion).getTime() -
        new Date(a.fecha_creacion).getTime()
    );

    renderReportes(filtrados);
  }

  // =============================
  //   PETICIONES AL BACKEND
  // =============================
  async function cargarReportes() {
    try {
      const res = await fetch("http://127.0.0.1:8000/reportes");
      if (!res.ok) throw new Error("No se pudieron cargar los reportes");

      todosReportes = await res.json();
      console.log("Reportes cargados:", todosReportes);
      aplicarFiltros();
    } catch (err) {
      console.error(err);
      const contenedor =
        document.getElementById("lista-reportes") ||
        document.getElementById("reports-container");
      if (contenedor) {
        contenedor.innerHTML =
          '<p class="text-center text-red-500 text-sm">Error al cargar reportes. Revisa el servidor.</p>';
      }
    }
  }

  // =============================
  //   EVENTOS DE FILTROS
  // =============================
  const inputFolio = document.getElementById("search-folio");
  const selectEstado = document.getElementById("filter-estado");
  const selectEdificio = document.getElementById("filter-edificio");
  const selectFecha = document.getElementById("filter-fecha");
  const btnLimpiar = document.getElementById("btn-limpiar-filtros");

  if (inputFolio) inputFolio.addEventListener("input", aplicarFiltros);
  if (selectEstado) selectEstado.addEventListener("change", aplicarFiltros);
  if (selectEdificio) selectEdificio.addEventListener("change", aplicarFiltros);
  if (selectFecha) selectFecha.addEventListener("change", aplicarFiltros);

  if (btnLimpiar) {
    btnLimpiar.addEventListener("click", () => {
      if (inputFolio) inputFolio.value = "";
      if (selectEstado) selectEstado.value = "todos";
      if (selectEdificio) selectEdificio.value = "todos";
      if (selectFecha) selectFecha.value = "todas";
      aplicarFiltros();
    });
  }

  // Cargar reportes al abrir
  cargarReportes();
});

// =============================
//    CAMBIAR ESTADO REPORTE
// =============================
async function cambiarEstado(id_reporte, estadoTexto) {
  if (!estadoTexto) return;

  const bodyData = { estado: estadoTexto };

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/reportes/${id_reporte}/estado-simple`,
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(bodyData),
      }
    );

    if (!response.ok) {
      const error = await response.text();
      console.error("Error al cambiar estado:", error);
      return;
    }

    console.log("Estado actualizado correctamente");
    location.reload();
  } catch (err) {
    console.error("Error en la solicitud:", err);
  }
}

// =============================
//      VER DETALLES (MODAL)
// =============================
async function verDetalles(folio) {
  try {
    const res = await fetch(
      `http://127.0.0.1:8000/reportes/folio/${folio}`
    );

    if (!res.ok) {
      const txt = await res.text();
      console.error("Error HTTP al obtener detalles:", res.status, txt);
      alert("Error al cargar detalles");
      return;
    }

    let data = await res.json();
    // Por si el backend regresa una lista en lugar de un solo objeto
    const rep = Array.isArray(data) ? data[0] : data;

    if (!rep) {
      console.error("No se encontró el reporte para el folio", folio);
      alert("No se encontró el reporte");
      return;
    }

    const modal = document.getElementById("modal-detalle");
    const cont = document.getElementById("contenido-detalle");
    if (!modal || !cont) {
      console.error("No se encontró el modal o el contenedor de detalles");
      return;
    }

    // Construir URL de imagen
    let imagenHTML = "";
    if (rep.imagen_url) {
      let imgUrl = rep.imagen_url;

      // Si no viene una URL absoluta, armamos una
      if (!imgUrl.startsWith("http")) {
        if (imgUrl.startsWith("uploads/")) {
          // Ya trae la carpeta
          imgUrl = `http://127.0.0.1:8000/${imgUrl}`;
        } else {
          // Solo guardaron el nombre del archivo
          imgUrl = `http://127.0.0.1:8000/uploads/${imgUrl}`;
        }
      }

      imagenHTML = `
        <div class="mt-4">
          <p class="font-medium text-slate-700 mb-1">Imagen adjunta:</p>
          <img
            src="${imgUrl}"
            alt="Imagen del reporte"
            class="w-full max-h-80 object-contain rounded-lg border border-slate-200 shadow-sm"
          />
        </div>
      `;
    }

    // Utilidad simple para el tipo de problema
    const tipoLegible = (code) => {
      if (!code) return "-";
      const map = {
        no_papel: "Falta de papel",
        taza_tapada: "WC tapado",
        fuga: "Fuga de agua",
        sanitario_sucio: "Sanitario sucio",
        orinal_tapado: "Mingitorio tapado",
        no_jabon: "Falta de jabón",
      };
      if (map[code]) return map[code];
      return code
        .replace(/_/g, " ")
        .replace(/\b\w/g, (c) => c.toUpperCase());
    };

    cont.innerHTML = `
      <p><strong>Folio:</strong> ${rep.folio}</p>
      <p><strong>Tipo de problema:</strong> ${tipoLegible(
        rep.tipo_reporte || rep.tipo_problema
      )}</p>
      <p><strong>Edificio:</strong> ${rep.edificio || "-"}</p>
      <p><strong>Baño:</strong> ${rep.sexo || "-"}</p>
      <p><strong>Fecha:</strong> ${rep.fecha_creacion || "-"}</p>
      <p><strong>Número de cuenta:</strong> ${
        rep.numero_cuenta || "ANONIMO"
      }</p>
      ${imagenHTML}
    `;

    modal.classList.remove("hidden");
  } catch (err) {
    console.error("Error al cargar detalles:", err);
    alert("Error al cargar detalles");
  }
}

// =============================
//          CERRAR MODAL
// =============================
function cerrarModal() {
  const modal = document.getElementById("modal-detalle");
  if (modal) modal.classList.add("hidden");
}