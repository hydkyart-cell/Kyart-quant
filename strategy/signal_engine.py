class SignalEngine:

    def generate(self, price, sma, ema, ema200, atr):

        # Indicator readiness check
        if sma is None or ema is None or ema200 is None or atr is None:
            return "WAIT"


        # ==========================
        # VOLATILITY / REGIME FILTER
        # ==========================

        # Avoid trading when price is too close
        # to the long-term trend line
        if abs(price - ema200) < atr * 0.5:
            return "HOLD"



        # ==========================
        # BULLISH MARKET REGIME
        # ==========================

        if price > ema200:

            # Strong bullish alignment
            if price > ema > sma and ema > ema200:
                return "STRONG BUY"


            # Normal bullish alignment
            if price > sma and sma > ema200:
                return "BUY"



        # ==========================
        # BEARISH MARKET REGIME
        # ==========================

        elif price < ema200:

            # Strong bearish alignment
            if price < ema < sma and ema < ema200:
                return "STRONG SELL"


            # Normal bearish alignment
            if price < sma and sma < ema200:
                return "SELL"



        # No valid setup
        return "HOLD"
