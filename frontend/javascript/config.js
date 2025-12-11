// =============================================
// CONFIGURACIÓN DINÁMICA DE URLs - BettSoft
// =============================================
//
// Este archivo gestiona la URL base del API
// Soporta:
// - Desarrollo local (127.0.0.1:8000)
// - ngrok (URL pública con dominio ngrok.io)
// - Producción (URL personalizada)
//
// =============================================

class APIConfig {
    constructor() {
        this.apiBaseUrl = this.detectAPIUrl();
        this.debug = true;
    }

    /**
     * Detecta automáticamente la URL del API según el entorno
     */
    detectAPIUrl() {
        // Prioridad 1: Variable en localStorage (permite cambio dinámico)
        const savedUrl = localStorage.getItem('bettsoft_api_url');
        if (savedUrl) {
            this.log("Usando URL del API desde localStorage:", savedUrl);
            return savedUrl;
        }

        // Prioridad 2: Variable global de window (para testing)
        if (window.BETTSOFT_API_URL) {
            this.log("Usando URL del API desde window.BETTSOFT_API_URL:", window.BETTSOFT_API_URL);
            return window.BETTSOFT_API_URL;
        }

        // Prioridad 3: Detectar ngrok desde el hostname
        if (window.location.hostname.includes('ngrok')) {
            // Si accedemos desde ngrok, usar la misma URL pero para el API
            const protocol = window.location.protocol;
            const hostname = window.location.hostname;
            const url = `${protocol}//${hostname}`;
            this.log("Detectado ngrok, usando URL:", url);
            return url;
        }

        // Prioridad 4: Default local
        const defaultUrl = "http://127.0.0.1:8000";
        this.log("Usando URL del API por defecto (local):", defaultUrl);
        return defaultUrl;
    }

    /**
     * Obtiene la URL base del API
     */
    getApiUrl() {
        return this.apiBaseUrl;
    }

    /**
     * Obtiene la URL de un endpoint específico
     */
    endpoint(path) {
        const baseUrl = this.getApiUrl();
        // Limpieza: remover trailing slash de baseUrl y leading slash de path
        const cleanBase = baseUrl.replace(/\/$/, '');
        const cleanPath = path.startsWith('/') ? path : `/${path}`;
        return `${cleanBase}${cleanPath}`;
    }

    /**
     * Cambia la URL del API dinámicamente
     * Útil para testing o configuración manual
     */
    setApiUrl(url) {
        this.apiBaseUrl = url;
        localStorage.setItem('bettsoft_api_url', url);
        this.log("URL del API actualizada a:", url);
    }

    /**
     * Reinicia a la URL por defecto
     */
    resetApiUrl() {
        localStorage.removeItem('bettsoft_api_url');
        this.apiBaseUrl = this.detectAPIUrl();
        this.log("URL del API reiniciada");
    }

    /**
     * Muestra información en consola (solo si debug está habilitado)
     */
    log(...args) {
        if (this.debug) {
            console.log('[BettSoft API]', ...args);
        }
    }

    /**
     * Getter para acceso rápido
     */
    get baseUrl() {
        return this.getApiUrl();
    }
}

// Instancia global
const apiConfig = new APIConfig();

// Exportar para módulos (si los hay)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = apiConfig;
}

// Debug: mostrar URL actual en consola
console.log('%c[BettSoft]', 'color: #003366; font-weight: bold', 'API URL:', apiConfig.getApiUrl());
