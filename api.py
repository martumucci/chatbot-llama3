import ollama
import json
import os
from fastapi import FastAPI
from pydantic import BaseModel

# Nombre del archivo para guardar la conversación
HISTORY_FILE = "conversation_history.json"

# Configurar OLLAMA_HOST desde la variable de entorno (por defecto a localhost)
# OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
# os.environ["OLLAMA_HOST"] = OLLAMA_HOST  # Establecer la variable globalmente

app = FastAPI()

# Modelo de datos para recibir input del usuario
class ChatRequest(BaseModel):
    message: str

def ensure_history_file():
    """Verifica si el archivo de historial existe, si no, lo crea con un JSON vacío."""
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)

def load_history():
    """Carga el historial desde un archivo JSON."""
    ensure_history_file()
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_history(history):
    """Guarda el historial en un archivo JSON."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)

def chat_with_llama3(prompt, model="llama3"):
    """Envía un mensaje al modelo con el historial completo."""
    try:
        conversation_history.append({"role": "user", "content": prompt})

        # Llamada a Ollama sin 'host'
        response = ollama.chat(model=model, messages=conversation_history)

        conversation_history.append({"role": "assistant", "content": response["message"]["content"]})

        # Guardar la conversación actualizada
        save_history(conversation_history)

        return response["message"]["content"]

    except Exception as e:
        print(f"⚠️ Error en el chatbot: {str(e)}")
        return {"error": str(e)}

# Cargar historial al iniciar
conversation_history = load_history()

@app.get("/")
def home():
    return {"message": "API de Chatbot con FastAPI y Llama3 🚀"}

@app.post("/chat")
def chat(request: ChatRequest):
    """Endpoint para enviar mensajes al chatbot."""
    response = chat_with_llama3(request.message)
    return {"response": response}

@app.get("/history")
def get_history():
    """Endpoint para obtener el historial de la conversación."""
    return {"history": conversation_history}

@app.delete("/history")
def clear_history():
    """Endpoint para borrar el historial."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump([], file)
    global conversation_history
    conversation_history = []
    return {"message": "Historial borrado"}
