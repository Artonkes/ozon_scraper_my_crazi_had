from functions import page_down
from playwright.async_api import async_playwright

class YMPars:
    def __init__(self, scroll_count, ym_inp):
        self.scroll_count = scroll_count
        self.ym_inp = ym_inp
        self.ym_unique_products = []

    async def ym_parse(self):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)  # Установите headless=True для скрытого режима
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                )

                page = await context.new_page()
                await page.goto(f'https://market.yandex.ru/search?text={self.ym_inp}')
                await page.wait_for_timeout(1000)

                for _ in range(self.scroll_count):  # Пролистывание страницы для предварительной прогрузки
                    await page.wait_for_timeout(1000)
                    await page_down(page)
                    await page.wait_for_timeout(1000)  # Дайте время для загрузки новых элементов

                    # Ждем, пока новые элементы загрузятся
                    await page.wait_for_selector('#ServerLayoutRenderer')  # Ждем появления карточек товаров
                    product_cards = await page.query_selector_all('article[data-auto="searchOrganic"]')

                    for card in product_cards:
                        title_element = await card.query_selector('span[itemprop="name"]')
                        title = await title_element.inner_text() if title_element else 'Нет названия'

                        
                        photo_element = await card.query_selector('img.w7Bf7')
                        photo = await photo_element.get_attribute('src') if photo_element else 'Нет картинки'

                        link_element = await card.query_selector('a[data-auto="snippet-link"]')
                        link = await link_element.get_attribute('href') if link_element else 'Нет ссылки'

                        price_element = await card.query_selector('span.ds-text_headline-5_bold')
                        price = await price_element.inner_text() if price_element else 'Нет цены'

                        raiting_element = await card.query_selector('span.ds-text_color_text-rating')  # Первый span для рейтинга
                        raiting = await raiting_element.inner_text() if raiting_element else 'Нет рейтинга'

                        reviews_element = await card.query_selector('span.ds-text_color_text-secondary')  # Второй span для отзывов
                        reviews = await reviews_element.inner_text() if reviews_element else 'Нет отзывов'

                        ym_product_data = {
                            'product_market': 'YandexMarket',
                            'product_name': title,
                            'product_photo': photo,
                            'product_link': link,
                            'product_price': price,
                            'product_stars': raiting,
                            'product_reviews': reviews,
                        }


                        self.ym_unique_products.append(ym_product_data)

        except Exception as e:
            print(f'Ошибка: {e}')



    def ym_get_unique_products(self):
        return {product['product_name']: product for product in self.ym_unique_products}.values()