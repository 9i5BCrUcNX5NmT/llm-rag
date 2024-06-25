from llama_index.core import SimpleDirectoryReader, Settings, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client

import nest_asyncio

nest_asyncio.apply()

documents = SimpleDirectoryReader("../data", recursive=True).load_data() 

base_url = "http://127.0.0.1:11434"
Settings.embed_model = OllamaEmbedding(
    base_url=base_url,
    model_name="nomic-embed-text",
)

# ollama
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

# client = qdrant_client.QdrantClient(url="http://localhost:6333")
aclient = qdrant_client.AsyncQdrantClient(host="localhost", port=6333)
vector_store = QdrantVectorStore(aclient=aclient, collection_name="my_collection")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

splitter = SemanticSplitterNodeParser(embed_model = Settings.embed_model)

# Раздиление документов на ноды
nodes = splitter.get_nodes_from_documents(documents)

# Добавление в qdrant
index = VectorStoreIndex(nodes=nodes, storage_context=storage_context, use_async=True)