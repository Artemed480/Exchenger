import requests
import json
from config import currency


class ConvertException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(quote, base, amount):
        try:
            quote_ticker = currency[quote.lower()]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = currency[base.lower()]
        except KeyError:
            raise ConvertException(f"Не удалось обработать валюту {base}")

        if quote == base:
            raise ConvertException(f"Невозможно перевести одинаковые валюты {currency[base]}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f"Не удалось обработать количество {amount}")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}"

        payload = {}
        headers = {
            "apikey": "rDcqiYvArZplLSRqoEdn3Q9R2W3sKebD"
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        resp = json.loads(response.content)
        message = f'Цена {amount} {quote} в {base}: {resp.get("result")}'
        return message