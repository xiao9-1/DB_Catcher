"""
Описание модуля

Этот модуль отвечает за предоставление информации через HTTP-сервер.

Функции:
- run_server: Запуск HTTP-сервера, который обрабатывает запросы.
- list_files: Отображение списка доступных файлов с активной ссылкой.
- show_file_content: Отображение содержимого выбранного файла.
- show_last_request_info: Показ информации о последнем HTTP-запросе.
"""

from flask import Flask, send_from_directory, render_template
import os
import time

app = Flask(__name__)

# Директория, где хранятся файлы
DATA_DIR = './data'

# Глобальная переменная для хранения информации о последнем запросе
last_request_info = {
    'type': None,
    'filename': None,
    'timestamp': None
}

# Функция для запуска сервера
def run_server():
    app.run(host='0.0.0.0', port=8090)

# Функция для обновления информации о последнем запросе
def update_last_request_info(req_type, filename):
    global last_request_info
    last_request_info['type'] = req_type
    last_request_info['filename'] = filename
    last_request_info['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')

# Route для отображения списка файлов
@app.route('/')
def list_files():
    files_with_time = [(filename, time.ctime(os.path.getctime(os.path.join(DATA_DIR, filename)))) for filename in os.listdir(DATA_DIR)]
    
    # Сортируем файлы по времени создания (от новых к старым)
    files_sorted = sorted(files_with_time, key=lambda x: x[1], reverse=True)
    
    # Передаем имена файлов и время создания в шаблон
    return render_template('file_list.html', files=files_sorted)

# Route для отображения содержимого файла
@app.route('/view/<filename>')
def show_file_content(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # Обновляем информацию о последнем запросе
    update_last_request_info('Просмотр файла', filename)
    
    return render_template('file_content.html', filename=filename, content=content)

# Route для скачивания файла
@app.route('/download/<filename>')
def download_file(filename):
    # Обновляем информацию о последнем запросе
    update_last_request_info('Скачивание файла', filename)
    
    return send_from_directory(DATA_DIR, filename, as_attachment=True)

# Route для отображения информации о последнем запросе
@app.route('/last_request_info')
def show_last_request_info():
    # Формируем строку с информацией о последнем запросе
    if last_request_info['type'] and last_request_info['filename'] and last_request_info['timestamp']:
        return (
            f"Последний запрос: {last_request_info['type']} файла '{last_request_info['filename']}' "
            f"в {last_request_info['timestamp']}"
        )
    else:
        return "Информация о последнем запросе отсутствует"

