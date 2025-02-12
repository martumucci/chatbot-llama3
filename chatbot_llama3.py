import ollama

# Lista para almacenar la conversación
conversation_history = []

def chat_with_llama3(prompt, model="llama3"):
    # Agregar la nueva pregunta al historial
    conversation_history.append({"role": "user", "content": prompt})

    # Llamar al modelo con todo el historial
    response = ollama.chat(model=model, messages=conversation_history)

    # Agregar la respuesta del modelo al historial
    conversation_history.append({"role": "assistant", "content": response["message"]["content"]})

    return response["message"]["content"]

# Chat interactivo
print("Chatbot con memoria activado. Escribe 'salir' para terminar.")
while True:
    user_input = input("Tú: ")
    if user_input.lower() in ["salir", "exit", "quit"]:
        print("Saliendo del chat...")
        break

    response = chat_with_llama3(user_input)
    print(f"Bot: {response}")
