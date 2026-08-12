class BacktestPortfolio:
    """
    Diagnostic backtest portfolio.

    Responsibilities:
    - Position management
    - Execution costs
    - Stop-loss / take-profit handling
    - Trade recording
    - Entry metadata preservation
    """

    def __init__(
        self,
        starting_cash=10000,
        position_fraction=0.20,
        stop_loss=0.01,
        take_profit=0.03,
        fee_rate=0.001,
        slippage_rate=0.0002
    ):

        self.starting_cash = starting_cash
        self.cash = starting_cash

        self.position = 0
        self.entry_price = None

        self.position_fraction = position_fraction

        self.stop_loss_percent = stop_loss
        self.take_profit_percent = take_profit

        self.fee_rate = fee_rate
        self.slippage_rate = slippage_rate

        self.stop_loss_price = None
        self.take_profit_price = None

        self.trades = []

        self.total_fees = 0
        self.total_slippage = 0

        self.entry_metadata = {}

    # =========================================================
    # BUY
    # =========================================================

    def buy(
        self,
        price,
        metadata=None
    ):

        if self.position > 0:
            return False

        execution_price = (
            price *
            (1 + self.slippage_rate)
        )

        allocation = (
            self.cash *
            self.position_fraction
        )

        fee = (
            allocation *
            self.fee_rate
        )

        usable_cash = (
            allocation - fee
        )

        if usable_cash <= 0:
            return False

        quantity = (
            usable_cash /
            execution_price
        )

        position_cost = (
            quantity *
            execution_price
        )

        self.cash -= position_cost
        self.cash -= fee

        self.position = quantity
        self.entry_price = execution_price

        self.stop_loss_price = (
            execution_price *
            (1 - self.stop_loss_percent)
        )

        self.take_profit_price = (
            execution_price *
            (1 + self.take_profit_percent)
        )

        self.total_fees += fee

        self.total_slippage += (
            quantity *
            abs(
                execution_price - price
            )
        )

        self.entry_metadata = dict(
            metadata or {}
        )

        return True

    # =========================================================
    # EXIT CHECK
    # =========================================================

    def check_exit(
        self,
        close,
        high,
        low
    ):

        if self.position <= 0:
            return False

        stop_hit = (
            low <= self.stop_loss_price
        )

        target_hit = (
            high >= self.take_profit_price
        )

        # Conservative assumption when
        # both are touched in one candle.
        if stop_hit and target_hit:

            return self.sell(
                self.stop_loss_price,
                reason="STOP LOSS"
            )

        if stop_hit:

            return self.sell(
                self.stop_loss_price,
                reason="STOP LOSS"
            )

        if target_hit:

            return self.sell(
                self.take_profit_price,
                reason="TAKE PROFIT"
            )

        return False

    # =========================================================
    # SELL
    # =========================================================

    def sell(
        self,
        price,
        reason="SIGNAL"
    ):

        if self.position <= 0:
            return False

        execution_price = (
            price *
            (1 - self.slippage_rate)
        )

        gross_value = (
            self.position *
            execution_price
        )

        fee = (
            gross_value *
            self.fee_rate
        )

        proceeds = (
            gross_value - fee
        )

        entry_value = (
            self.position *
            self.entry_price
        )

        profit = (
            proceeds -
            entry_value
        )

        self.cash += proceeds

        self.total_fees += fee

        self.total_slippage += (
            self.position *
            abs(
                self.entry_price -
                execution_price
            )
        )

        trade = {

            "entry":
                self.entry_price,

            "exit":
                execution_price,

            "profit":
                profit,

            "reason":
                reason,

            "fees":
                fee,

            "quantity":
                self.position,

            "entry_metadata":
                dict(
                    self.entry_metadata
                )
        }

        self.trades.append(
            trade
        )

        self.position = 0

        self.entry_price = None

        self.stop_loss_price = None
        self.take_profit_price = None

        self.entry_metadata = {}

        return True

    # =========================================================
    # EQUITY
    # =========================================================

    def equity(
        self,
        price
    ):

        if self.position > 0:

            return (
                self.cash +
                self.position * price
            )

        return self.cash
