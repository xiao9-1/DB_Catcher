# Используем базовый образ Python 3.11
FROM python:3.11-slim

# Устанавливаем зависимости
RUN pip install --no-cache-dir pyodbc Flask schedule

# Устанавливаем драйверы для MSSQL
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unixodbc-dev gcc g++ curl gnupg2 && \
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/microsoft.gpg && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Создаем директорию для приложения
WORKDIR /app

# Копируем код приложения в контейнер
COPY . /app

# Копируем папку с шаблонами в директорию приложения
COPY templates /app/templates

# Запускаем приложение
CMD ["python", "-u", "main.py"]


