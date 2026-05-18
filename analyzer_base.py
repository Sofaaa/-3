from abc import ABC, abstractmethod
import pandas as pd
import matplotlib.pyplot as plt
from forecasting import MovingAverageForecaster

class DataAnalyzer(ABC):
    """Базовый абстрактный класс для всех анализаторов данных"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.forecaster = MovingAverageForecaster()
    
    @abstractmethod
    def display_table(self):
        """Вывести данные в табличном формате"""
        pass
    
    @abstractmethod
    def plot_data(self):
        """Построить графики зависимости от времени"""
        pass
    
    @abstractmethod
    def calculate_statistics(self):
        """Вычислить специфическую статистику по варианту"""
        pass
    
    def forecast(self, n_periods: int, window_size: int):
        """Прогнозирование методом скользящей средней"""
        values = self.data.iloc[:, 1].values  # предполагаем, что числовые данные во 2-м столбце
        forecast_values = self.forecaster.moving_average_forecast(values, n_periods, window_size)
        return forecast_values