from backtesting.portfolio import BacktestPortfolio


class Backtester:
    """
    KQ deterministic historical backtester.

    Responsibilities:
    - Consume precomputed indicator data
    - Generate strategy signals
    - Execute through BacktestPortfolio
    - Preserve entry metadata
    - Track MFE / MAE
    - Track execution diagnostics
    - Track timestamped equity curve
    """

    def __init__(
        self,
        starting_cash=10000,
        position_fraction=0.20,
        stop_loss=0.01,
        take_profit=0.03,
        fee_rate=0.001,
        slippage_rate=0.0002,
        initial_cash=None
    ):

        # Support both names for compatibility.
        if initial_cash is not None:
            starting_cash = initial_cash

        self.starting_cash = starting_cash

        self.portfolio = BacktestPortfolio(
            starting_cash=starting_cash,
            position_fraction=position_fraction,
            stop_loss=stop_loss,
            take_profit=take_profit,
            fee_rate=fee_rate,
            slippage_rate=slippage_rate
        )

        self.diagnostics = {
            "total": 0,
            "buy": 0,
            "strong_buy": 0,
            "sell": 0,
            "strong_sell": 0,
            "hold": 0,
            "missing_indicators": 0,
            "atr_distance": 0,
            "entries_attempted": 0,
            "entries_accepted": 0,
            "entries_rejected_position": 0,
            "signal_exits": 0,
            "stop_loss_exits": 0,
            "take_profit_exits": 0
        }

        self.equity_curve = []

        # Current-trade excursion tracking.
        self.current_mfe_percent = 0.0
        self.current_mae_percent = 0.0

    # =========================================================
    # SIGNAL GENERATION
    # =========================================================

    def generate_signal(
        self,
        price,
        sma,
        ema,
        ema200,
        atr,
        candle
    ):

        if (
            price is None
            or sma is None
            or ema is None
            or ema200 is None
            or atr is None
        ):
            return "HOLD"

        if atr <= 0:
            return "HOLD"

        # Reject only when price is extremely close to EMA200.
        if abs(price - ema200) < atr * 0.25:
            return "HOLD"

        bullish = candle.close > candle.open
        bearish = candle.close < candle.open

        # -----------------------------------------------------
        # BULLISH REGIME
        # -----------------------------------------------------

        if price > ema200:

            if (
                price > ema
                and ema > sma
                and ema > ema200
                and bullish
            ):
                return "STRONG BUY"

            if (
                price > sma
                and sma > ema200
                and bullish
            ):
                return "BUY"

        # -----------------------------------------------------
        # BEARISH REGIME
        # -----------------------------------------------------

        if price < ema200:

            if (
                price < ema
                and ema < sma
                and ema < ema200
                and bearish
            ):
                return "STRONG SELL"

            if (
                price < sma
                and sma < ema200
                and bearish
            ):
                return "SELL"

        return "HOLD"

    # =========================================================
    # DIAGNOSTICS
    # =========================================================

    def report_diagnostics(self):
        return dict(self.diagnostics)

    # =========================================================
    # TIMESTAMP EXTRACTION
    # =========================================================

    def _timestamp(self, candle, index):

        for attribute in (
            "timestamp",
            "open_time",
            "time",
            "datetime",
            "date"
        ):

            value = getattr(
                candle,
                attribute,
                None
            )

            if value is not None:
                return value

        return index

    # =========================================================
    # MFE / MAE
    # =========================================================

    def _update_excursion(
        self,
        high,
        low
    ):

        if self.portfolio.position <= 0:
            return

        entry = self.portfolio.entry_price

        if entry is None or entry <= 0:
            return

        favorable = (
            (high - entry)
            / entry
            * 100
        )

        adverse = (
            (low - entry)
            / entry
            * 100
        )

        self.current_mfe_percent = max(
            self.current_mfe_percent,
            favorable
        )

        self.current_mae_percent = min(
            self.current_mae_percent,
            adverse
        )

    def _reset_excursion(self):

        self.current_mfe_percent = 0.0
        self.current_mae_percent = 0.0

    def _attach_excursion_to_trade(self):

        if not self.portfolio.trades:
            return

        trade = self.portfolio.trades[-1]

        trade["mfe_percent"] = (
            self.current_mfe_percent
        )

        trade["mae_percent"] = (
            self.current_mae_percent
        )

        self._reset_excursion()

    # =========================================================
    # EXIT REASON
    # =========================================================

    def _record_exit_reason(self):

        if not self.portfolio.trades:
            return

        reason = self.portfolio.trades[-1].get(
            "reason"
        )

        if reason == "STOP LOSS":

            self.diagnostics[
                "stop_loss_exits"
            ] += 1

        elif reason == "TAKE PROFIT":

            self.diagnostics[
                "take_profit_exits"
            ] += 1

        else:

            self.diagnostics[
                "signal_exits"
            ] += 1

        self._attach_excursion_to_trade()

    # =========================================================
    # BACKTEST
    # =========================================================

    def run(
        self,
        candles,
        indicator_data
    ):

        self.equity_curve = []

        for key in self.diagnostics:
            self.diagnostics[key] = 0

        self._reset_excursion()

        for i, candle in enumerate(candles):

            self.diagnostics["total"] += 1

            # -------------------------------------------------
            # INDICATORS
            # -------------------------------------------------

            indicators = {}

            if isinstance(
                indicator_data,
                list
            ):

                if i < len(indicator_data):
                    indicators = (
                        indicator_data[i]
                        or {}
                    )

            elif isinstance(
                indicator_data,
                dict
            ):

                for key, values in (
                    indicator_data.items()
                ):

                    try:
                        indicators[key] = (
                            values[i]
                        )

                    except (
                        IndexError,
                        KeyError,
                        TypeError
                    ):
                        indicators[key] = None

            price = candle.close

            sma = indicators.get("sma")
            ema = indicators.get("ema")
            ema200 = indicators.get("ema200")
            atr = indicators.get("atr")

            if sma is None:
                sma = indicators.get("SMA")

            if ema is None:
                ema = indicators.get("EMA")

            if ema200 is None:
                ema200 = indicators.get("EMA200")

            if atr is None:
                atr = indicators.get("ATR")

            # -------------------------------------------------
            # UPDATE MFE / MAE BEFORE EXIT CHECK
            # -------------------------------------------------

            if self.portfolio.position > 0:

                self._update_excursion(
                    candle.high,
                    candle.low
                )

            # -------------------------------------------------
            # EXISTING POSITION EXIT
            # -------------------------------------------------

            if self.portfolio.position > 0:

                exited = self.portfolio.check_exit(
                    candle.close,
                    candle.high,
                    candle.low
                )

                if exited:
                    self._record_exit_reason()

            # -------------------------------------------------
            # INDICATOR READINESS
            # -------------------------------------------------

            if (
                sma is None
                or ema is None
                or ema200 is None
                or atr is None
            ):

                self.diagnostics[
                    "missing_indicators"
                ] += 1

                self.equity_curve.append({
                    "timestamp":
                        self._timestamp(
                            candle,
                            i
                        ),

                    "price":
                        candle.close,

                    "equity":
                        self.portfolio.equity(
                            candle.close
                        )
                })

                continue

            # -------------------------------------------------
            # ATR DISTANCE
            # -------------------------------------------------

            if abs(
                price - ema200
            ) < atr * 0.25:

                self.diagnostics[
                    "atr_distance"
                ] += 1

            # -------------------------------------------------
            # SIGNAL
            # -------------------------------------------------

            signal = self.generate_signal(
                price,
                sma,
                ema,
                ema200,
                atr,
                candle
            )

            signal_key = (
                signal
                .lower()
                .replace(" ", "_")
            )

            if signal_key in self.diagnostics:

                self.diagnostics[
                    signal_key
                ] += 1

            # -------------------------------------------------
            # SIGNAL EXIT
            # -------------------------------------------------

            if self.portfolio.position > 0:

                if signal in (
                    "SELL",
                    "STRONG SELL"
                ):

                    if self.portfolio.sell(
                        candle.close,
                        reason="SIGNAL"
                    ):

                        self._record_exit_reason()

            # -------------------------------------------------
            # ENTRY
            # -------------------------------------------------

            if self.portfolio.position <= 0:

                if signal in (
                    "BUY",
                    "STRONG BUY"
                ):

                    self.diagnostics[
                        "entries_attempted"
                    ] += 1

                    metadata = {

                        "signal":
                            signal,

                        "atr":
                            atr,

                        "ema200_distance_percent":
                            (
                                abs(
                                    price - ema200
                                )
                                / ema200
                                * 100
                            ),

                        "candle_direction":
                            (
                                "BULLISH"
                                if candle.close
                                > candle.open
                                else
                                "BEARISH"
                                if candle.close
                                < candle.open
                                else
                                "NEUTRAL"
                            ),

                        "sma":
                            sma,

                        "ema":
                            ema,

                        "ema200":
                            ema200
                    }

                    accepted = (
                        self.portfolio.buy(
                            candle.close,
                            metadata=metadata
                        )
                    )

                    if accepted:

                        self.diagnostics[
                            "entries_accepted"
                        ] += 1

                        self._reset_excursion()

                    else:

                        self.diagnostics[
                            "entries_rejected_position"
                        ] += 1

            # -------------------------------------------------
            # EQUITY
            # -------------------------------------------------

            self.equity_curve.append({

                "timestamp":
                    self._timestamp(
                        candle,
                        i
                    ),

                "price":
                    candle.close,

                "equity":
                    self.portfolio.equity(
                        candle.close
                    )
            })

        return self.equity_curve
