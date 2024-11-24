import json
import time
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functions import page_down, collect_product_info
from read import prints

a = input("Введите название товара: ")
def get_products_links(item_name=a):
    global products_urls

    def init_webdriver():
        driver = webdriver.Chrome()
        stealth(driver, platform='Win32', languages=["en-US", "en"])
        return driver
    driver = init_webdriver()
    driver.implicitly_wait(5)

    driver.get(url='https://ozon.ru')
    time.sleep(2)

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

    try:
        find_links = driver.find_elements(By.CLASS_NAME, 'tile-hover-target')
        products_urls = list(set([f'{link.get_attribute("href")}' for link in find_links]))

        print('[+] Ссылки на товары собраны!')
    except:
        print('[!] Что-то сломалось при сборе ссылок на товары!')

    products_urls_dict = {}

    for k, v in enumerate(products_urls):
        products_urls_dict.update({k: v})

    with open('products_urls_dict.json', 'w', encoding='utf-8') as file:
        json.dump(products_urls_dict, file, indent=4, ensure_ascii=False)

    time.sleep(2)

    products_data = []

    for url in products_urls:
        data = collect_product_info(driver=driver, url=url)
        print(f'[+] Собрал данные товара с id: {data.get("product_id")}')
        time.sleep(2)
        products_data.append(data)

    with open('PRODUCTS_DATA.json', 'w', encoding='utf-8') as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)

    driver.close()
    driver.quit()


def main():
    print('[INFO] Сбор данных начался. Пожалуйста ожидайте...')
    get_products_links(item_name=a)
    print('[INFO] Работа выполнена успешно!')
    inr = int(input('Для вывода товаров введите 1 '))
    if inr == 1:
        prints()
    else:
        print("Error")



if __name__ == '__main__':
    main()
