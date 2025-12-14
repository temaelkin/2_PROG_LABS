import unittest
from unittest.mock import patch, Mock
import requests
from get_currencies_iter_3 import get_currencies, logger

class TestGetCurrenciesLogging(unittest.TestCase):
    """Тесты функции get_currencies с логированием ошибок и предупреждений"""

    @patch("get_currencies_iter_3.requests.get")
    def test_successful_request(self, mock_get):
        """Проверка успешного запроса и структуры словаря"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 80.5},
                "EUR": {"Value": 88.7}
            }
        }
        mock_get.return_value = mock_response

        result = get_currencies(["USD", "EUR"])
        self.assertIsInstance(result, dict)
        self.assertEqual(result["USD"], 80.5)
        self.assertEqual(result["EUR"], 88.7)

    @patch("get_currencies_iter_3.requests.get")
    def test_nonexistent_currency(self, mock_get):
        """Проверка отсутствующей валюты и warning в логах"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "Valute": {"USD": {"Value": 80.5}}
        }
        mock_get.return_value = mock_response

        with self.assertLogs(logger, level='WARNING') as cm:
            result = get_currencies(["USD", "XYZ"])
        self.assertIn("Запрошен несуществующий код валюты: XYZ", cm.output[0])
        self.assertIn("XYZ", result)
        self.assertIsNone(result["XYZ"])

    @patch("get_currencies_iter_3.requests.get")
    def test_bad_url_exception_and_log(self, mock_get):
        """Проверка RequestException и логирования ошибки"""
        mock_get.side_effect = requests.exceptions.RequestException("bad url")
        with self.assertLogs(logger, level='ERROR') as cm:
            with self.assertRaises(requests.exceptions.RequestException):
                get_currencies(["USD"])
        self.assertTrue(any("Ошибка при запросе к API" in m for m in cm.output))

    @patch("get_currencies_iter_3.requests.get")
    def test_missing_key_in_response_and_log(self, mock_get):
        """Проверка KeyError и логирования ошибки"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        with self.assertLogs(logger, level='ERROR') as cm:
            result = get_currencies(["USD"])
        self.assertIsNone(result)
        self.assertTrue(any("Логическая ошибка данных" in m for m in cm.output))

    @patch("get_currencies_iter_3.requests.get")
    def test_empty_valute_with_nonexistent_currency(self, mock_get):
        """Проверка обработки пустого словаря Valute и warning"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"Valute": {}}
        mock_get.return_value = mock_response

        with self.assertLogs(logger, level='WARNING') as cm:
            result = get_currencies(["XYZ"])
        self.assertIsNone(result["XYZ"])
        self.assertTrue(any("Запрошен несуществующий код валюты: XYZ" in m for m in cm.output))

if __name__ == "__main__":
    unittest.main()
