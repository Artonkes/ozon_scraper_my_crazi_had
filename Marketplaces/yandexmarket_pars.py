import json
from functions import page_down, sort_products
from playwright.async_api import async_playwright

class YMPars:
    def __init__(self, scroll_count, ym_inp, user_id):
        self.scroll_count = scroll_count
        self.ym_inp = ym_inp
        self.user_id = user_id
        self.output_file = f'{user_id}_PRODUCTS_DATA.json'
        self.sorted_file = f'{user_id}_SORTED_PRODUCTS_DATA.json'
        self.ym_unique_products = []

    async def ym_parse(self):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                )
                page = await context.new_page()
                await page.goto(f'https://market.yandex.ru/search?text={self.ym_inp}')
                await page.wait_for_timeout(7000)

                for _ in range(self.scroll_count):
                    await page_down(page)
                    await page.wait_for_timeout(1000)

                    await page.wait_for_selector('div[data-zone-name="productSnippet"]')
                    product_cards = await page.query_selector_all('div[data-zone-name="productSnippet"]')

                    for card in product_cards:
                        title_element = await card.query_selector('span[itemprop="name"]')
                        title = await title_element.inner_text() if title_element else 'Нет названия'

                        photo_element = await card.query_selector('img.w7Bf7')
                        photo = await photo_element.get_attribute('src') if photo_element else 'Нет картинки'

                        link_element = await card.query_selector('a[data-auto="snippet-link"]')
                        link = f"https://market.yandex.ru{await link_element.get_attribute('href')}" if link_element else 'Нет ссылки'

                        price_element = await card.query_selector('span.ds-text_headline-5_bold')
                        price = await price_element.inner_text() if price_element else 'Нет цены'

                        reviews_element = await card.query_selector('span.ds-text_lineClamp_1')
                        reviews = await reviews_element.inner_text() if reviews_element else 'Нет отзывов'

                        raiting_element = await card.query_selector('span.ds-text_color_text-rating')
                        raiting = await raiting_element.inner_text() if raiting_element else 'Нет рейтинга'


                        ym_product_data = {
                            'product_market': 'YandexMarket',
                            'product_name': title,
                            'product_photo': photo,
                            'product_link': link,
                            'product_price': price,
                            'product_stars': reviews,
                            'product_reviews': raiting,
                        }

                        self.ym_unique_products.append(ym_product_data)
                        self.save_product(ym_product_data)

        except Exception as e:
            print(f'Ошибка: {e}')

    def save_product(self, product):
        try:
            with open(self.output_file, 'r+', encoding='utf-8') as file:
                print(f'[Y] внёс в {self.output_file}')
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
