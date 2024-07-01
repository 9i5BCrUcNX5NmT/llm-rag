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

# import nest_asyncio

# nest_asyncio.apply()

ollama_url = "http://127.0.0.1:11434"
qdrant_url = "http://localhost:6333"
# qdrant_url = "opossum-accurate-chipmunk.ngrok-free.app"

# ollama

Settings.embed_model = OllamaEmbedding(
    base_url=ollama_url,
    model_name="all-minilm",
    # ollama_additional_kwargs={"mirostat": 0},
)

Settings.llm = Ollama(base_url=ollama_url, model="llama3", request_timeout=360.0)


documents = SimpleDirectoryReader("data\Книги", recursive=True).load_data(
    show_progress=True
)

Settings.node_parser = SemanticSplitterNodeParser(embed_model=Settings.embed_model)
# nodes = parser.get_nodes_from_documents(documents)


client = qdrant_client.QdrantClient(url=qdrant_url)
aclient = qdrant_client.AsyncQdrantClient(url=qdrant_url)


# client.set_model(
#     embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
#     providers=["CUDAExecutionProvider"],
# )
client.set_sparse_model(
    embedding_model_name="Qdrant/bm42-all-minilm-l6-v2-attentions",
    providers=["CUDAExecutionProvider"],
)
# aclient.set_model(
#     embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
#     providers=["CUDAExecutionProvider"],
# )
aclient.set_sparse_model(
    embedding_model_name="Qdrant/bm42-all-minilm-l6-v2-attentions",
    providers=["CUDAExecutionProvider"],
)


vector_store = QdrantVectorStore(
    collection_name="Book",
    client=client,
    aclient=aclient,
    # enable_hybrid=True,
    # batch_size=20,
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Добавление в qdrant
vector_index = VectorStoreIndex.from_documents(
    documents=documents,
    storage_context=storage_context,
    show_progress=True,
    # use_async=True,
)
