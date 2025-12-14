# Отчёт к лабораторной работе №6
## Тема: "Запросы к API. Логирование и обработка ошибок"
---
Работу выполнил Елькин А.О.
---
## Постановка задачи:
Написать функцию get_currencies(currency_codes, url), которая обращается к API по url (по умолчанию - https://www.cbr-xml-daily.ru/daily_json.js) и возвращает словарь курсов валют для валют из списка currency_codes.

В возвращаемом словаре ключи - символьные коды валют, а значения - их курсы.
В случае ошибки запроса функция должна вернуть None.
Для обращения к API использовать функцию get модуля requests.

## Итерация 1:
Предусмотреть в функции логирование ошибок с использованием стандартного потока вывода (sys.stdout).

Функция должна обрабатывать следующие исключения:
- в ответе не содержатся курсы валют;
- в словаре курсов валют нет валюты из списка currency_codes;
- ошибка выполнения запроса к API.

### Код программы:
```python
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
```

## Итерация 2:
Вынести логирование ошибок из функции get_currencies(currency_codes, url) в декоратор.

### Код программы:
```python
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
```

## Итерация 3:
Оформить логирование ошибок с использованием модуля logging.

### Код программы:
```python
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
```

### Пример лога:
```log
2025-12-14 16:56:33,913 - INFO - Запрос курсов валют: ['USD', 'EUR']
2025-12-14 16:56:34,608 - INFO - Успешно получены курсы для ['USD', 'EUR']
2025-12-14 16:56:34,610 - INFO - Запрос курсов валют: ['USD', 'XYZ']
2025-12-14 16:56:35,388 - WARNING - Запрошен несуществующий код валюты: XYZ
2025-12-14 16:56:35,393 - INFO - Успешно получены курсы для ['USD', 'XYZ']
2025-12-14 16:56:35,394 - INFO - Запрос курсов валют: ['USD', 'EUR']
2025-12-14 16:56:36,464 - ERROR - Ошибка при запросе к API: Expecting value: line 1 column 1 (char 0)
```

## Тестирование
Были рассмотрены следующие ситуации:
- Проверка корректных ключей и значений:
```python
result = get_currencies(["USD", "EUR"])
assert isinstance(result["USD"], (int, float))
```
- Проверка обработки несуществующей валюты:
```python
result = get_currencies(["XYZ"])
assert result["XYZ"] is None
```
- Проверка исключений:
```python
try:
    get_currencies(["USD"], url="https://bad_url")
except requests.exceptions.RequestException:
    pass
```
- Проверка логов с помощью unittest и assertLogs:
```python
with self.assertLogs(logger, level="ERROR") as cm:
    get_currencies(["USD"], url="https://bad_url")
assert any("Ошибка при запросе к API" in msg for msg in cm.output)
```

## Анализ результатов
- Функция корректно возвращает курсы существующих валют.
- Для несуществующих валют возвращает None и пишет предупреждение в лог.
- Логирование позволяет отслеживать все события: запрос, успех, предупреждение и ошибку.
- Сетевые ошибки перехватываются и пробрасываются для дальнейшей обработки.
- KeyError при отсутствии ключа Valute корректно логируется и не ломает программу.

## Вывод
1. Декоратор log_errors позволяет централизованно обрабатывать исключения и логировать все важные события.
2. Использование logging облегчает отладку и аудит работы функции.
3. Функция работает корректно и стабильно обрабатывает любые ситуации, возникающие при запросе к API.