import requests

def log_errors(func):
    """
    Декоратор для обработки и вывода ошибок, возникающих при работе с сетью
    и внешним API.

    Отвечает за:
    - перехват сетевых ошибок (RequestException)
    - вывод сообщений об ошибках пользователю
    - повторное возбуждение исключения для сетевых ошибок
    - обработку логических и неожиданных ошибок
    """
    def wrapper(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
        try:
            # Выполняем декорируемую функцию
            return func(currency_codes, url)
        
        except requests.exceptions.RequestException as e:
            # Ошибки сети, HTTP, URL, таймауты и т.п.
            print(f"Ошибка при запросе к API: {e}")
            # Пробрасываем исключение дальше
            raise requests.exceptions.RequestException("Ошибка сети при запросе к API") from e
        
        except KeyError as e:
            # Ошибка структуры данных (ожидаемого ключа нет в ответе API)
            print(f"Логическая ошибка данных: отсутствует ключ: {e}")
            return None
        
        except Exception as e:
            # Любая другая непредвиденная ошибка
            print(f"Неизвестная ошибка: {e}")
            return None
    return wrapper

@log_errors
def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']),
        url (str): URL API ЦБ РФ.

    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
              Возвращает None в случае ошибки запроса.
    """

    # Отправляем HTTP-запрос к API
    response = requests.get(url)
    response.raise_for_status()

    # Парсинг JSON-ответа
    data = response.json()

    # Проверяем ожидаемую структуру данных
    if "Valute" not in data:
        raise KeyError("Valute")

    currencies = {}

    # Обрабатываем каждую запрошенную валюту
    for code in currency_codes:
        if code in data["Valute"]:
            currencies[code] = data["Valute"][code]["Value"]
        else:
            # Некритичная ситуация: валюта отсутствует в ответе API
            currencies[code] = f"Код валюты '{code}' не найден."

    return currencies
    
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