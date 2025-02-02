import json
from functions import page_down, sort_products
from playwright.async_api import async_playwright

class WbPars:
    def __init__(self, scroll_count, wb_inp, user_id):
        self.scroll_count = scroll_count
        self.wb_inp = wb_inp
        self.user_id = user_id
        self.output_file = f'{user_id}_PRODUCTS_DATA.json'
        self.sorted_file = f'{user_id}_SORTED_PRODUCTS_DATA.json'
        self.wb_unique_products = []

    async def wb_parse(self):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                )
                page = await context.new_page()
                await page.goto(f'https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&cardsize=big&search={self.wb_inp}')
                await page.wait_for_timeout(5000)

                for _ in range(self.scroll_count):
                    await page_down(page)
                    await page.wait_for_timeout(1000)

                    await page.wait_for_selector('.product-card__wrapper')
                    product_cards = await page.query_selector_all('.product-card__wrapper')

                    for card in product_cards:
                        title_element = await card.query_selector('a.product-card__link')
                        title = await title_element.get_attribute('aria-label') if title_element else 'Нет названия'

                        photo_element = await card.query_selector('img.j-thumbnail')
                        photo = await photo_element.get_attribute('src') if photo_element else 'Нет картинки'

                        link_element = await card.query_selector('a.product-card__link')
                        link = await link_element.get_attribute('href') if link_element else 'Нет ссылки'

                        price_element = await card.query_selector('.price__lower-price')
                        price = await price_element.inner_text() if price_element else 'Нет цены'

                        raiting_element = await card.query_selector('span.product-card__count')
                        raiting = await raiting_element.inner_text() if raiting_element else 'Нет рейтинга'

                        reviews_element = await card.query_selector('span.address-rate-mini')
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
                        self.save_product(wb_product_data)

        except Exception as e:
            print(f'Ошибка: {e}')

    def save_product(self, product):
        try:
            with open(self.output_file, 'r+', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
                data.append(product)
                file.seek(0)
                json.dump(data, file, ensure_ascii=False, indent=4)

                # Запускаем сортировку для индивидуального файла
                sort_products(input_file=self.output_file, output_file=self.sorted_file)

        except FileNotFoundError:
            with open(self.output_file, 'w', encoding='utf-8') as file:
                json.dump([product], file, ensure_ascii=False, indent=4)

                # Запускаем сортировку после создания нового файла
                sort_products(input_file=self.output_file, output_file=self.sorted_file)