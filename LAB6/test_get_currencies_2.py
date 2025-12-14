import unittest
from unittest.mock import patch, Mock
import requests
from get_currencies_iter_2 import get_currencies


class TestGetCurrenciesWithDecorator(unittest.TestCase):
    """Тесты функции get_currencies с декоратором log_errors"""

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
        self.assertIsInstance(result["XYZ"], str)
        self.assertIn("не найден", result["XYZ"])

    def test_bad_url_exception(self):
        """Проверка поднятия RequestException при недоступном URL"""
        with self.assertRaises(requests.exceptions.RequestException):
            get_currencies(["USD"], url="https://bad_url")

    @patch("requests.get")
    def test_missing_key_in_response(self, mock_get):
        """Проверка обработки KeyError при отсутствии 'Valute'"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {}  # нет ключа "Valute"
        mock_get.return_value = mock_response

        result = get_currencies(["USD"])
        self.assertIsNone(result)

    @patch("requests.get")
    def test_empty_valute_with_nonexistent_currency(self, mock_get):
        """Проверка пустого словаря Valute и несуществующей валюты"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"Valute": {}}  # пустой словарь валют
        mock_get.return_value = mock_response

        result = get_currencies(["XYZ"])
        self.assertIn("XYZ", result)
        self.assertIsInstance(result["XYZ"], str)
        self.assertIn("не найден", result["XYZ"])


if __name__ == "__main__":
    unittest.main()
