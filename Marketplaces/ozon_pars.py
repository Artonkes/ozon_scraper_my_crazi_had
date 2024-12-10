from functions import page_down
from playwright.async_api import async_playwright

class OzonPars:
    def __init__(self, scroll_count, oz_inp):
        self.scroll_count = scroll_count
        self.oz_inp = oz_inp
        self.oz_unique_products = []

    async def oz_pars(self):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                )

                page = await context.new_page()
                await page.goto('https://www.ozon.ru/')
                await page.wait_for_timeout(2000)
                await page.reload()
                await page.wait_for_timeout(2000)
                await page.get_by_placeholder('Искать на Ozon').type(self.oz_inp, delay=1.5)
                await page.click('button[aria-label="Поиск"]')

                for _ in range(self.scroll_count):
                    await page_down(page)
                    await page.wait_for_timeout(1000)
                    await page.wait_for_selector('.tile-root')

                    product_cards = await page.query_selector_all('.tile-root')
                    for card in product_cards:
                        title_element = await card.query_selector('.tsBody500Medium')
                        title = await title_element.inner_text() if title_element else 'Нет названия'

                        link_element = await card.query_selector('a.tile-hover-target')
                        link = await link_element.get_attribute('href') if link_element else 'Нет ссылки'

                        price_element = await card.query_selector('.tsHeadline500Medium')
                        price = await price_element.inner_text() if price_element else 'Нет цены'

                        raiting_element = await card.query_selector('.tsBodyMBold span:nth-of-type(1)')
                        raiting = await raiting_element.inner_text() if raiting_element else 'Нет рейтинга'

                        reviews_element = await card.query_selector('.tsBodyMBold span:nth-of-type(2)')
                        reviews = await reviews_element.inner_text() if reviews_element else 'Нет отзывов'

                        product_data = {
                            'product_market': 'Ozon',
                            'product_name': title,
                            'product_link': link,
                            'product_price': price,
                            'product_stars': raiting,
                            'product_reviews': reviews,
                        }

                        self.oz_unique_products.append(product_data)

        except Exception as e:
            print(f'Ошибка: {e}')

    def oz_get_unique_products(self):
        # Возвращаем уникальные продукты
        return {product['product_name']: product for product in self.oz_unique_products}.values()
