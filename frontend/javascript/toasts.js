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
        success: {
            bg: 'bg-emerald-50',
            border: 'border-l-4 border-emerald-500',
            text: 'text-emerald-900',
            icon: 'text-emerald-600',
            iconBg: 'bg-emerald-100'
        },
        error: {
            bg: 'bg-red-50',
            border: 'border-l-4 border-red-500',
            text: 'text-red-900',
            icon: 'text-red-600',
            iconBg: 'bg-red-100'
        },
        info: {
            bg: 'bg-blue-50',
            border: 'border-l-4 border-blue-500',
            text: 'text-blue-900',
            icon: 'text-blue-600',
            iconBg: 'bg-blue-100'
        }
    };

    const colors = colorMap[type] || colorMap.info;
    const toast = document.createElement('div');
    toast.className = `${colors.bg} ${colors.border} ${colors.text} px-5 py-4 rounded-md shadow-xl shadow-black/20 max-w-sm transform transition-all duration-300 backdrop-blur-sm border border-opacity-20 ${colors.border.split(' ')[1].split('-')[0] === 'border' ? '' : ''}`;
    toast.style.opacity = '0';
    toast.style.marginTop = '6px';
    toast.style.boxShadow = '0 10px 35px rgba(0, 0, 0, 0.15)';

    toast.innerHTML = `
        <div class="flex items-start gap-4">
            <div class="flex-shrink-0 ${colors.iconBg} rounded-full p-2.5 mt-0.5">
                <span class="material-icons text-lg ${colors.icon}">
                    ${type === 'success' ? 'check_circle' : type === 'error' ? 'error' : 'info'}
                </span>
            </div>
            <div class="flex-1">
                <p class="text-sm font-medium">${message}</p>
            </div>
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
