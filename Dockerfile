# Используем официальный Python образ
FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry==1.8.2

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Настраиваем Poetry для работы в контейнере
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости
RUN poetry install --no-dev --no-interaction --no-ansi

# Копируем исходный код
COPY src/ ./src/
COPY photos/ ./photos/
COPY alembic.ini ./

# Создаем директорию для фотографий
RUN mkdir -p /app/photos

# Открываем порт
EXPOSE 8000

# Запускаем приложение через main.py
CMD ["python", "-m", "src.core.main"]