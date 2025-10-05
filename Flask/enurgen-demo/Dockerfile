FROM python:3.10

WORKDIR /backend
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip poetry
RUN poetry install --no-root

CMD ["poetry", "run", "flask", "--app", "./src/server.py", "run", "-p", "5001", "--host", "0.0.0.0"]