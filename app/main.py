"""
Описание приложения

Этот модуль запускает HTTP-сервер и выполняет периодические опросы базы данных.

Функции:
- start_querying: Запуск периодического опроса базы данных.
"""

import threading
import logging
from query_module import query_database
from web_module import run_server
import time
import os

# Параметры
QUERY_INTERVAL = int(os.getenv('QUERY_INTERVAL', 60))  # Время между опросами

def start_querying():
    logging.info("Запуск опроса базы данных.")
    while True:
        logging.info(f"Опрос базы данных.")
        query_database()
        logging.info(f"Ожидание следующего опроса... {QUERY_INTERVAL} секунд")
        time.sleep(QUERY_INTERVAL)

if __name__ == "__main__":
    # Настройка логирования
    logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Вывод логов в консоль (stdout)
    ]
)

    # Запускаем периодический опрос базы данных в отдельном потоке
    threading.Thread(target=start_querying, daemon=True).start()

    # Запускаем веб-сервер
    logging.info("Запуск HTTP-сервера...")
    run_server()



