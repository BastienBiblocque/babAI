import chainlit as cl
import ollama

@cl.on_message
async def on_message(message: cl.Message):
    response = await call_ollama(cl.chat_context.to_openai(), message.content)
    await cl.Message(response).send()

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content=f"Début du chat...",
    ).send()

async def call_ollama(chat_history: list, user_message: str) -> str:
    try:
        chat_history.append({"role": "user", "content": user_message})

        stream = ollama.chat(
            model="llama3.1",
            messages=chat_history,
            stream=False,
        )

        full_response = stream.get("message", {}).get("content", "")

        return full_response

    except Exception as e:
        return f"Erreur lors de l'appel à Ollama : {str(e)}"