from enum import Enum


class MarketRegime(Enum):

    TRENDING = "TRENDING"
    RANGING = "RANGING"
    UNCERTAIN = "UNCERTAIN"


class MarketRegimeFilter:
    """
    Deterministic market-regime classifier.

    Trend strength is primarily determined by
    EMA separation.

    Volatility is used as a confirmation/state
    variable rather than an absolute requirement
    for every trend.

    Volatility is expressed as a decimal.

    Example:

        0.001 = 0.10%
        0.005 = 0.50%
    """

    def __init__(
        self,
        volatility_threshold=0.001,
        trend_separation=0.003
    ):

        self.volatility_threshold = (
            volatility_threshold
        )

        self.trend_separation = (
            trend_separation
        )


    def classify(
        self,
        price,
        ema_fast,
        ema200,
        volatility
    ):

        if (
            price is None
            or ema_fast is None
            or ema200 is None
            or volatility is None
        ):

            return MarketRegime.UNCERTAIN


        if ema200 == 0:

            return MarketRegime.UNCERTAIN


        ema_separation = (
            abs(ema_fast - ema200)
            / abs(ema200)
        )


        # -------------------------------------------------
        # STRONG DIRECTIONAL STRUCTURE
        # -------------------------------------------------

        if ema_separation >= self.trend_separation:

            return MarketRegime.TRENDING


        # -------------------------------------------------
        # LOW VOLATILITY / COMPRESSED STRUCTURE
        # -------------------------------------------------

        if volatility < self.volatility_threshold:

            return MarketRegime.RANGING


        # -------------------------------------------------
        # BETWEEN STATES
        # -------------------------------------------------

        return MarketRegime.UNCERTAIN
