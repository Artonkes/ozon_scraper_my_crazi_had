import json

def sort_products(input_file='PRODUCTS_DATA.json', output_file='SORTED_PRODUCTS_DATA.json'):
    try:
        # Чтение данных из файла
        with open(input_file, 'r', encoding='utf-8') as file:
            products = json.load(file)

        def calculate_score(product):
            try:
                # Очистка цены
                price_text = product['product_price'].replace('\xa0', '').replace(' ', '').replace('₽', '')
                price = float(price_text) if price_text.isdigit() else float('inf')

                # Очистка отзывов
                reviews_text = product['product_reviews'].replace('\xa0', '').replace(' ', '')
                reviews_text = reviews_text.split()[0] if reviews_text else '0'
                reviews = int(reviews_text) if reviews_text.isdigit() else 0

                # Очистка рейтинга
                stars_text = product['product_stars'].replace(',', '.').replace('\xa0', '')
                stars_text = stars_text.split()[0] if stars_text else '0'
                stars = float(stars_text) if stars_text.replace('.', '', 1).isdigit() else 0

                # Если рейтинга нет или он равен 0, товар исключается из сортировки
                if stars == 0:
                    return 0

                # Нормализация данных
                price_score = -1 / price if price > 0 else 0
                review_score = reviews
                star_score = stars

                # Расчет итогового рейтинга
                total_score = (price_score * 0.50) + (review_score * 0.10) + (star_score * 0.40)
                return total_score
            except Exception as e:
                print(f"Ошибка при расчете оценки: {e}")
                return 0

        # Фильтрация товаров без рейтинга
        products = [product for product in products if product['product_stars'] and product['product_stars'] != 'Нет рейтинга']

        # Удаление дубликатов (используем product_link для уникальности)
        seen = set()
        unique_products = []
        for product in products:
            product_link = product.get('product_link')  # Используем уникальную ссылку на товар
            if product_link not in seen:
                unique_products.append(product)
                seen.add(product_link)

        # Сортировка данных
        sorted_products = sorted(unique_products, key=calculate_score, reverse=True)

        # Сохранение в новый файл
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(sorted_products, file, ensure_ascii=False, indent=4)



    except FileNotFoundError:
        print(f'Файл "{input_file}" не найден.')
    except json.JSONDecodeError:
        print(f'Ошибка декодирования JSON в файле "{input_file}".')







async def page_down(page):
    await page.evaluate('''
        const scrollStep = 200; // Размер шага прокрутки (в пикселях)
        const scrollInterval = 100; // Интервал между шагами (в миллисекундах)

        const scrollHeight = document.documentElement.scrollHeight;
        let currentPosition = 0;
        const interval = setInterval(() => {
            window.scrollBy(0, scrollStep);
            currentPosition += scrollStep;

            if (currentPosition >= scrollHeight) {
                clearInterval(interval);
            }
        }, scrollInterval);
    ''')
