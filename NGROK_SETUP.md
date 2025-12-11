# Publicar BettSoft con ngrok

## ¿Qué es ngrok?

ngrok es una herramienta que expone aplicaciones locales a Internet de manera segura. Crea un tunel desde tu computadora a un servidor ngrok, asignándote una URL pública (ej: `https://abc123.ngrok.io`).

## Requisitos

✅ ngrok instalado (ya tienes v3.24.0)
✅ Backend FastAPI corriendo en `http://127.0.0.1:8000`
✅ Frontend en una carpeta servida (Apache, nginx, servidor Python, etc.)

## Paso 1: Levantar el Backend

```bash
cd c:\Users\MVSarai\Repositorios\Bett-Soft\backend\backend
python main.py
```

O con uvicorn:
```bash
uvicorn main:app --reload
```

## Paso 2: Crear túnel ngrok para el Backend

En otra terminal PowerShell:

```bash
ngrok http 8000
```

**Salida esperada:**
```
Forwarding                    https://abc123-def456.ngrok.io -> http://localhost:8000
```

**⚠️ GUARDA ESTA URL** (ej: `https://abc123-def456.ngrok.io`)

## Paso 3: Servir el Frontend

### Opción A: Con Python (recomendado)

```bash
cd c:\Users\MVSarai\Repositorios\Bett-Soft\frontend
python -m http.server 8080
```

Accede a: `http://localhost:8080`

### Opción B: Con Node.js http-server

```bash
npm install -g http-server
cd c:\Users\MVSarai\Repositorios\Bett-Soft\frontend
http-server -p 8080
```

## Paso 4: Configurar la URL del API en el Frontend

### Opción 1: Automático (recomendado)

El sistema detecta automáticamente si estás en ngrok y usa la URL correcta. 

**Simplemente abre la consola (F12) y ejecuta:**
```javascript
apiConfig.setApiUrl('https://abc123-def456.ngrok.io')
```

### Opción 2: LocalStorage (persistente)

En la consola:
```javascript
localStorage.setItem('bettsoft_api_url', 'https://abc123-def456.ngrok.io')
location.reload()
```

### Opción 3: Editar config.js

Abre `frontend/javascript/config.js` y edita el método `detectAPIUrl()`:
```javascript
// Sección de Prioridad 4 (Default)
const defaultUrl = "https://abc123-def456.ngrok.io"; // Cambia esto
```

## Paso 5: Acceder a la Aplicación

1. Abre el navegador
2. Ve a `http://localhost:8080` (si usaste Python server)
3. Deberías ver el frontend cargando sin errores
4. Abre la consola (F12) y verifica:
   ```
   [BettSoft API] API URL: https://abc123-def456.ngrok.io
   ```

## Paso 6: Exponer el Frontend (Opcional)

Si también quieres compartir el frontend públicamente:

### Crear túnel ngrok para el Frontend

En una tercera terminal:
```bash
ngrok http 8080
```

Esto te dará una segunda URL (ej: `https://xyz789.ngrok.io`)

Comparte esta URL con otros usuarios para que accedan a tu aplicación.

## URLs Finales

- **Frontend público**: `https://xyz789.ngrok.io` (el que comparten otros)
- **Backend público**: `https://abc123-def456.ngrok.io` (el que usan los clientes)
- **Local frontend**: `http://localhost:8080` (para desarrollo)
- **Local backend**: `http://127.0.0.1:8000` (para desarrollo)

## Verificar Conexión

En la consola del navegador (F12), ejecuta:
```javascript
fetch(apiConfig.endpoint('/'))
  .then(r => r.json())
  .then(d => console.log('✅ Conectado:', d))
  .catch(e => console.error('❌ Error:', e))
```

## Troubleshooting

### "Error de conexión al cargar reportes"
- Verifica que ngrok esté corriendo
- Verifica que la URL en `apiConfig.getApiUrl()` sea correcta
- En la consola: `apiConfig.setApiUrl('https://tu-url-ngrok.ngrok.io')`

### "Error al descargar archivo"
- ngrok a veces tiene límites de descarga
- Intenta desde Incógnito
- Intenta recargar la página

### "CORS error"
- Abre la consola y busca errores de CORS
- El backend debe tener CORS configurado para ngrok
- En `backend/main.py`, verifica que CORSMiddleware permita ngrok

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ En producción, especifica los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### ngrok cae constantemente
- Verifica que tu backend esté corriendo sin errores
- Mira los logs de ngrok
- Reinicia ngrok

## Automatizar con Script

Crea `start-ngrok.ps1`:

```powershell
# start-ngrok.ps1
$backend = Start-Process python -ArgumentList "main.py" -WorkingDirectory "c:\Users\MVSarai\Repositorios\Bett-Soft\backend\backend" -PassThru
$frontend = Start-Process python -ArgumentList "-m http.server 8080" -WorkingDirectory "c:\Users\MVSarai\Repositorios\Bett-Soft\frontend" -PassThru

Start-Sleep -Seconds 2

ngrok http 8000 &
Start-Sleep -Seconds 1
ngrok http 8080

Write-Host "Backend PID: $($backend.Id)"
Write-Host "Frontend PID: $($frontend.Id)"
```

Ejecuta:
```bash
powershell -ExecutionPolicy Bypass -File .\start-ngrok.ps1
```

## Tips

- ngrok genera URLs diferentes cada vez que se reinicia (plan gratuito)
- ngrok Pro te da URLs fijas (permanentes)
- Las URLs ngrok tienen límite de ~40 conexiones por minuto (plan gratuito)
- ngrok es perfecto para testing, demos y compartir con otros
- Para producción, usa un servidor real (AWS, Azure, Heroku, etc.)

## Más Información

- ngrok docs: https://ngrok.com/docs
- Alternativas: localtunnel, serveo, Cloudflare Tunnel

---

¿Necesitas ayuda con ngrok o configuración adicional? 🚀
