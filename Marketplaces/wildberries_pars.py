from functions import page_down
from playwright.async_api import async_playwright

class WbPars:
    def __init__(self, scroll_count, wb_inp):
        self.scroll_count = scroll_count
        self.wb_inp = wb_inp
        self.wb_unique_products = []

    async def wb_parse(self):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)  # Установите headless=True для скрытого режима
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                )

                page = await context.new_page()
                await page.goto(f'https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&cardsize=big&search={self.wb_inp}')
                await page.wait_for_timeout(5000)

                for _ in range(self.scroll_count):  # Пролистывание страницы для предварительной прогрузки
                    await page_down(page)
                    await page.wait_for_timeout(1000)  # Дайте время для загрузки новых элементов

                    # Ждем, пока новые элементы загрузятся
                    await page.wait_for_selector('.product-card__wrapper')  # Ждем появления карточек товаров
                    product_cards = await page.query_selector_all('.product-card__wrapper')

                    for card in product_cards:
                        title_element = await card.query_selector('a.product-card__link')
                        title = await title_element.get_attribute('aria-label') if title_element else 'Нет названия'

                        photo_element = await card.query_selector('img.j-thumbnail')
                        photo = await photo_element.get_attribute('src') if photo_element else 'Нет картинки'

                        link_element = await card.query_selector('a.product-card__link')
                        link = await link_element.get_attribute('href') if link_element else 'Нет ссылки'

                        price_element = await card.query_selector('.price__lower-price')
                        price = await price_element.inner_text() if price_element else print(price_element)

                        raiting_element = await card.query_selector('span.product-card__count')  # Первый span для рейтинга
                        raiting = await raiting_element.inner_text() if raiting_element else 'Нет рейтинга'

                        reviews_element = await card.query_selector('span.address-rate-mini')  # Второй span для отзывов
                        reviews = await reviews_element.inner_text() if reviews_element else 'Нет отзывов'

                        wb_product_data = {
                            'product_market': 'Wildberries',
                            'product_name': title,
                            'product_photo': photo,
                            'product_link': link,
                            'product_price': price,
                            'product_stars': raiting,
                            'product_reviews': reviews,
                        }

                        self.wb_unique_products.append(wb_product_data)

        except Exception as e:
            print(f'Ошибка: {e}')

    def wb_get_unique_products(self):
        return {product['product_name']: product for product in self.wb_unique_products}.values()