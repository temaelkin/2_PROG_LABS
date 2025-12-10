import requests
import sys

def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js", handle=sys.stdout):
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']),
        url (str): URL API ЦБ РФ.

    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
              Возвращает None в случае ошибки запроса.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if "Valute" not in data:
            handle.write(f"В API отсутствуют курсы валют!")
            return None

        currencies = {}

        for code in currency_codes:
            if code in data["Valute"]:
                currencies[code] = data["Valute"][code]["Value"]
            else:
                currencies[code] = f"Код валюты '{code}' не найден."
        return currencies

    except requests.exceptions.RequestException as e:
        print(e, file=handle)
        handle.write(f"Ошибка при запросе к API: {e}")
        raise requests.exceptions.RequestException("Ошибка сети при запросе к API") from e
    except KeyError as e:
        handle.write(f"Ошибка: отсутствует ключ: {e}")
        return None
    except Exception as e:
        handle.write(f"Неизвестная ошибка: {e}")
        return None
    
if __name__ == "__main__":
    # Корректный запрос
    currencies = get_currencies(["USD", "EUR"])
    print("Курсы валют: ", currencies)

    # Несуществующий код валюты
    currencies = get_currencies(["USD", "XYZ"])
    print("Результат с несуществующей валютой: ", currencies)