// Reusable toast notifications
function showToast(message, type = "success", duration = 4000) {
    // Crear contenedor si no existe
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'fixed top-6 right-6 z-50 flex flex-col gap-3 items-end';
        document.body.appendChild(container);
    }

    const colorMap = {
        success: 'bg-green-600 text-white',
        error: 'bg-red-600 text-white',
        info: 'bg-slate-700 text-white'
    };

    const toast = document.createElement('div');
    toast.className = `${colorMap[type] || colorMap.info} px-4 py-2 rounded-lg shadow-lg max-w-xs transform transition-all duration-300`;
    toast.style.opacity = '0';
    toast.style.marginTop = '6px';

    toast.innerHTML = `
        <div class="flex items-center gap-3">
            <div class="flex-shrink-0">
                ${type === 'success' ? '<span class="material-icons">check_circle</span>' : '<span class="material-icons">error</span>'}
            </div>
            <div class="text-sm">${message}</div>
        </div>
    `;

    container.appendChild(toast);

    // force reflow then show
    requestAnimationFrame(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    });

    // Remover después del tiempo
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-10px)';
        setTimeout(() => {
            if (toast && toast.parentNode) toast.parentNode.removeChild(toast);
        }, 300);
    }, duration);
}

// Export for older modules (optional)
window.showToast = showToast;
