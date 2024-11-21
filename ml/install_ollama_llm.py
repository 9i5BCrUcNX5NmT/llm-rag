from ollama import Client
import os

client = Client(host=os.environ.get("OLLAMA_URL"))


def not_pulled(name) -> bool:
    all([i["name"] == name for i in client.list()["models"]])


if not_pulled(os.environ.get("OLLAMA_LLM")):
    client.pull(os.environ.get("OLLAMA_LLM"))

if not_pulled(os.environ.get("OLLAMA_EMBEDDING")):
    client.pull(os.environ.get("OLLAMA_EMBEDDING"))

if not_pulled(os.environ.get("OLLAMA_TRANSLATE")):
    client.pull(os.environ.get("OLLAMA_TRANSLATE"))
