import asyncio
import json

from Marketplaces.wildberries_pars import WbPars
from Marketplaces.yandexmarket_pars import YMPars
from Marketplaces.ozon_pars import OzonPars
from Marketplaces.avito_pars import AvitoPars

async def main(pars_inp, scrolls, user_id):
    # Создаем индивидуальный файл для пользователя
    output_file = f"{user_id}_PRODUCTS_DATA.json"
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump([], file, ensure_ascii=False, indent=4)

    # Инициализируем парсеры с индивидуальными параметрами
    oz_parser = OzonPars(scroll_count=scrolls, ozon_inp=pars_inp, user_id=user_id)
    wb_parser = WbPars(scroll_count=scrolls, wb_inp=pars_inp, user_id=user_id)
    ym_parser = YMPars(scroll_count=scrolls, ym_inp=pars_inp, user_id=user_id)
    av_parser = AvitoPars(scroll_count=scrolls, avito_inp=pars_inp, user_id=user_id)

    # Запускаем парсеры асинхронно
    await asyncio.gather(
        oz_parser.ozon_parse(),
        wb_parser.wb_parse(),
        ym_parser.ym_parse(),
        av_parser.avito_parse(),
    )

if __name__ == "__main__":
    import sys
    asyncio.run(main(pars_inp="Телефон", scrolls=5, user_id=0))