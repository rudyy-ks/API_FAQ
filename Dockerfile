# Используем официальный образ Python 3.11
FROM dh-mirror.gitverse.ru/library/python:3.11-slim


# Устанавливаем рабочую директорию
WORKDIR /app

RUN find /etc/apt/sources.list.d/ -type f -name "*.list" -exec sed -i 's/deb.debian.org/mirror.yandex.ru/g' {} + && \
    echo "deb http://mirror.yandex.ru/debian trixie main" > /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["sh", "-c", "\
    echo 'Waiting for PostgreSQL...' && \
    while ! pg_isready -h db -p 5432 -U user -d mydb; do \
        sleep 1; \
    done && \
    echo 'PostgreSQL is ready!' && \
    alembic revision --autogenerate -m 'Create questions table' && \
    alembic upgrade head || { echo 'Migration failed!'; exit 1; } && \
    echo 'Starting FastAPI...' && \
    uvicorn main:app --host 0.0.0.0 --port 8000 \
"]
