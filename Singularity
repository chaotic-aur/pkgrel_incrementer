Bootstrap: docker
From: python:3.10-slim

%files
  pyproject.toml /app/
  poetry.lock /app/
  app.py /app/

%post
  pip install poetry
  poetry config virtualenvs.create false
  poetry install --no-cache --no-interaction --no-ansi --only main -C /app

%runscript
  export DATA_DIR="${DATA_DIR:-/data}"
  export PORT="${PORT:-15854}"
  cd /app
  exec uvicorn --port="$PORT" app:app
