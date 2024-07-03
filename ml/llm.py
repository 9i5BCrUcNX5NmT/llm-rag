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
import lib

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


@app.post("/api/llm/")
async def put_llm_ans(data: InputData):
    aquery = await query_engine.aquery(data.question)
    ru_answer = await lib.translate("English", "Русский", str(aquery))

    output = {"answer": ru_answer}
    return output


uvicorn.run(app, host="0.0.0.0", port=8009)
