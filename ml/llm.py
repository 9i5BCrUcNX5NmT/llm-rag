from llama_index.core import (
    Settings,
    VectorStoreIndex,
)

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
from pydantic import BaseModel
import uvicorn
from ollama import AsyncClient

nest_asyncio.apply()


# ollama
Settings.embed_model = OllamaEmbedding(
    base_url="http://127.0.0.1:11434",
    model_name="rjmalagon/gte-qwen2-1.5b-instruct-embed-f16",
    # ollama_additional_kwargs={"mirostat": 0},
)

Settings.llm = Ollama(
    base_url="http://127.0.0.1:11434", model="gemma2", request_timeout=360.0
)

client = qdrant_client.QdrantClient()
aclient = qdrant_client.AsyncQdrantClient()

# client.set_sparse_model(
#     embedding_model_name="Qdrant/bm42-all-minilm-l6-v2-attentions",
#     providers=["CUDAExecutionProvider"],
# )
# aclient.set_sparse_model(
#     embedding_model_name="Qdrant/bm42-all-minilm-l6-v2-attentions",
#     providers=["CUDAExecutionProvider"],
# )

vector_store = QdrantVectorStore(
    collection_name="Book",
    client=client,
    aclient=aclient,
    # enable_hybrid=True,
    # batch_size=20,
)

vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

# similarity_top_k=2, sparse_top_k=12
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


async def translate(first, second, text):
    message = {
        "role": "user",
        "content": f"translate the following text from {first} to {second}:\n{text}\nРусский:",
    }
    translate = await AsyncClient().chat(
        model="thinkverse/towerinstruct", messages=[message]
    )

    return translate["message"]["content"]


@app.post("/api/llm/")
async def put_llm_ans(data: InputData):
    # plus_context = f"{data.question} Ответ на русском:"
    # eng_data = await translate("Русский", "English", data.question)
    # print(eng_data)
    aquery = await query_engine.aquery(data.question)
    print(aquery)
    ru_answer = await translate("English", "Русский", str(aquery))

    output = {"answer": ru_answer}
    # output = {"answer": str(async query_engine.aquery(plus_context, ))}
    return output


uvicorn.run(app, host="0.0.0.0", port=8009)
