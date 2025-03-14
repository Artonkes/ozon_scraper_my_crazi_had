import json
from functions import page_down, sort_products
from playwright.async_api import async_playwright

class OzonPars:
    def __init__(self, scroll_count, ozon_inp, user_id):
        self.scroll_count = scroll_count
        self.ozon_inp = ozon_inp
        self.user_id = user_id
        self.output_file = f'{user_id}_PRODUCTS_DATA.json'
        self.sorted_file = f'{user_id}_SORTED_PRODUCTS_DATA.json'
        self.ozon_unique_products = []

    async def ozon_parse(self):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True, args=[
                    "--disable-blink-features=AutomationControlled",
                    "--start-maximized",])
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                )
                page = await context.new_page()
                await page.goto('https://www.ozon.ru')
                await page.wait_for_timeout(2000)
                await page.get_by_placeholder("Искать на Ozon").nth(0).type(f'{self.ozon_inp}', delay=0.5)
                await page.keyboard.press('Enter')

                for _ in range(self.scroll_count):
                    await page.wait_for_timeout(1000)
                    await page_down(page)
                    await page.wait_for_timeout(1000)

                    await page.wait_for_selector('.tile-root')
                    product_cards = await page.query_selector_all('.tile-root')

                    for card in product_cards:
                        title_element = await card.query_selector('span.tsBody500Medium')
                        title = await title_element.inner_text() if title_element else 'Нет названия'

                        photo_element = await card.query_selector('img')
                        photo = await photo_element.get_attribute('src') if photo_element else 'Нет картинки'

                        link_element = await card.query_selector('a.tile-clickable-element')
                        link = f"https://www.ozon.ru{await link_element.get_attribute('href')}" if link_element else 'Нет ссылки'

                        price_element = await card.query_selector('span.tsHeadline500Medium')
                        price = await price_element.inner_text() if price_element else 'Нет цены'

                        rating_element = await card.query_selector('span.p6b17-a4 > span:nth-child(1)')
                        rating = await rating_element.inner_text() if rating_element else 'Нет рейтинга'

                        # reviews_element = await card.query_selector('')
                        # reviews = await reviews_element.inner_text() if reviews_element else 'Нет отзывов'

                        ozon_product_data = {
                            'product_market': 'Ozon',
                            'product_name': title,
                            'product_photo': photo,
                            'product_link': link,
                            'product_price': price,
                            'product_stars': rating,
                            # 'product_reviews': reviews,
                        }

                        self.ozon_unique_products.append(ozon_product_data)
                        self.save_product(ozon_product_data)

        except Exception as e:
            print(f'Ошибка: {e}')

    def save_product(self, product):
        try:
            with open(self.output_file, 'r+', encoding='utf-8') as file:
                print(f'[OZ] Внёс в {self.output_file}')
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
