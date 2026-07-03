from collections import deque


class PriceBuffer:
    """
    Stores a rolling history of market prices.
    """

    def __init__(self, max_size=1000):
        self.prices = deque(maxlen=max_size)

    def add(self, price):
        self.prices.append(float(price))

    def latest(self):
        if not self.prices:
            return None
        return self.prices[-1]

    def size(self):
        return len(self.prices)

    def is_ready(self, minimum=20):
        return len(self.prices) >= minimum

    def get_prices(self):
        return list(self.prices)

    def clear(self):
        self.prices.clear()
