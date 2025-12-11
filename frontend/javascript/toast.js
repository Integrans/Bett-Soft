// toast.js
console.log("toast.js cargado correctamente");

const TOAST_TYPES = {
  success: {
    bg: "bg-emerald-600",
    border: "border-emerald-500",
    icon: "✔️",
    srLabel: "Éxito"
  },
  error: {
    bg: "bg-red-600",
    border: "border-red-500",
    icon: "❗",
    srLabel: "Error"
  },
  warning: {
    bg: "bg-amber-500",
    border: "border-amber-400",
    icon: "⚠️",
    srLabel: "Advertencia"
  },
  info: {
    bg: "bg-sky-600",
    border: "border-sky-500",
    icon: "ℹ️",
    srLabel: "Información"
  }
};

// Crea el contenedor superior centrado si no existe
function getToastRoot() {
  let root = document.getElementById("toast-root");
  if (!root) {
    root = document.createElement("div");
    root.id = "toast-root";
    root.className = "fixed inset-x-0 top-4 flex justify-center z-50 pointer-events-none";
    document.body.appendChild(root);
  }
  return root;
}

/**
 * Muestra un toast
 * @param {string} message  Texto del mensaje
 * @param {"success"|"error"|"warning"|"info"} type  Tipo de toast
 * @param {number} duration  Tiempo en ms antes de que se oculte (por defecto 4000)
 */
function showToast(message, type = "info", duration = 4000) {
  const config = TOAST_TYPES[type] || TOAST_TYPES.info;
  const root = getToastRoot();

  // Contenedor del toast
  const wrapper = document.createElement("div");
  wrapper.className =
    "pointer-events-auto w-full max-w-sm mx-2 transition-all duration-300 transform opacity-0 -translate-y-4";

  // Tarjeta del toast
  const toast = document.createElement("div");
  toast.className = [
    "rounded-lg shadow-lg border",
    config.bg,
    config.border,
    "text-white px-4 py-3 flex items-start gap-3"
  ].join(" ");

    // Icono más visible
  const iconSpan = document.createElement("span");
  iconSpan.className = `
    flex items-center justify-center
    h-7 w-7 rounded-full border border-white/40
    bg-white/15 text-base mt-0.5
  `;
  iconSpan.textContent = config.icon;

  // Texto
  const textContainer = document.createElement("div");
  textContainer.className = "flex-1 text-sm";

  const sr = document.createElement("span");
  sr.className = "sr-only";
  sr.textContent = config.srLabel + ": ";

  const msgSpan = document.createElement("span");
  msgSpan.textContent = message;

  textContainer.appendChild(sr);
  textContainer.appendChild(msgSpan);

  // Botón de cerrar
  const closeBtn = document.createElement("button");
  closeBtn.type = "button";
  closeBtn.className =
    "ml-2 text-white/80 hover:text-white focus:outline-none text-sm font-bold";
  closeBtn.textContent = "✖";

  // Ensamblar
  toast.appendChild(iconSpan);
  toast.appendChild(textContainer);
  toast.appendChild(closeBtn);
  wrapper.appendChild(toast);
  root.appendChild(wrapper);

  // Animación de entrada
  requestAnimationFrame(() => {
    wrapper.classList.remove("opacity-0", "-translate-y-4");
    wrapper.classList.add("opacity-100", "translate-y-0");
  });

  // Cerrar manualmente
  function removeToast() {
    wrapper.classList.remove("opacity-100", "translate-y-0");
    wrapper.classList.add("opacity-0", "-translate-y-4");
    setTimeout(() => {
      wrapper.remove();
    }, 250);
  }

  closeBtn.addEventListener("click", removeToast);

  // Auto–cerrado
  const timeoutId = setTimeout(removeToast, duration);

  // Por si en un futuro necesitas cancelar desde fuera:
  return {
    close: () => {
      clearTimeout(timeoutId);
      removeToast();
    }
  };
}