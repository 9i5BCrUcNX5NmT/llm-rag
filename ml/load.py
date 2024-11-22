from llama_index.core import (
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    VectorStoreIndex,
)
import settings

settings.init()


# from llama_index.core.node_parser import SemanticSplitterNodeParser
# Settings.node_parser = SemanticSplitterNodeParser(embed_model=Settings.embed_model)
# nodes = parser.get_nodes_from_documents(documents)

# Проверяем наличие хранилища по имени
try:
    collection_info = settings.client.get_collection(collection_name="my_collection")
    print(f"Хранилище '{collection_info.name}' существует.")
except Exception as _:
    Settings.embed_model = settings.embed_model
    Settings.llm = settings.llm_model

    data_dir = "data"
    documents = SimpleDirectoryReader(data_dir, recursive=True).load_data(
        show_progress=True
    )

    storage_context = StorageContext.from_defaults(vector_store=settings.vector_store)

    # Добавление в qdrant
    vector_index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        show_progress=True,
        # use_async=True,
    )
