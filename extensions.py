import json
import requests
from config import keys

class APIException(Exception):
    pass

class Convertor:    #класс исключения ошибок и подсчета нужного количества валют
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={quote_key}')
        new_price = json.loads(r.content)[keys[quote]]
        p = new_price * amount
        message = f"Цена {int(amount)} {base} в {quote} : {p}" #вывод запроса, если не возникло ошибок

        return message
