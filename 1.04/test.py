import unittest
from collections import Counter
from cat_fact_processor import CatFactProcessor, APIError

class TestCatFactProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Метод, который выполняется один раз перед всеми тестами."""
        cls.processor = CatFactProcessor()
        cls.fact = cls.processor.get_fact()  #получаем факт один раз

    def test_get_fact_success(self):
        print(f"Полученный факт: {self.fact}")  #выводим факт
        self.assertIsInstance(self.fact, str)  #проверяем, что факт - это строка
        self.assertGreater(len(self.fact), 0)  #проверяем, что длина факта больше 0

    def test_get_fact_analysis_a_count(self):
        analysis = self.processor.get_fact_analysis()

        #проверяем, что количество букв 'a' равно 5
        letter_frequencies = dict(Counter(self.fact.lower()))
        count_a = letter_frequencies.get('a', 0)
        print(f"Количество букв 'a': {count_a}")  #выводим количество букв 'a'
        self.assertEqual(count_a, 5)  #проверяем, что количество 'a' равно 5

    def test_get_fact_analysis_no_fact(self):
        processor = CatFactProcessor()
        processor.last_fact = ""  #устанавливаем пустой факт
        analysis = processor.get_fact_analysis()

        self.assertEqual(analysis, {"length": 0, "letter_frequencies": {}})

if __name__ == '__main__':
    unittest.main()