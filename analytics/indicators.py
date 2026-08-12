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

        for price in prices[1:]:
            ema = (
                (price - ema) * multiplier
                + ema
            )

        return ema


    @staticmethod
    def volatility(prices, period=14):

        """
        Percentage volatility.

        Measures standard deviation of
        percentage price changes rather
        than absolute price differences.

        Example:
            0.005 = 0.5%
            0.01  = 1.0%
        """

        if prices is None:
            return None

        prices = list(prices)

        if len(prices) < period + 1:
            return None

        returns = []

        for i in range(
            len(prices) - period,
            len(prices)
        ):

            previous = prices[i - 1]
            current = prices[i]

            if previous == 0:
                continue

            returns.append(
                (current - previous) / previous
            )

        if len(returns) < period:
            return None

        avg = mean(returns)

        variance = sum(
            (value - avg) ** 2
            for value in returns
        ) / period

        return variance ** 0.5
