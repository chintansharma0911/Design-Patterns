from abc import ABC, abstractmethod


class TradingStrategy(ABC):
    @abstractmethod
    def execute_trade(self, data):
        pass


class MovingAverageStrategy(TradingStrategy):
    def execute_trade(self, data):
        # Calculate Moving Average (Simple example for illustration)
        window_size = 3  # Adjust as needed
        moving_average = sum(data[-window_size:]) / window_size
        return f"Executing Moving Average Trading Strategy. Moving Average: {moving_average:.2f}"

class MeanReversionStrategy(TradingStrategy):
    def execute_trade(self, data):
        # Calculate Mean Reversion (Simple example for illustration)
        mean_value = sum(data) / len(data)
        deviation = data[-1] - mean_value


# Step 3: Create the Context
class TradingContext:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def execute_trade(self, data):
        return self._strategy.execute_trade(data)