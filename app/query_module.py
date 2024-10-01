"""
Описание модуля

Этот модуль отвечает за периодические опросы базы данных 
и предоставление информации через HTTP-сервер.

Функции:
- query_database: Опрос базы данных и сохранение данных в файл.
- save_to_file: Сохранение данных в CSV-файл.
- cleanup_old_files: Удаление неактуальных файлов.
"""

import os
import pyodbc
import csv
import time
import logging

# Настройки логирования
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Вывод логов в консоль (stdout)
    ]
)

# Настройки подключения к MSSQL (получаем из переменных окружения)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '1433')
DB_USER = os.getenv('DB_USER', 'sa')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'YourStrong!Passw0rd')
DB_NAME = os.getenv('DB_NAME', 'your_database')

# Директория для сохранения файлов (из переменных окружения)
DATA_DIR = os.getenv('DATA_DIR', './data')
# SQL-запрос, который будем выполнять (из переменных окружения)
QUERY = os.getenv('SQL_QUERY', 'SELECT * FROM your_table')

# Параметры
QUERY_INTERVAL = int(os.getenv('QUERY_INTERVAL', 60))  # Время между опросами
FILE_LIFETIME = int(os.getenv('FILE_LIFETIME', 600))  # Время жизни файлов

def query_database():
    try:
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_HOST},{DB_PORT};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD};"
        )
        
        # Используем with для автоматического закрытия соединения и курсора
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(QUERY)
                rows = cursor.fetchall()

                logging.info(f"Получено {len(rows)} строк(и) из базы данных.")

                if rows:
                    save_to_file(cursor, rows)

        cleanup_old_files()       

    except Exception as e:
        logging.error(f"Ошибка при опросе базы данных: {e}")
    

def save_to_file(cursor, rows):
    timestamp = int(time.time())
    filename = os.path.join(DATA_DIR, f"query_result_{timestamp}.csv")
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Получаем имена столбцов
        writer.writerow([column[0] for column in cursor.description])
        writer.writerows(rows)

    logging.info(f"Данные сохранены в файл: {filename}")

def cleanup_old_files():
    current_time = time.time()
    if os.path.exists(DATA_DIR):
        for filename in os.listdir(DATA_DIR):
            filepath = os.path.join(DATA_DIR, filename)
            if os.path.isfile(filepath) and (current_time - os.path.getmtime(filepath)) > FILE_LIFETIME:
                os.remove(filepath)
                logging.info(f"Удален старый файл: {filename}")


