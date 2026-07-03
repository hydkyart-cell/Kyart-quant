class SignalEngine:

    def generate(self, price, sma, ema):

        if sma is None or ema is None:
            return "WAIT"

        if price > ema > sma:
            return "STRONG BUY"

        if price > sma:
            return "BUY"

        if price < ema < sma:
            return "STRONG SELL"

        if price < sma:
            return "SELL"

        return "HOLD"
