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

## Установка бекенда

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
- llama3 - для ответов
- rjmalagon/gte-qwen2-1.5b-instruct-embed-f16 - для создания ембедингов
- thinkverse/towerinstruct - для перевода
P.S. при желании установка ollama в docker

### Запуск qdrant в docker
```bash
docker run -p 6333:6333 -p 6334:6334 -d --restart always -v ~/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

### Poetry
Использовать мануал [poetry](https://python-poetry.org/docs/#installation)

## Комманды для запуска
### Бекенд
```bash
git clone https://github.com/9i5BCrUcNX5NmT/llm-rag
cd llm-rag
git submodule update --init
poetry shell
poetry install
mkdir data
```
Поместить в data файлы для загрузки
```bash
python ./ml/load.py
python ./ml/llm.py
```
Бекенд запущен
P.S. можно использовать ngrok для открытия туннеля к порту 8009 и соединить его с фронтом по адресу chat_ai/src/components/SendMessage.tsx(53 строчка)

## Установка фронтенда
[Репозиторий фронтенда](https://github.com/Aspir01/chat_ai)
### bun
Установить с [официального сайта](https://bun.sh/)
### Команды
```bash
cd chat_ai
bun install
```
#### Для запуска
```bash
bun run start
```
#### Для сборки установщика
```bash
bun run build
```

## TODO
- общие переменные +
- rest api для загрузки файлов -
- полная развёртка в docker -
