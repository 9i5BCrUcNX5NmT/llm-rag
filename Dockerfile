FROM python:3.12

# Configure Poetry
ENV POETRY_VERSION=1.2.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN poetry install

# COPY data/ /data/

# Setup models
CMD [ "poetry", "run", "python", "ml/install_ollama_llm.py" ]

# Загрузка данных в векторную бд
CMD [ "poetry", "run", "python", "ml/load.py" ]
