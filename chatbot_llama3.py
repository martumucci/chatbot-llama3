import ollama
import json
import os

# Nombre del archivo para guardar la conversación
HISTORY_FILE = "conversation_history.json"

def ensure_history_file():
    """Verifica si el archivo de historial existe, si no, lo crea con un JSON vacío."""
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)

def load_history():
    """Carga el historial desde un archivo JSON si el usuario lo permite."""
    ensure_history_file()

    user_choice = input("¿Quieres borrar el historial anterior? (sí/no): ").strip().lower()
    if user_choice in ["si", "sí", "s"]:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_history(history):
    """Guarda el historial en un archivo JSON."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)

def chat_with_llama3(prompt, model="llama3"):
    """Envía un mensaje al modelo con un prompt optimizado y el historial completo."""

    # Prompt mejorado con Role-Based Prompting + Chain of Thought
    enhanced_prompt = (
        "Actúa como un asistente experto en IA. Responde de manera clara y estructurada. "
        "Si el usuario hace una pregunta técnica, explica paso a paso. "
        "Si no entiendes algo, pide más información en lugar de adivinar. "
        "Pregunta del usuario: " + prompt
    )

    conversation_history.append({"role": "user", "content": enhanced_prompt})

    response = ollama.chat(model=model, messages=conversation_history)

    conversation_history.append({"role": "assistant", "content": response["message"]["content"]})

    # Guardar la conversación actualizada
    save_history(conversation_history)

    return response["message"]["content"]

# Cargar el historial al iniciar
conversation_history = load_history()

# Chat interactivo
print("Chatbot optimizado con Prompt Engineering activado. Escribe 'salir' para terminar.")
while True:
    user_input = input("Tú: ")
    if user_input.lower() in ["salir", "exit", "quit"]:
        print("Saliendo del chat y guardando la conversación...")
        break

    response = chat_with_llama3(user_input)
    print(f"Bot: {response}")
