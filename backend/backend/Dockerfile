# 1. Usamos una versión ligera de Python
FROM python:3.9-slim

# 2. Creamos una carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Instalamos herramientas de sistema necesarias para MySQL
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config

# 4. Copiamos los requerimientos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo el código
COPY . .

# 6. El comando de arranque (escuchando en 0.0.0.0 para que sea público)
# Versión segura:
CMD uvicorn main:app --host 0.0.0.0 --port 8000