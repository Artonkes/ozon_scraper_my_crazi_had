import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium_stealth import stealth
from functions import page_down, collect_product_info
from read import prints

searchinp=input()

def get_products_links(item_name):
    global products_urls

    def init_webdriver():
        driver = webdriver.Chrome()
        stealth(driver, platform='Win32', languages=["en-US", "en"])
        return driver

    driver = init_webdriver()
    driver.implicitly_wait(5)

    driver.get(url='https://ozon.ru')
    time.sleep(3)

    find_input = driver.find_element(By.NAME, 'text')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(2)

    find_input.send_keys(Keys.ENTER)
    time.sleep(2)

    current_url = f'{driver.current_url}&sorting=rating'
    driver.get(url=current_url)
    time.sleep(2)

    page_down(driver=driver)
    time.sleep(2)

    products_data =[]
    products_urls = set()

    while True:
        try:
            find_links = driver.find_elements(By.CLASS_NAME, 'tile-hover-target')
            products_urls.update(link.get_attribute("href") for link in find_links)

            print('[+] Ссылки на товары собраны!')

            for url in products_urls:
                data = collect_product_info(driver=driver, url=url)
                print(f'[+] Собрал данные товара с id: {data.get("product_id")}')
                products_data.append(data)

            # Переход на следующую страницу
            next_button = driver.find_element(By.XPATH, '//a[@data-testid="pagination-next"]')
            if next_button:
                next_button.click()
                time.sleep(2)  # Ждем загрузку следующей страницы
            else:
                break  # Если нет кнопки "Далее", выходим из цикла

        except Exception as e:
            print(f'[!] Ошибка при сборе данных: {e}')
            break

    with open('PRODUCTS_DATA.json', 'w', encoding='utf-8') as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)

    driver.close()
    driver.quit()


def main():
    print('[INFO] Сбор данных начался. Пожалуйста, ожидайте...')
    get_products_links(item_name=searchinp)

    # # Находим лучшее предложение
    # best_offer = find_best_offer()
    # if best_offer:
    #     print(f"[INFO] Лучшее предложение:\nНазвание: {best_offer['product_name']}\nЦена: {best_offer['product_discount_price']}\nОтзывы: {best_offer['product_reviews']}")
    # else:
    #     print("[INFO] Нет доступных предложений.")
    a = int(input("1 "))
    if a ==1:
        prints(a)
    else:
        print('error')

    print('[INFO] Работа выполнена успешно!')

if __name__ == '__main__':
    main()