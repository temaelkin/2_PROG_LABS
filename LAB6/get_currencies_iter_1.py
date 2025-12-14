import requests
import sys

def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js", handle=sys.stdout):
    """
    Получает курсы валют с API Центробанка России.

    Функция выполняет HTTP-запрос к внешнему API, обрабатывает ответ
    и возвращает курсы запрошенных валют.

    Все сообщения об ошибках выводятся в переданный поток handle
    (по умолчанию stdout).

    Args:
        currency_codes (list):
            Список символьных кодов валют (например: ['USD', 'EUR'])
        url (str):
            URL API ЦБ РФ
        handle (file-like object):
            Поток для вывода сообщений об ошибках (stdout, файл и т.п.)

    Returns:
        dict | None:
            Словарь с курсами валют или None в случае ошибки.
    """

    try:
        # Отправляем запрос к API
        response = requests.get(url)
        response.raise_for_status()

        # Парсинг JSON-ответа
        data = response.json()

        # Проверяем наличие ключа с курсами валют
        if "Valute" not in data:
            handle.write(f"В API отсутствуют курсы валют!")
            return None

        currencies = {}

        # Обрабатываем список запрошенных валют
        for code in currency_codes:
            if code in data["Valute"]:
                currencies[code] = data["Valute"][code]["Value"]
            else:
                # Некритичная ситуация: валюта не найдена
                currencies[code] = f"Код валюты '{code}' не найден."
        return currencies

    except requests.exceptions.RequestException as e:
        # Ошибки сети, HTTP, DNS, таймауты и т.п.
        print(e, file=handle)
        handle.write(f"Ошибка при запросе к API: {e}")
        # Пробрасываем исключение дальше
        raise requests.exceptions.RequestException("Ошибка сети при запросе к API") from e
    
    except KeyError as e:
        # Ошибка структуры ответа API
        handle.write(f"Ошибка: отсутствует ключ: {e}")
        return None
    
    except Exception as e:
        # Любая другая непредвиденная ошибка
        handle.write(f"Неизвестная ошибка: {e}")
        return None
    
if __name__ == "__main__":
    # Корректный запрос
    currencies = get_currencies(["USD", "EUR"])
    print("Курсы валют: ", currencies)

    # Несуществующий код валюты
    currencies = get_currencies(["USD", "XYZ"])
    print("Результат с несуществующей валютой: ", currencies)

    # Запрос по неправильному URL
    currencies = get_currencies(["USD", "EUR"], url="https://example.com")
    print("Курсы валют по неправильному URL: ", currencies)