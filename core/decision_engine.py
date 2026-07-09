class DecisionEngine:
    """
    Conservative decision layer.

    Uses:
    - Trend
    - EMA/SMA relationship
    - Candle direction
    - Volatility
    """

    def decide(self, market_data):

        price = market_data.get("price")
        sma = market_data.get("sma")
        ema = market_data.get("ema")
        volatility = market_data.get("volatility")
        candle = market_data.get("candle")


        if sma is None or ema is None:
            return "HOLD"


        bullish = (
            price > sma
            and ema > sma
        )


        bearish = (
            price < sma
            and ema < sma
        )


        candle_bullish = False
        candle_bearish = False


        if candle:

            candle_bullish = (
                candle["close"] > candle["open"]
            )

            candle_bearish = (
                candle["close"] < candle["open"]
            )


        # Conservative confirmation

        if (
            bullish
            and candle_bullish
        ):
            return "BUY"


        if (
            bearish
            and candle_bearish
        ):
            return "SELL"


        return "HOLD"
