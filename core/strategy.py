from collections import deque
import random

class SimpleStrategy:
    def __init__(self, window=5):
        self.prices = deque(maxlen=window)

    def update(self, price):
        self.prices.append(price)

        if len(self.prices) < self.prices.maxlen:
            return "HOLD"

        avg = sum(self.prices) / len(self.prices)

        if price > avg * 1.002:
            return "BUY"
        elif price < avg * 0.998:
            return "SELL"
        else:
            return "HOLD"
