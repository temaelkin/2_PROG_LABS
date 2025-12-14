import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Вывод в консоль
        logging.FileHandler('currencies.log', encoding="utf-8")  # Запись в файл

    ]
)

logger = logging.getLogger(__name__)

def log_errors(func):
    """
    Декоратор для логирования ошибок и ключевых событий выполнения функции.

    Отвечает за:
    - логирование начала запроса
    - логирование успешного результата
    - обработку сетевых ошибок (RequestException)
    - логирование логических и неожиданных ошибок

    Сетевые ошибки пробрасываются дальше,
    остальные обрабатываются и возвращают None.
    """
    def wrapper(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
        try:
            # Логируем факт начала запроса
            logger.info(f"Запрос курсов валют: {currency_codes}")

            result = func(currency_codes, url)

            # Если результат успешно получен — логируем успех
            if result:
                logger.info(f"Успешно получены курсы для {list(result.keys())}")
            return result
        
        except requests.exceptions.RequestException as e:
            # Критическая ошибка сети или HTTP
            logger.error(f"Ошибка при запросе к API: {e}")
            # Пробрасываем исключение дальше
            raise requests.exceptions.RequestException("Ошибка сети при запросе к API") from e
        
        except KeyError as e:
            # Ошибка структуры данных (API вернул неожиданный формат)
            logger.error(f"Логическая ошибка данных: отсутствует ключ: {e}")
            return None
        
        except Exception as e:
            # Любая другая непредвиденная ошибка
            logger.error(f"Неизвестная ошибка: {e}")
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

    # Выполняем HTTP-запрос к API
    response = requests.get(url)
    response.raise_for_status()

    # Парсинг JSON-ответа
    data = response.json()

    # Проверяем ожидаемую структуру данных
    if "Valute" not in data:
        raise KeyError("Valute")

    currencies = {}

    # Обрабатываем запрошенные валюты
    for code in currency_codes:
        if code in data["Valute"]:
            currencies[code] = data["Valute"][code]["Value"]
        else:
            # Некритичная ситуация: валюта отсутствует в ответе API
            logger.warning(f"Запрошен несуществующий код валюты: {code}")
            currencies[code] = None

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