# Репозиторий для хранения проекта ollama + llamaindex + qdrant + fastapi

## Запуск qdrant в docker
```bash
docker run -p 6333:6333 -p 6334:6334 -d --restart always -v ~/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

## TODO
- общие переменные
- rest api для загрузки файлов
- полная развёртка в docker