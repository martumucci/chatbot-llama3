# Etapa 1: Base con Ollama para descargar el modelo
FROM ollama/ollama AS ollama_base

# Descargar el modelo `llama3` dentro del contenedor de Ollama
RUN ollama pull llama3

# Etapa 2: API con FastAPI en Python
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Configurar PYTHONPATH para que FastAPI encuentre `app`
ENV PYTHONPATH=/app/src

# Configurar la variable de entorno para conectar con Ollama en Docker
ENV OLLAMA_HOST=http://ollama:11434

# Exponer el puerto en el que correrá FastAPI
EXPOSE 8000

# Comando para ejecutar la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
