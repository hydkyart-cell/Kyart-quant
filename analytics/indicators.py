from statistics import mean


class Indicators:

    @staticmethod
    def sma(prices, period=14):

        if prices is None:
            return None

        prices = list(prices)

        if len(prices) < period:
            return None

        return mean(prices[-period:])

    @staticmethod
    def ema(prices, period=14):

        if prices is None:
            return None

        prices = list(prices)

        if len(prices) < period:
            return None

        multiplier = 2 / (period + 1)
        ema = prices[0]

        for p in prices[1:]:
            ema = (p - ema) * multiplier + ema

        return ema

    @staticmethod
    def volatility(prices, period=14):

        if prices is None:
            return None

        prices = list(prices)

        if len(prices) < period:
            return None

        avg = mean(prices[-period:])

        variance = sum((p - avg) ** 2 for p in prices[-period:]) / period

        return variance ** 0.5
