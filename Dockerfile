FROM python:3.12-slim

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
   libpq-dev gcc python3-dev && \
   apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы Poetry
COPY pyproject.toml /app/
COPY README.md /app/

# Настраиваем Poetry и устанавливаем зависимости
RUN poetry config virtualenvs.create false && \
   poetry install --no-interaction --no-ansi --no-root

# Копируем остальную часть приложения
COPY . /app/

ENV PYTHONDONTWRITEBYTECODE=1 \
   PYTHONUNBUFFERED=1 \
   DEBUG=False

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]