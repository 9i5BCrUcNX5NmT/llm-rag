async def translate(first, second, text):
    from ollama import AsyncClient
    import os

    translate_model_name = os.environ.get("OLLAMA_TRANSLATE")

    message = {
        "role": "user",
        "content": f"Переведи следующий текст с {first} на {second}:\n{text}\n{second}:",
    }
    translate = await AsyncClient().chat(model=translate_model_name, messages=[message])

    return translate["message"]["content"]
