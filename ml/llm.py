from llama_index.core import (
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)

from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

nest_asyncio.apply()


# documents = SimpleDirectoryReader("data", recursive=True).load_data()

# ollama
# Settings.embed_model = OllamaEmbedding(
#     base_url="http://127.0.0.1:11434",
#     model_name="nomic-embed-text",
# )
Settings.embed_model = OllamaEmbedding(
    base_url="http://127.0.0.1:11434",
    model_name="nomic-embed-text",
    # ollama_additional_kwargs={"mirostat": 0},
)

Settings.llm = Ollama(model="llama3", request_timeout=360.0)

# client = qdrant_client.QdrantClient(url="http://localhost:6333")
# aclient = qdrant_client.AsyncQdrantClient(host="localhost", port=6333)

# vector_store = QdrantVectorStore(client=client, aclient=aclient, collection_name="my_collection", enable_hybrid=True, batch_size=20)
# storage_context = StorageContext.from_defaults(vector_store=vector_store)

# splitter = SemanticSplitterNodeParser(embed_model=Settings.embed_model)
# nodes = splitter.get_nodes_from_documents(documents)
# Settings.chunk_size = 512

client = qdrant_client.QdrantClient()
aclient = qdrant_client.AsyncQdrantClient()

vector_store = QdrantVectorStore(
    collection_name="my_collection",
    client=client,
    aclient=aclient,
    enable_hybrid=True,
    batch_size=20,
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


@app.post("/api/llm/")
async def put_llm_ans(data: InputData):
    plus_context = f"Отвечай на русском: {data.question}"
    output = {"answer": str(await query_engine.aquery(plus_context))}
    return output


uvicorn.run(app, host="0.0.0.0", port=8009)
