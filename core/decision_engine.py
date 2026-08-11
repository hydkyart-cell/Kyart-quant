class DecisionEngine:
    """
    Main decision layer.

    Uses:
    - EMA200 market regime
    - EMA/SMA alignment
    - Candle confirmation
    - ATR volatility filter
    """

    def decide(self, market_data):

        price = market_data.get("price")
        sma = market_data.get("sma")
        ema = market_data.get("ema")
        ema200 = market_data.get("ema200")
        atr = market_data.get("atr")
        candle = market_data.get("candle")


        if (
            price is None
            or sma is None
            or ema is None
            or ema200 is None
            or atr is None
        ):
            return "HOLD"


        # Avoid sideways markets
        if abs(price - ema200) < atr * 0.5:
            return "HOLD"


        candle_bullish = False
        candle_bearish = False


        if candle:

            candle_bullish = candle.close > candle.open
            candle_bearish = candle.close < candle.open


        # Bullish regime

        if price > ema200:

            if (
                price > ema > sma
                and ema > ema200
                and candle_bullish
            ):
                return "STRONG BUY"


            if (
                price > sma
                and sma > ema200
                and candle_bullish
            ):
                return "BUY"



        # Bearish regime

        elif price < ema200:

            if (
                price < ema < sma
                and ema < ema200
                and candle_bearish
            ):
                return "STRONG SELL"


            if (
                price < sma
                and sma < ema200
                and candle_bearish
            ):
                return "SELL"


        return "HOLD"
