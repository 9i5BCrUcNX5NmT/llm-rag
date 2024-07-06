def init():
    import os

    # vars
    ollama_url = (
        "http://localhost:11434"
        if not os.environ.get("OLLAMA_URL")
        else os.environ.get("OLLAMA_URL")
    )
    qdrant_url = (
        "http://localhost:6333"
        if not os.environ.get("QDRANT_URL")
        else os.environ.get("QDRANT_URL")
    )
    # qdrant_url = "opossum-accurate-chipmunk.ngrok-free.app"
    collection_name = "Hack"
    llm_model_name = "llama3"
    embed_model_name = "rjmalagon/gte-qwen2-1.5b-instruct-embed-f16"

    global embed_model, llm_model, vector_store

    # ollama
    from llama_index.embeddings.ollama import OllamaEmbedding
    from llama_index.llms.ollama import Ollama

    embed_model = OllamaEmbedding(
        base_url=ollama_url,
        model_name=embed_model_name,
        # ollama_additional_kwargs={"mirostat": 0},
    )
    llm_model = Ollama(base_url=ollama_url, model=llm_model_name, request_timeout=360.0)

    # qdrant
    from llama_index.vector_stores.qdrant import QdrantVectorStore
    import qdrant_client

    client = qdrant_client.QdrantClient(url=qdrant_url)
    aclient = qdrant_client.AsyncQdrantClient(url=qdrant_url)

    # connection
    vector_store = QdrantVectorStore(
        collection_name=collection_name,
        client=client,
        aclient=aclient,
    )
