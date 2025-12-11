# 🚀 Instalar y Levantar BettSoft con ngrok

ngrok es una herramienta que expone tu aplicación local a Internet de forma segura.

## 📋 Requisitos

- ✅ ngrok instalado
- ✅ Python 3.9+
- ✅ \ requirements.txt\ con todas las dependencias

---

## 🔧 Paso 0: Preparar Entorno Virtual

\\\powershell
cd Bett-Soft
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
\\\

---

## Paso 1: Levantar Backend (Terminal 1)

\\\powershell
cd backend\backend
python main.py
\\\

Verás: \INFO: Uvicorn running on http://127.0.0.1:8000\

---

## Paso 2: Crear Túnel ngrok (Terminal 2)

\\\powershell
ngrok http 8000
\\\

**Copia la URL** que aparece (ej: \https://abc123.ngrok-free.dev\ )

---

## Paso 3: Levantar Frontend (Terminal 3)

\\\powershell
cd frontend
python -m http.server 8080
\\\

---

## Paso 4: Configurar URL Backend

En navegador abre \http://localhost:8080\, luego en consola (F12):

\\\javascript

apiConfig.setApiUrl('https://abc123.ngrok-free.dev')// TuURL de ngrok

\\\

Recarga la página (F5).

---

## URLs Finales

| Uso | URL |
|-----|-----|
| Local | \http://localhost:8080\ |
| Público | \https://abc123.ngrok-free.dev\ |

---

## Compartir con Equipo

1. Ejecuta Pasos 0-4
2. Comparte tu URL de ngrok
3. ¡Listo! Tu equipo puede reportar

**Credenciales:**
- Email: \dmin@bettsoft.com\
- Contraseña: \dmin123\

---

## Quick Troubleshooting

- **Error de conexión:** \piConfig.setApiUrl('https://tu-url-ngrok'); location.reload()\
- **ngrok se cae:** Reinicia ngrok
- **Nueva URL cada reinicio:** Normal en plan gratuito

PARA IGNORAR WARNINGS de consola: allow pasting