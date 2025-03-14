import json

def sort_products(min_price=None, max_price=None, min_rating=None, max_rating=None, 
                  input_file='PRODUCTS_DATA.json', output_file='SORTED_PRODUCTS_DATA.json'):
    try:
        # Чтение данных из файла
        with open(input_file, 'r', encoding='utf-8') as file:
            products = json.load(file)

        def clean_price(price_text):
            """Очищает и преобразует цену в число"""
            if not price_text:
                return None
            price_text = price_text.replace('\xa0', '').replace(' ', '').replace('₽', '')
            return float(price_text) if price_text.replace('.', '', 1).isdigit() else None

        def clean_reviews(reviews_text):
            """Очищает и преобразует количество отзывов в число"""
            if not reviews_text:
                return 0
            reviews_text = reviews_text.replace('\xa0', '').replace(' ', '').split()[0]
            return int(reviews_text) if reviews_text.isdigit() else 0

        def clean_stars(stars_text):
            """Очищает и преобразует рейтинг в число"""
            if not stars_text or stars_text == "Нет рейтинга":
                return None
            stars_text = stars_text.replace(',', '.').replace('\xa0', '').split()[0]
            return float(stars_text) if stars_text.replace('.', '', 1).isdigit() else None

        def calculate_score(product):
            """Вычисляет рейтинг товара на основе цены, отзывов и звёзд"""
            try:
                price = clean_price(product.get('product_price', ''))
                reviews = clean_reviews(product.get('product_reviews', ''))
                stars = clean_stars(product.get('product_stars', ''))

                if price is None or stars is None:  # Исключаем товары без цены или рейтинга
                    return None

                # Проверка условий фильтрации
                if (min_price is not None and price < min_price) or (max_price is not None and price > max_price):
                    return None
                if (min_rating is not None and stars < min_rating) or (max_rating is not None and stars > max_rating):
                    return None

                # Расчёт итогового рейтинга (весовые коэффициенты можно подстроить)
                price_score = -1 / price if price > 0 else 0  # Дешёвые товары получают более высокий балл
                review_score = reviews * 0.1  # Количество отзывов учитывается, но не доминирует
                star_score = stars * 0.4  # Рейтинг (звёзды) имеет наибольший вес

                total_score = price_score + review_score + star_score
                return total_score

            except Exception as e:
                print(f"Ошибка при расчёте оценки: {e}")
                return None

        # Удаление дубликатов (по ссылке на товар)
        seen = set()
        unique_products = []
        for product in products:
            product_link = product.get('product_link', '')
            if product_link and product_link not in seen:
                unique_products.append(product)
                seen.add(product_link)

        # Фильтрация товаров по критериям пользователя
        filtered_products = []
        for product in unique_products:
            score = calculate_score(product)
            if score is not None:  # Добавляем только те, что прошли фильтр
                product['score'] = score
                filtered_products.append(product)

        # Сортировка по рассчитанному рейтингу
        sorted_products = sorted(filtered_products, key=lambda x: x['score'], reverse=True)

        # Сохранение в новый JSON-файл
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
