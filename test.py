import unittest
from unittest.mock import MagicMock, patch
from cat_tests import CatFactProcessor, APIError
import requests

class TestCats(unittest.TestCase):
    def setUp(self):
        self.processor = CatFactProcessor()

    # Тесты на get fact
    # 1. Нет соединения
    @patch('requests.get')
    def test_get_fact_bad_connection(self, mock_get):
        mock_get.side_effect = ConnectionError
        mock_get.return_value.ok = False

        with self.assertRaises(ConnectionError):
            self.processor.get_fact()

    # 2. Пустая строка факта
    @patch('requests.get')
    def test_get_fact_null(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {
            "fact": "",
            "length": 20}

        fact = self.processor.get_fact()
        self.assertEqual(fact, "")

    # 3. Все хорошо
    @patch('requests.get')
    def test_get_fact_good_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {
            "fact": "Bla bla bla",
            "length": 11}

        fact = self.processor.get_fact()
        self.assertEqual(fact, "Bla bla bla")

    #Тесты на get_fact_analysis
    # 1. Нулевая длина
    @patch('requests.get')
    def test_get_fact_analysis_zero_length(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {"fact": "", "length": 0}

        analysis = self.processor.get_fact_analysis()
        self.assertEqual(analysis['length'], 0)

    # 2. Пустые частоты символов
    @patch('requests.get')
    def test_get_fact_analysis_null_frequencies(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {"fact": "", "length": 0}

        analysis = self.processor.get_fact_analysis()
        self.assertEqual(analysis['letter_frequencies'], {})

    # 3. Все хорошо
    @patch('requests.get')
    def test_get_fact_analysis_good_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {"fact": "Bla bla bla", "length": 11}

        self.processor.get_fact()
        analysis = self.processor.get_fact_analysis()
        self.assertEqual(analysis['length'], 11)
        self.assertEqual(analysis['letter_frequencies'], {'b': 3, 'l': 3, 'a': 3, ' ': 2,})

    # Интеграционный тест
    @patch('requests.get')
    def test_correct_functioning(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {
            "fact": "Unlike other cats, lions have a tuft of hair at the end of their tails.",
            "length": 71}

        fact = self.processor.get_fact()
        self.assertEqual(fact, "Unlike other cats, lions have a tuft of hair at the end of their tails.")

        analysis = self.processor.get_fact_analysis()
        self.assertEqual(analysis['length'], 71)
        self.assertEqual(analysis['letter_frequencies'], {'u': 2, 'n': 3, 'l': 3, 'i': 5, 'k': 1, 'e': 6, ' ': 14,
                                                          'o': 4, 't': 8, 'h': 5, 'r': 3, 'c': 1, 'a': 6, 's': 3,
                                                          ',': 1, 'v': 1, 'f': 3, 'd': 1, '.': 1})

if __name__ == '__main__':
    unittest.main()