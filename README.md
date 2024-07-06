# Репозиторий для хранения проекта
## Стек
### Бекенд
- Ollama
- Llamaindex
- Qdrant
- Fastapi
### Фронтенд
- React
- Typescript
- Axios

## Установка
### Поддержка GPU вычислений
#### Nvidia
Ставим [cuda](https://developer.nvidia.com/cuda-toolkit)
#### AMD
Ставим ROCM
P.S. Поддержка ollama rocm пока в стадии разработки

### docker
#### Windows
Установка docker-desctop или docker в wsl
#### Linux
Установка docker

### Ollama
[Скачать](https://ollama.com/download)

Установить 3 используемые модели:
- llama3-chatqa - для ответов
- rjmalagon/gte-qwen2-1.5b-instruct-embed-f16 - для создания ембедингов
- thinkverse/towerinstruct - для перевода
P.S. при желании установка ollama в docker

### Запуск qdrant в docker
```bash
docker run -p 6333:6333 -p 6334:6334 -d --restart always -v ~/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

### 

## TODO
- общие переменные +
- rest api для загрузки файлов -
- полная развёртка в docker -
