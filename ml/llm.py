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


# documents = SimpleDirectoryReader("data", recursive=True).load_data()

# ollama
# Settings.embed_model = OllamaEmbedding(
#     base_url="http://127.0.0.1:11434",
#     model_name="nomic-embed-text",
# )
Settings.embed_model = OllamaEmbedding(
    base_url="http://127.0.0.1:11434",
    model_name="all-minilm",
    # ollama_additional_kwargs={"mirostat": 0},
)

Settings.llm = Ollama(
    base_url="http://127.0.0.1:11434", model="llama3", request_timeout=360.0
)

# client = qdrant_client.QdrantClient(url="http://localhost:6333")
# aclient = qdrant_client.AsyncQdrantClient(host="localhost", port=6333)

# vector_store = QdrantVectorStore(client=client, aclient=aclient, collection_name="my_collection", enable_hybrid=True, batch_size=20)
# storage_context = StorageContext.from_defaults(vector_store=vector_store)

# splitter = SemanticSplitterNodeParser(embed_model=Settings.embed_model)
# nodes = splitter.get_nodes_from_documents(documents)
# Settings.chunk_size = 512

client = qdrant_client.QdrantClient()
aclient = qdrant_client.AsyncQdrantClient()

client.set_sparse_model(
    embedding_model_name="Qdrant/bm42-all-minilm-l6-v2-attentions",
    providers=["CUDAExecutionProvider"],
)
aclient.set_sparse_model(
    embedding_model_name="Qdrant/bm42-all-minilm-l6-v2-attentions",
    providers=["CUDAExecutionProvider"],
)

vector_store = QdrantVectorStore(
    collection_name="Book",
    client=client,
    aclient=aclient,
    enable_hybrid=True,
    # batch_size=20,
)
# storage_context = StorageContext.from_defaults(vector_store=vector_store)

vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

# query_engine = index.as_query_engine()
query_engine = vector_index.as_query_engine(similarity_top_k=2, sparse_top_k=12)


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
