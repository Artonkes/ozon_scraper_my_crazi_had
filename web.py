import asyncio
import os
import time
import json
import uuid
from flask import Flask, render_template, request, redirect, url_for, jsonify
from main import main
import concurrent.futures
from functions import sort_products

app = Flask('Deshovka')

# Создаем пул потоков
executor = concurrent.futures.ThreadPoolExecutor()


# Функция для генерации уникального ID пользователя
def generate_user_id():
    return str(uuid.uuid4())


# Функция для сохранения запроса в отдельный JSON файл
def save_request_data(user_id, pars_inp, scrolls):
    request_data = {
        "user_id": user_id,
        "input_value": pars_inp,
        "scrolls": scrolls,
        "timestamp": time.time()
    }
    # Сохраняем запрос в файл с уникальным именем
    file_name = f"{user_id}_{int(time.time())}_запрос.json"
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(request_data, f, ensure_ascii=False, indent=4)


# Функция для получения последнего запроса пользователя
def get_last_user_request(user_id):
    # Ищем все файлы с запросами этого пользователя
    user_requests = []
    for file_name in os.listdir():
        if file_name.startswith(user_id) and file_name.endswith('_запрос.json'):
            with open(file_name, 'r', encoding='utf-8') as f:
                user_requests.append(json.load(f))

    if user_requests:
        # Сортируем запросы по времени (timestamp), чтобы выбрать последний
        user_requests.sort(key=lambda x: x['timestamp'], reverse=True)
        return user_requests[0]  # Возвращаем самый последний запрос
    return None


# Обновленная асинхронная задача
def run_async_task(pars_inp, scrolls, user_id):
    # Сохраняем данные запроса в файл
    save_request_data(user_id, pars_inp, scrolls)
    # Запускаем асинхронную задачу в фоновом потоке
    asyncio.run(main(pars_inp=pars_inp, scrolls=5, user_id=user_id))


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        input_value = request.form.get("input")
        min_price = request.form.get("min_price")
        max_price = request.form.get("max_price")
        min_rating = request.form.get("min_rating")
        max_rating = request.form.get("max_rating")

        # Обработка ошибок (важно!)
        if input_value is None or len(input_value) == 0:
            return render_template("home.html")  # Или перенаправление на страницу ошибки

        # Генерируем уникальный ID для пользователя
        user_id = generate_user_id()

        # Запускаем асинхронную задачу в фоновом потоке
        executor.submit(run_async_task, input_value, 5, user_id)

        # Перенаправление на страницу с продуктами сразу
        return redirect(
            url_for(
                'products', 
                user_id=user_id, 
                min_price=min_price, 
                max_price=max_price, 
                min_rating=min_rating,
                max_rating=max_rating
            )
        )
    else:
        return render_template("home.html")

@app.route('/products', methods=["GET", "POST"])
def products():
    # Получаем ID пользователя из параметров запроса
    user_id = request.args.get('user_id')

    # Получаем параметры фильтрации из запроса
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', type=float)
    max_rating = request.args.get('max_rating', type=float)

    if user_id:
        # Получаем последний запрос пользователя
        last_request = get_last_user_request(user_id)

        if last_request:
            # Проверяем наличие файла перед его загрузкой
            file_path = f'{user_id}_PRODUCTS_DATA.json'
            sorted_file_path = f'{user_id}_SORTED_PRODUCTS_DATA.json'
            time.sleep(5)

            while not os.path.exists(file_path):
                # Если файл не найден, ожидаем 1 секунду перед повторной проверкой
                time.sleep(10)

            # Когда файл найден, загружаем данные и сортируем их
            sort_products(
                min_price=min_price,
                max_price=max_price,
                min_rating=min_rating,
                max_rating=max_rating,
                input_file=file_path,
                output_file=sorted_file_path
                )
              

            # Загружаем отсортированные данные
            with open(sorted_file_path, "r", encoding='utf-8') as f:
                data = json.load(f)

            return render_template('product_json.html', data=data, last_request=last_request)
        else:
            return "No requests found for this user."

    return redirect(url_for('home'))
    
@app.route('/api/products', methods=['GET'])
def get_products():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    sorted_file_path = f'{user_id}_SORTED_PRODUCTS_DATA.json'

    if not os.path.exists(sorted_file_path):
        return jsonify([])  # Возвращаем пустой список, если данных пока нет

    with open(sorted_file_path, "r", encoding='utf-8') as f:
        data = json.load(f)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
