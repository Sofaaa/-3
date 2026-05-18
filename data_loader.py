import pandas as pd
import json
import csv

class DataLoader:
    """Загрузка данных из различных форматов"""
    
    @staticmethod
    def load_csv(filepath: str) -> pd.DataFrame:
        """Загрузка из CSV файла"""
        return pd.read_csv(filepath)
    
    @staticmethod
    def load_json(filepath: str) -> pd.DataFrame:
        """Загрузка из JSON файла"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    
    @staticmethod
    def load_excel(filepath: str) -> pd.DataFrame:
        """Загрузка из Excel файла"""
        return pd.read_excel(filepath)
    
    @staticmethod
    def generate_sample_population():
        """Генерация демо-данных для численности населения (Вариант 5)"""
        years = list(range(2009, 2025))  # 2009-2024
        # Примерные данные численности населения России (млн чел)
        population = [142.8, 142.9, 143.0, 143.2, 143.3, 143.5, 146.3, 146.5, 
                      146.8, 146.9, 146.7, 146.2, 145.9, 145.6, 145.3, 145.0]
        return pd.DataFrame({'Год': years, 'Численность_населения_млн': population})
    
    @staticmethod
    def generate_sample_weather():
        """Генерация демо-данных для погоды (Вариант 3)"""
        days = list(range(1, 32))
        import random
        random.seed(42)
        temps = {
            'День': days,
            'Максимальная_°C': [random.randint(-10, 25) for _ in days],
            'Минимальная_°C': [random.randint(-20, 15) for _ in days],
            'Средняя_°C': [random.randint(-15, 20) for _ in days],
            'Описание': random.choices(['Солнечно', 'Облачно', 'Дождь', 'Снег'], k=31)
        }
        return pd.DataFrame(temps)
    
    @staticmethod
    def generate_sample_inflation():
        """Генерация демо-данных для инфляции (Вариант 10)"""
        years = list(range(2009, 2025))
        inflation = [11.7, 8.8, 6.1, 6.6, 6.5, 11.4, 12.9, 5.4, 2.5, 4.3, 
                     3.0, 4.9, 8.4, 11.9, 7.4, 8.5]
        return pd.DataFrame({'Год': years, 'Инфляция_процент': inflation})