import json
from playwright.sync_api import sync_playwright

def page_down(page):
    page.evaluate('''
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


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Установите headless=True для скрытого режима
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = context.new_page()

        page.goto('https://www.ozon.ru/')
        page.wait_for_timeout(2000)
        page.reload()
        page.wait_for_timeout(2000)
        print(page)
        page.get_by_placeholder('Искать на Ozon').type('Наушники', delay=1.5)  # Здесь менять запрос
        page.click('button[aria-label="Поиск"]')
        print(page)

        products = []
        total_scrolls = 5  # Количество прокруток

        for _ in range(total_scrolls):  # Пролистывание страницы для предварительной прогрузки
            page_down(page)
            page.wait_for_timeout(1000)  # Дайте время для загрузки новых элементов

            # Ждем, пока новые элементы загрузятся
            page.wait_for_selector('.tile-root')  # Ждем появления карточек товаров
            product_cards = page.query_selector_all('.tile-root')

            for card in product_cards:
                title_element = card.query_selector('.tsBody500Medium')
                title = title_element.inner_text() if title_element else 'Нет названия'

                price_element = card.query_selector('.tsHeadline500Medium')
                price = price_element.inner_text() if price_element else 'Нет цены'

                raiting_element = card.query_selector('.tsBodyMBold span:nth-of-type(1)')  # Первый span для рейтинга
                raiting = raiting_element.inner_text() if raiting_element else 'Нет рейтинга'

                reviews_element = card.query_selector('.tsBodyMBold span:nth-of-type(2)')  # Второй span для отзывов
                reviews = reviews_element.inner_text() if reviews_element else 'Нет отзывов'

                product_data = {
                    'product_name': title,
                    'product_price': price,
                    'product_stars': raiting,
                    'product_reviews': reviews,
                }

                products.append(product_data)

        # Удалите дубликаты, если они есть
        unique_products = {product['product_name']: product for product in products}.values()

        with open('PRODUCTS_DATA.json', 'w', encoding='utf-8') as file:
            json.dump(list(unique_products), file, indent=4, ensure_ascii=False)

        print('[info] Программа выполнена успешно')
        page.wait_for_timeout(10000)
        browser.close()


if __name__ == "__main__":
    main()