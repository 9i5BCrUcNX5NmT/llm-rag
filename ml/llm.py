from llama_index.core import (
    Settings,
    VectorStoreIndex,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
from pydantic import BaseModel
import uvicorn
import settings

settings.init()
nest_asyncio.apply()

Settings.embed_model = settings.embed_model
Settings.llm = settings.llm_model
vector_index = VectorStoreIndex.from_vector_store(vector_store=settings.vector_store)
query_engine = vector_index.as_query_engine()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InputData(BaseModel):
    question: str


# async def translate(first, second, text):
#     message = {
#         "role": "user",
#         "content": f"Переведи следующий текст с {first} на {second}:\n{text}\n",
#     }
#     translate = await AsyncClient().chat(
#         model="thinkverse/towerinstruct", messages=[message]
#     )

#     return translate["message"]["content"]


@app.post("/api/llm/")
async def put_llm_ans(data: InputData):
    # plus_context = f"{data.question} Ответ на русском:"
    # eng_data = await translate("Русский", "English", data.question)
    aquery = await query_engine.aquery(data.question)
    # ru_answer = await translate("English", "Русский", str(aquery))

    output = {"answer": str(aquery)}
    # output = {"answer": str(async query_engine.aquery(plus_context, ))}
    return output


uvicorn.run(app, host="0.0.0.0", port=8009)
