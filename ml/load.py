from llama_index.core import (
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client

import nest_asyncio

nest_asyncio.apply()


# ollama
base_url = "http://127.0.0.1:11434"

Settings.embed_model = OllamaEmbedding(
    base_url=base_url,
    model_name="nomic-embed-text",
    # ollama_additional_kwargs={"mirostat": 0},
)

Settings.llm = Ollama(model="llama3", request_timeout=360.0)


documents = SimpleDirectoryReader("../data", recursive=True).load_data(
    show_progress=True
)

Settings.node_parser = SemanticSplitterNodeParser(embed_model=Settings.embed_model)
# nodes = parser.get_nodes_from_documents(documents)


client = qdrant_client.QdrantClient(url="http://localhost:6333")
aclient = qdrant_client.AsyncQdrantClient(host="localhost", port=6333)

vector_store = QdrantVectorStore(
    collection_name="test1",
    client=client,
    aclient=aclient,
    enable_hybrid=True,
    batch_size=20,
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Добавление в qdrant
vector_index = VectorStoreIndex.from_documents(
    documents=documents,
    storage_context=storage_context,
    show_progress=True,
    use_async=True,
)
