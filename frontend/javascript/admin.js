document.addEventListener("DOMContentLoaded", async () => {

    // Mapeo de estados segun su número en la BD
    const mappingTextoNum = {
        1: "Pendiente",
        2: "En proceso",
        3: "Resuelto",
        4: "Descartado"
    };

    // Colores de etiquetas según estado
    const clasesEstado = {
        "Pendiente": "bg-slate-100 text-slate-800",
        "En proceso": "bg-yellow-100 text-yellow-800",
        "Resuelto": "bg-green-100 text-green-800",
        "Descartado": "bg-slate-300 text-slate-800"
    };

    // Formatear fecha
    function formatearFecha(fechaStr) {
        const fecha = new Date(fechaStr);
        return fecha.toLocaleDateString("es-ES");
    }

    // Formatear hora
    function formatearHora(fechaStr) {
        const fecha = new Date(fechaStr);
        return fecha.toLocaleTimeString("es-ES", { hour: '2-digit', minute: '2-digit' });
    }

    // =============================
    //   CARGAR LISTA DE REPORTES
    // =============================
    async function cargarReportes() {
        try {
            const response = await fetch("http://127.0.0.1:8000/reportes");
            if (!response.ok) throw new Error("No se pudieron cargar los reportes");

            const reportes = await response.json();
            console.log("Reportes cargados:", reportes);

            const contenedor = document.getElementById("lista-reportes");
            contenedor.innerHTML = "";

            reportes.forEach(rep => {

                const estadoTexto = mappingTextoNum[rep.id_estado] || "Pendiente";
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

    // Cargar reportes al abrir
    cargarReportes();
});


// =============================
//    CAMBIAR ESTADO REPORTE
// =============================
async function cambiarEstado(id_reporte, estadoTexto) {

    const estados = {
        "en_proceso": 2,
        "resuelto": 3,
        "descartado": 4
    };

    const nuevoEstado = estados[estadoTexto];

    try {
        const response = await fetch(`http://127.0.0.1:8000/reportes/${id_reporte}/estado-simple`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nuevo_estado: nuevoEstado })
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


// =============================
//      VER DETALLES (MODAL)
// =============================
async function verDetalles(folio) {
    try {
        const res = await fetch(`http://127.0.0.1:8000/reportes/folio/${folio}`);
        if (!res.ok) throw new Error("No se pudo cargar el reporte");

        const rep = await res.json();

        const modal = document.getElementById("modal-detalle");
        const cont = document.getElementById("contenido-detalle");

        cont.innerHTML = `
            <p><strong>Folio:</strong> ${rep.folio}</p>
            <p><strong>Problema:</strong> ${rep.tipo_reporte}</p>
            <p><strong>Edificio:</strong> ${rep.edificio}</p>
            <p><strong>Pasillo:</strong> ${rep.pasillo}</p>
            <p><strong>Sexo:</strong> ${rep.sexo}</p>
            <p><strong>Fecha:</strong> ${rep.fecha_creacion}</p>
            

            ${rep.imagen_url ? `<img src="${rep.imagen_url}" class="w-full rounded mt-2">` : ""}
        `;

        modal.classList.remove("hidden");

    } catch (err) {
        console.error(err);
        alert("Error al cargar detalles");
    }
}


// =============================
//          CERRAR MODAL
// =============================
function cerrarModal() {
    document.getElementById("modal-detalle").classList.add("hidden");
}
