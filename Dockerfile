# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем зависимости для работы Poetry
RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev

# Копируем файлы Poetry
COPY poetry.lock pyproject.toml /app/

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Копируем код приложения
COPY . /app/

# Переходим в директорию приложения
WORKDIR /app

# Устанавливаем зависимости с помощью Poetry
RUN poetry install --no-dev

# Запускаем приложение
CMD ["poetry", "run", "start"]