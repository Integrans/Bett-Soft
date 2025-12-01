document.addEventListener("DOMContentLoaded", async () => {

    // Mapeo entre estados de BD -> texto visible
    const mappingTexto = {
        "pendiente": "Pendiente",
        "en_proceso": "En proceso",
        "resuelto": "Resuelto",
        "descartado": "Descartado"
    };

    // Colores de etiquetas según estado
    const clasesEstado = {
        "Pendiente": "bg-slate-100 text-slate-800",
        "En proceso": "bg-yellow-100 text-yellow-800",
        "Resuelto": "bg-green-100 text-green-800",
        "Descartado": "bg-slate-300 text-slate-800"
    };

    // Formatear fecha "YYYY-MM-DDTHH:MM:SS" a DD/MM/YYYY
    function formatearFecha(fechaStr) {
        const fecha = new Date(fechaStr);
        return fecha.toLocaleDateString("es-ES");
    }

    // Formatear hora HH:MM:SS a HH:MM
    function formatearHora(fechaStr) {
        const fecha = new Date(fechaStr);
        return fecha.toLocaleTimeString("es-ES", { hour: '2-digit', minute: '2-digit' });
    }

    async function cargarReportes() {
        try {
            const response = await fetch("http://127.0.0.1:8000/reportes");
            if (!response.ok) throw new Error("No se pudieron cargar los reportes");

            const reportes = await response.json();
            console.log("Reportes cargados:", reportes);

            const contenedor = document.getElementById("lista-reportes");
            contenedor.innerHTML = "";

            reportes.forEach(rep => {

                const estadoEnum = Object.keys(mappingTexto).find(key => mappingTexto[key] === mappingTexto[rep.id_estado] || mappingTexto[key] === mappingTexto[rep.id_estado]);
                const estadoTexto = mappingTexto[rep.id_estado] || mappingTexto["pendiente"];
                const estadoClase = clasesEstado[estadoTexto];

                const item = `
                <article class="bg-white rounded-lg shadow-sm overflow-hidden">

                    <header class="p-4 border-b border-slate-200 flex justify-between items-center">
                        <h2 class="font-semibold text-slate-900">
                            Reporte ${rep.folio}
                        </h2>
                        <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${estadoClase}">
                            ${estadoTexto}
                        </span>
                    </header>

                    <div class="p-4 grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
                        <div>
                            <p class="font-medium text-slate-500">Fecha</p>
                            <p>${formatearFecha(rep.fecha_creacion)}</p>
                        </div>

                        <div>
                            <p class="font-medium text-slate-500">Hora</p>
                            <p>${formatearHora(rep.fecha_creacion)}</p>
                        </div>

                        <div>
                            <p class="font-medium text-slate-500">Problema</p>
                            <p>${rep.tipo_reporte}</p>
                        </div>

                        <div>
                            <p class="font-medium text-slate-500">Ubicación</p>
                            <p>${rep.edificio}, ${rep.sexo}</p>
                        </div>
                    </div>

                    <footer class="px-4 py-3 bg-slate-50 flex justify-between items-center text-sm">
                        <button class="font-medium text-primary hover:underline" onclick="verDetalles('${rep.folio}')">
                            Ver detalles
                        </button>

                        <div class="flex items-center gap-2">
                            <button onclick="cambiarEstado(${rep.id_reporte}, 'en_proceso')"
                                class="px-2 py-1 rounded bg-yellow-200 text-yellow-800 hover:bg-yellow-300 text-xs">
                                En proceso
                            </button>

                            <button onclick="cambiarEstado(${rep.id_reporte}, 'resuelto')"
                                class="px-2 py-1 rounded bg-green-200 text-green-800 hover:bg-green-300 text-xs">
                                Resuelto
                            </button>

                            <button onclick="cambiarEstado(${rep.id_reporte}, 'descartado')"
                                class="px-2 py-1 rounded bg-slate-200 text-slate-800 hover:bg-slate-300 text-xs">
                                Descartado
                            </button>
                        </div>
                    </footer>
                </article>
                `;

                contenedor.innerHTML += item;
            });

        } catch (err) {
            console.error(err);
            alert("Error al cargar reportes");
        }
    }

    // Cargar reportes al abrir la página
    cargarReportes();
});

// --- Cambiar estado ---
async function cambiarEstado(id_reporte, estado) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/reportes/${id_reporte}/estado-simple`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ estado }) // debe ser string exacto: "en_proceso", "resuelto", "descartado"
        });

        if (!response.ok) {
            const text = await response.text();
            console.error("Error response:", text);
            alert("Error al cambiar estado");
            return;
        }

        alert("Estado actualizado correctamente");
        location.reload();

    } catch (err) {
        console.error(err);
        alert("Error en la solicitud");
    }
}

// --- Ver detalles ---
function verDetalles(folio) {
    window.location.href = `detalle.html?folio=${folio}`;
}
