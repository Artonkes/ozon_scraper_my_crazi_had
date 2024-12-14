import json
import asyncio
from Marketplaces.ozon_pars import OzonPars  # Измените на правильный импорт
from Marketplaces.wildberries_pars import WbPars
from Marketplaces.yandexmarket_pars import YMPars

async def main():
    try:
        # Создаем экземпляры классов
        oz_pars_instance = OzonPars(scroll_count=scrolls, oz_inp=pars_inp)
        wb_pars_instance = WbPars(scroll_count=scrolls, wb_inp=pars_inp)
        ym_pars_instance = YMPars(scroll_count=scrolls, ym_inp=pars_inp)

        # Запускаем парсинг
        await wb_pars_instance.wb_parse()
        await oz_pars_instance.oz_pars()
        await ym_pars_instance.ym_parse()

        # Получаем уникальные продукты
        oz_unique_products = oz_pars_instance.oz_get_unique_products()
        wb_unique_products = wb_pars_instance.wb_get_unique_products()
        ym_unique_products = ym_pars_instance.ym_get_unique_products()

        # Объединяем продукты
        combined_products = list(oz_unique_products) + list(wb_unique_products) + list(ym_unique_products)

        # Записываем в файл
        with open('PRODUCTS_DATA.json', 'w', encoding='utf-8') as file:
            json.dump(combined_products, file, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f'Произошла ошибка: {e}')

    print('[YAZAEBALSYA] Программа выполнена успешно')

if __name__ == "__main__":
    pars_inp = input('Введите товар, который хотите найти: ')
    scrolls = 5
    asyncio.run(main())