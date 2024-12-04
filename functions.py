import json
import time as tm
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

def page_down(driver):
    driver.execute_script('''
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

def collect_product_info(driver, url=''):
    driver.switch_to.new_window('tab')
    tm.sleep(3)
    driver.get(url=url)
    tm.sleep(3)

    # product_id
    product_id = driver.find_element(
        By.XPATH, '//div[contains(text(), "Артикул: ")]'
    ).text.split('Артикул: ')[1]

    page_source = str(driver.page_source)
    soup = BeautifulSoup(page_source, 'lxml')

    product_name = soup.find('div', attrs={"data-widget": 'webProductHeading'}).find(
        'h1').text.strip().replace('\t', '').replace('\n', ' ')

    product_url = f'{driver.current_url}'

    # product statistic
    try:
        product_statistic = soup.find(
            'div', attrs={"data-widget": 'webSingleProductScore'}).text.strip()

        if " • " in product_statistic:
            product_stars = product_statistic.split(' • ')[0].strip()
            product_reviews = product_statistic.split(' • ')[1].strip()
        else:
            product_statistic = product_statistic
    except:
        product_statistic = None
        product_stars = None
        product_reviews = None

    # product price
    try:
        ozon_card_price_element = soup.find(
            'span', string="c Ozon Картой").parent.find('div').find('span')
        product_ozon_card_price = ozon_card_price_element.text.strip(
        ) if ozon_card_price_element else ''

        price_element = soup.find(
            'span', string="без Ozon Карты").parent.parent.find('div').findAll('span')

        product_discount_price = price_element[0].text.strip(
        ) if price_element[0] else ''
        product_base_price = price_element[1].text.strip(
        ) if price_element[1] is not None else ''
    except:
        product_ozon_card_price = None
        product_discount_price = None
        product_base_price = None

    product_data = {
        'product_id': product_id,
        'product_name': product_name,
        'product_url': product_url,
        'product_ozon_card_price': product_ozon_card_price,
        'product_discount_price': product_discount_price,
        'product_base_price': product_base_price,
        'product_statistic': product_statistic,
        'product_stars': product_stars,
        'product_reviews': product_reviews,
    }

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return product_data
#
# def find_best_offer():
#     best_offer = None
#     best_value = float('-inf')  # Начальное значение для сравнения
#     with open('PRODUCTS_DATA.json', 'r', encoding='utf-8') as file:
#         products = json.load(file)
#
#     for product in products:
#         try:
#             discount_price = float(product['product_discount_price'].replace('₽', '').replace(' ', '').replace(',', '.'))
#             reviews = int(product['product_reviews'].replace('отзывов', '').replace('отзыв', '').replace(' ', '').replace(',', ''))
#
#             # Рассчитываем значение (количество отзывов / цена)
#             value = reviews / discount_price if discount_price > 0 else 0
#
#             # Сравниваем с лучшим предложением
#             if value > best_value:
#                 best_value = value
#                 best_offer = product
#         except (ValueError, AttributeError):
#                     # Игнорируем продукты с некорректными данными
#                     continue
#
#         return best_offer