import json

from Marketplaces.ozon_pars import OzonPars  # Измените на правильный импорт
from Marketplaces.wildberries_pars import WbPars

async def main(pars_inp, scrolls):
    try:
        # Создаем экземпляры классов
        oz_pars_instance = OzonPars(scroll_count=scrolls, oz_inp=pars_inp)
        wb_pars_instance = WbPars(scroll_count=scrolls, wb_inp=pars_inp)

        # Запускаем парсинг
        await wb_pars_instance.wb_parse()
        await oz_pars_instance.oz_pars()

        # Получаем уникальные продукты
        oz_unique_products = oz_pars_instance.oz_get_unique_products()
        wb_unique_products = wb_pars_instance.wb_get_unique_products()

        # Объединяем продукты
        combined_products = list(oz_unique_products) + list(wb_unique_products)

        # Записываем в файл
        with open('PRODUCTS_DATA.json', 'w', encoding='utf-8') as file:
            json.dump(combined_products, file, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f'Произошла ошибка: {e}')

    print('[YAZAEBALSYA] Программа выполнена успешно')
