# Dockerfile para backend FastAPI
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala dependencias
RUN pip install --no-cache-dir fastapi uvicorn
RUN pip install --no-cache-dir -r requirements.txt || true

# Expone el puerto de FastAPI
EXPOSE 8000

# Comando para iniciar el servidor
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
