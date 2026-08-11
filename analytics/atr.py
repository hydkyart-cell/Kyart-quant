class ATR:

    def __init__(self, period=14):
        self.period = period
        self.values = []

    def update(self, high, low, previous_close):

        if previous_close is None:
            return None

        tr = max(
            high - low,
            abs(high - previous_close),
            abs(low - previous_close)
        )

        self.values.append(tr)

        if len(self.values) > self.period:
            self.values.pop(0)

        if len(self.values) < self.period:
            return None

        return sum(self.values) / len(self.values)
