import json

from main import a

def find_largest_by_key(file_path, price, reviews):

    if a == 1:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                return "JSON-данные не являются списком объектов."

            # Цена
            largest_value_price = None
            largest_object_price = None


            for obj in data:
                if isinstance(obj, dict) and price in obj:
                    value = obj[price]
                    try: # Обработка возможных ошибок при сравнении
                        if largest_value_price is None or value < largest_value_price:
                            largest_value_price = value
                            largest_object_price = obj

                    except TypeError:
                        return f"Невозможно сравнить значения ключа '{price}'. Проверьте типы данных."



            if largest_object_price is not None:
                return largest_object_price
            else:
                return f"Ключ '{price}' не найден ни в одном объекте."

            # Отзывы
            largest_value_reviews = None
            largest_object_reviews = None

            for obj in data:
                if isinstance(obj, dict) and key in obj:
                    value = obj[reviews]
                    try:  # Обработка возможных ошибок при сравнении
                        if largest_value_reviews is None or value > largest_value_reviews:
                            largest_value_reviews = largest_value_reviews
                            largest_object_reviews = largest_object_reviews

                    except TypeError:
                        return f"Невозможно сравнить значения ключа '{reviews}'. Проверьте типы данных."



            if largest_object is not None:
                return largest_object
            else:
                return f"Ключ '{reviews}' не найден ни в одном объекте."


        except FileNotFoundError:
            return f"Файл {file_path} не найден."
        except json.JSONDecodeError as e:
            return f"Ошибка при разборе JSON: {e}"
        except Exception as e:
            return f"Произошла ошибка: {e}"


def prints():
    # Пример использования:
    file_path = 'PRODUCTS_DATA.json' # Замените на путь к вашему файлу
    key_to_price = 'product_discount_price' # Замените на нужный ключ
    key_to_reviews = 'product_reviews' # Замените на нужный ключ
    largest_obj = find_largest_by_key(file_path, price=key_to_price, reviews=key_to_reviews)
    print(f"Товар с высокой ценой': {largest_obj['product_discount_price']}\nЕго название: {largest_obj['product_name']} \n ")
    print(f"Товар с наибольшим количеством отзывов: '{largest_obj['product_reviews']}\nЕго название: {largest_obj['product_name']} \n ")