from statistics import mean


class Indicators:
    """
    Basic Technical Indicators
    """

    @staticmethod
    def sma(prices, period):

        if len(prices) < period:
            return None

        return mean(prices[-period:])

    @staticmethod
    def ema(prices, period):

        if len(prices) < period:
            return None

        multiplier = 2 / (period + 1)

        ema = prices[0]

        for price in prices[1:]:
            ema = (price - ema) * multiplier + ema

        return ema

    @staticmethod
    def volatility(prices, period):

        if len(prices) < period:
            return None

        data = prices[-period:]

        avg = mean(data)

        variance = sum((x - avg) ** 2 for x in data) / len(data)

        return variance ** 0.5
