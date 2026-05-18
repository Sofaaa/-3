class MovingAverageForecaster:
    """Реализация метода скользящей средней"""
    
    def moving_average_forecast(self, data, n_forecast: int, window_size: int):
        """
        Прогнозирование методом скользящей средней
        
        Args:
            data: исходный ряд данных
            n_forecast: количество прогнозируемых периодов
            window_size: размер окна для скользящей средней (n)
        
        Returns:
            список прогнозных значений
        """
        forecasts = []
        current_series = list(data)
        
        for _ in range(n_forecast):
            if len(current_series) < window_size:
                window_size = len(current_series)
            
            # Вычисляем скользящую среднюю за последние window_size периодов
            avg = sum(current_series[-window_size:]) / window_size
            forecasts.append(avg)
            current_series.append(avg)
        
        return forecasts