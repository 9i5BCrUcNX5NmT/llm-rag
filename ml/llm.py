from llama_index.core import (
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    VectorStoreIndex,
)

# from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client

import nest_asyncio

nest_asyncio.apply()


documents = SimpleDirectoryReader("data", recursive=True).load_data()

Settings.embed_model = OllamaEmbedding(
    base_url="http://127.0.0.1:11434",
    model_name="nomic-embed-text",
)

# ollama
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

# client = qdrant_client.QdrantClient(url="http://localhost:6333")
aclient = qdrant_client.AsyncQdrantClient(host="localhost", port=6333)

# vector_store = QdrantVectorStore(client=client, aclient=aclient, collection_name="my_collection", enable_hybrid=True, batch_size=20)
# storage_context = StorageContext.from_defaults(vector_store=vector_store)

# splitter = SemanticSplitterNodeParser(embed_model = Settings.embed_model)

# Settings.chunk_size = 512

index = VectorStoreIndex(
    documents,
    vector_store=aclient,
    # use_async=True,
)

query_engine = index.as_query_engine()


from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI()

class InputData(BaseModel):
    question: str


@app.post("/api/llm/")
async def put_llm_ans(data: InputData):
    plus_context = f"Отвечай на русском: {data.question}"
    output = {"answer": str(await query_engine.aquery(plus_context))}
    return output


uvicorn.run(app, host="0.0.0.0", port=8009)
