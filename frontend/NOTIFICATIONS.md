# Sistema de Notificaciones (Toast)

## Descripción
Se ha implementado un sistema de notificaciones tipo **toast** que reemplaza los tradicionales `alert()`. Las notificaciones aparecen en la esquina superior derecha de la pantalla con estilos profesionales usando Tailwind CSS.

## Ubicación
- **Librería principal**: `frontend/javascript/toasts.js`
- **Función global**: `showToast(message, type, duration)`

## Uso

### Notificación de éxito
```javascript
showToast("Operación completada exitosamente", "success");
```

### Notificación de error
```javascript
showToast("Error al procesar la solicitud", "error");
```

### Notificación de información
```javascript
showToast("Esta es una notificación informativa", "info");
```

### Con duración personalizada (milisegundos)
```javascript
// Por defecto: 4000ms (4 segundos)
showToast("Este mensaje se mostrará por 2 segundos", "success", 2000);
```

## Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `message` | string | Texto del mensaje | Sí |
| `type` | string | `"success"`, `"error"` o `"info"` | No (default: `"success"`) |
| `duration` | number | Tiempo en milisegundos | No (default: `4000`) |

## Estilos

- **Success (Verde)**: `bg-green-600 text-white` ✓
- **Error (Rojo)**: `bg-red-600 text-white` ✗
- **Info (Gris oscuro)**: `bg-slate-700 text-white` ⓘ

## Integración en HTML

Para usar `showToast()` en cualquier página, incluye el archivo **antes** de tu script principal:

```html
<script src="./javascript/toasts.js"></script>
<script src="./javascript/mi-script.js"></script>
```

### Ejemplo en admin.html
```html
<script src="./javascript/toasts.js"></script>
<script src="./javascript/admin.js"></script>
```

## Páginas que utilizan toast

✅ `admin.html` - Descargas, cambio de estado, etc.
✅ `reportar.html` - Envío de reportes
✅ `consultar.html` - Búsqueda de reportes
✅ `login.html` - Inicio de sesión

## Ejemplos prácticos

### Descarga de archivo
```javascript
fetch('/api/descargar')
  .then(response => response.blob())
  .then(blob => {
    // Descargar archivo...
    showToast("Archivo descargado exitosamente", "success");
  })
  .catch(err => {
    showToast("Error al descargar el archivo", "error");
  });
```

### Validación de formulario
```javascript
if (!email || !password) {
  showToast("Por favor completa todos los campos", "info");
  return;
}
```

### API call fallido
```javascript
try {
  const response = await fetch('/api/data');
  if (!response.ok) {
    showToast("Error del servidor: " + response.status, "error");
    return;
  }
  showToast("Datos cargados correctamente", "success");
} catch (err) {
  showToast("No se pudo conectar con el servidor", "error");
}
```

## Características

- 🎨 Diseño responsivo con Tailwind CSS
- ⏱️ Desaparece automáticamente tras el tiempo especificado
- 🎯 Se apila automáticamente si hay múltiples notificaciones
- 🔔 Animación suave de entrada/salida
- 📱 Compatible con mobile y desktop
- ♿ Accesible con iconos Material Design

## Troubleshooting

### Las notificaciones no aparecen
1. Verifica que `toasts.js` se cargue **antes** de tu script
2. Abre la consola (F12) y comprueba que no hay errores
3. Asegúrate de que estés en una página con Tailwind CSS incluido

### El estilo se ve mal
- Comprueba que Tailwind CSS esté cargado en el HTML
- Los estilos dependen de Tailwind, no funcionarán sin él

### Necesito otro estilo de notificación
- Edita `toasts.js` y añade un nuevo tipo en `colorMap`:
  ```javascript
  const colorMap = {
    success: 'bg-green-600 text-white',
    error: 'bg-red-600 text-white',
    info: 'bg-slate-700 text-white',
    warning: 'bg-amber-600 text-white'  // Nuevo
  };
  ```
