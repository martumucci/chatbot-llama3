# Usar la imagen oficial de Ollama como base
FROM ollama/ollama AS ollama_base

# Descargar el modelo `llama3` dentro del contenedor
RUN ollama pull llama3

# Imagen base con Python para la API
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que correrá FastAPI
EXPOSE 8000

# Configurar la variable de entorno para conectar con Ollama en Docker
ENV OLLAMA_HOST=http://ollama:11434

# Comando para ejecutar la API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
