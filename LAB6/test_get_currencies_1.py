import unittest
from io import StringIO
from unittest.mock import patch, Mock
import requests
from get_currencies_iter_1 import get_currencies  # импорт твоей функции


class TestGetCurrencies(unittest.TestCase):
    """Тесты функции get_currencies с проверкой словаря, исключений и вывода в поток"""

    def test_successful_request(self):
        """Проверка ключей и числовых значений словаря"""
        result = get_currencies(["USD", "EUR"])
        self.assertIsInstance(result, dict)
        self.assertIn("USD", result)
        self.assertIn("EUR", result)
        self.assertIsInstance(result["USD"], (int, float))
        self.assertIsInstance(result["EUR"], (int, float))

    def test_nonexistent_currency(self):
        """Проверка поведения при несуществующем коде валюты"""
        result = get_currencies(["USD", "XYZ"])
        self.assertIn("USD", result)
        self.assertIn("XYZ", result)
        self.assertIsInstance(result["XYZ"], str)  # возвращается сообщение об ошибке

    def test_bad_url_exception_and_output(self):
        """Проверка поднятия RequestException и вывода ошибки в поток"""
        buf = StringIO()
        with self.assertRaises(requests.exceptions.RequestException):
            get_currencies(["USD"], url="https://bad_url", handle=buf)
        output = buf.getvalue().lower()
        self.assertIn("ошибка при запросе к api", output)

    @patch("requests.get")
    def test_missing_key_in_response_and_output(self, mock_get):
        """Проверка обработки KeyError и вывода сообщения о пропавшем ключе"""
        buf = StringIO()

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {}  # нет ключа "Valute"
        mock_get.return_value = mock_response

        result = get_currencies(["USD"], handle=buf)
        self.assertIsNone(result)
        output = buf.getvalue().lower()
        self.assertIn("в api отсутствуют курсы валют", output)

    @patch("requests.get")
    def test_empty_valute_with_nonexistent_currency(self, mock_get):
        """Проверка обработки пустого словаря Valute"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"Valute": {}}  # пустой словарь валют
        mock_get.return_value = mock_response

        result = get_currencies(["XYZ"])
        self.assertIn("XYZ", result)
        self.assertIsInstance(result["XYZ"], str)
        self.assertIn("не найден", result["XYZ"])  # проверяем текст ошибки в словаре

if __name__ == "__main__":
    unittest.main()