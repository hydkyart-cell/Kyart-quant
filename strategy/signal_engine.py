class SignalEngine:

    def generate(self, price, sma, ema, ema200):

        if sma is None or ema is None or ema200 is None:
            return "WAIT"


        # Market regime filter
        trend_distance = (
            abs(price - ema200) / ema200
        )


        # No clear trend
        if trend_distance < 0.001:
            return "HOLD"



        # Bullish regime
        if price > ema200:

            if price > ema > sma:
                return "STRONG BUY"

            if price > sma:
                return "BUY"



        # Bearish regime
        if price < ema200:

            if price < ema < sma:
                return "STRONG SELL"

            if price < sma:
                return "SELL"


        return "HOLD"
