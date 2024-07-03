async def translate(first, second, text):
    from ollama import AsyncClient

    message = {
        "role": "user",
        "content": f"Переведи следующий текст с {first} на {second}:\n{text}\n",
    }
    translate = await AsyncClient().chat(
        model="thinkverse/towerinstruct", messages=[message]
    )

    return translate["message"]["content"]
