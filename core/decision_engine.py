from strategy.market_regime import (
    MarketRegime,
    MarketRegimeFilter
)


class DecisionEngine:
    """
    Deterministic KQ decision layer.

    Produces trading decisions and exposes
    rejection diagnostics for backtesting.

    Pipeline:

    1. Indicator readiness
    2. ATR distance filter
    3. Market regime filter
    4. Candle confirmation
    5. EMA/SMA alignment
    """

    def __init__(self):

        self.regime_filter = MarketRegimeFilter(
            volatility_threshold=0.005,
            trend_separation=0.003
        )

        self.diagnostics = {
            "TOTAL": 0,
            "BUY": 0,
            "STRONG BUY": 0,
            "SELL": 0,
            "STRONG SELL": 0,
            "HOLD": 0,

            "MISSING_INDICATORS": 0,
            "ATR_DISTANCE": 0,
            "RANGING": 0,
            "UNCERTAIN": 0,
            "NO_ALIGNMENT": 0,
            "NO_CANDLE_CONFIRMATION": 0
        }


    def decide(self, market_data):

        self.diagnostics["TOTAL"] += 1

        price = market_data.get("price")
        sma = market_data.get("sma")
        ema = market_data.get("ema")
        ema200 = market_data.get("ema200")
        atr = market_data.get("atr")
        volatility = market_data.get("volatility")
        candle = market_data.get("candle")


        # -------------------------------------------------
        # INDICATOR READINESS
        # -------------------------------------------------

        if (
            price is None
            or sma is None
            or ema is None
            or ema200 is None
            or atr is None
            or volatility is None
        ):

            self.diagnostics["MISSING_INDICATORS"] += 1
            self.diagnostics["HOLD"] += 1

            return "HOLD"


        # -------------------------------------------------
        # ATR DISTANCE FILTER
        # -------------------------------------------------

        if abs(price - ema200) < atr * 0.5:

            self.diagnostics["ATR_DISTANCE"] += 1
            self.diagnostics["HOLD"] += 1

            return "HOLD"


        # -------------------------------------------------
        # MARKET REGIME
        # -------------------------------------------------

        regime = self.regime_filter.classify(
            price,
            ema,
            ema200,
            volatility
        )


        if regime == MarketRegime.RANGING:

            self.diagnostics["RANGING"] += 1
            self.diagnostics["HOLD"] += 1

            return "HOLD"


        if regime == MarketRegime.UNCERTAIN:

            self.diagnostics["UNCERTAIN"] += 1
            self.diagnostics["HOLD"] += 1

            return "HOLD"


        # -------------------------------------------------
        # CANDLE CONFIRMATION
        # -------------------------------------------------

        candle_bullish = False
        candle_bearish = False

        if candle:

            candle_bullish = (
                candle.close > candle.open
            )

            candle_bearish = (
                candle.close < candle.open
            )


        # -------------------------------------------------
        # BULLISH TREND
        # -------------------------------------------------

        if price > ema200:

            if not candle_bullish:

                self.diagnostics[
                    "NO_CANDLE_CONFIRMATION"
                ] += 1

                self.diagnostics["HOLD"] += 1

                return "HOLD"


            if (
                price > ema
                and ema > sma
                and ema > ema200
            ):

                self.diagnostics["STRONG BUY"] += 1

                return "STRONG BUY"


            if (
                price > sma
                and sma > ema200
            ):

                self.diagnostics["BUY"] += 1

                return "BUY"


        # -------------------------------------------------
        # BEARISH TREND
        # -------------------------------------------------

        elif price < ema200:

            if not candle_bearish:

                self.diagnostics[
                    "NO_CANDLE_CONFIRMATION"
                ] += 1

                self.diagnostics["HOLD"] += 1

                return "HOLD"


            if (
                price < ema
                and ema < sma
                and ema < ema200
            ):

                self.diagnostics["STRONG SELL"] += 1

                return "STRONG SELL"


            if (
                price < sma
                and sma < ema200
            ):

                self.diagnostics["SELL"] += 1

                return "SELL"


        # -------------------------------------------------
        # NO VALID ALIGNMENT
        # -------------------------------------------------

        self.diagnostics["NO_ALIGNMENT"] += 1
        self.diagnostics["HOLD"] += 1

        return "HOLD"


    def diagnostic_report(self):

        return dict(self.diagnostics)
