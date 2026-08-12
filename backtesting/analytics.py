import math
from statistics import mean, stdev


class BacktestAnalytics:
    """
    Robust analytics layer for KQ backtests.

    Accepts either:
        [{"equity": 10000}, {"equity": 10020}]
    or:
        [10000, 10020]
    """

    def __init__(self, trades=None, equity_curve=None):
        self.trades = trades or []
        self.equity_curve = equity_curve or []

    # ---------------------------------------------------------
    # Normalization
    # ---------------------------------------------------------

    def _equity_values(self):
        values = []

        for item in self.equity_curve:

            if isinstance(item, dict):
                value = item.get("equity")

            else:
                value = item

            try:
                values.append(float(value))
            except (
                TypeError,
                ValueError
            ):
                continue

        return values

    # ---------------------------------------------------------
    # Trade metrics
    # ---------------------------------------------------------

    def total_profit(self):
        return sum(
            float(t.get("profit", 0))
            for t in self.trades
            if isinstance(t, dict)
        )

    def win_rate(self):
        if not self.trades:
            return 0.0

        wins = sum(
            1
            for t in self.trades
            if float(t.get("profit", 0)) > 0
        )

        return (wins / len(self.trades)) * 100

    def profit_factor(self):
        gross_profit = sum(
            float(t.get("profit", 0))
            for t in self.trades
            if float(t.get("profit", 0)) > 0
        )

        gross_loss = sum(
            abs(float(t.get("profit", 0)))
            for t in self.trades
            if float(t.get("profit", 0)) < 0
        )

        if gross_loss == 0:
            return 0.0

        return gross_profit / gross_loss

    def expectancy(self):
        if not self.trades:
            return 0.0

        return self.total_profit() / len(self.trades)

    # ---------------------------------------------------------
    # Returns
    # ---------------------------------------------------------

    def returns(self):
        equity = self._equity_values()

        if len(equity) < 2:
            return []

        returns = []

        for previous, current in zip(
            equity,
            equity[1:]
        ):

            if previous == 0:
                continue

            returns.append(
                (current - previous) / previous
            )

        return returns

    # ---------------------------------------------------------
    # Sharpe
    # ---------------------------------------------------------

    def sharpe_ratio(self):
        returns = self.returns()

        if len(returns) < 2:
            return 0.0

        average = mean(returns)

        deviation = stdev(returns)

        if deviation == 0:
            return 0.0

        return (
            average / deviation
        ) * math.sqrt(len(returns))

    # ---------------------------------------------------------
    # Drawdown
    # ---------------------------------------------------------

    def max_drawdown(self):
        equity = self._equity_values()

        if not equity:
            return 0.0

        peak = equity[0]
        max_dd = 0.0

        for value in equity:

            if value > peak:
                peak = value

            drawdown = peak - value

            if drawdown > max_dd:
                max_dd = drawdown

        return max_dd

    def max_drawdown_percent(self):
        equity = self._equity_values()

        if not equity:
            return 0.0

        peak = equity[0]
        max_dd = 0.0

        for value in equity:

            if value > peak:
                peak = value

            if peak > 0:

                drawdown_pct = (
                    (peak - value) / peak
                ) * 100

                max_dd = max(
                    max_dd,
                    drawdown_pct
                )

        return max_dd

    # ---------------------------------------------------------
    # Consecutive losses
    # ---------------------------------------------------------

    def max_consecutive_losses(self):
        current = 0
        maximum = 0

        for trade in self.trades:

            profit = float(
                trade.get("profit", 0)
            )

            if profit < 0:

                current += 1

                maximum = max(
                    maximum,
                    current
                )

            else:
                current = 0

        return maximum

    # ---------------------------------------------------------
    # Total return
    # ---------------------------------------------------------

    def total_return_percent(self):

        equity = self._equity_values()

        if len(equity) < 2:
            return 0.0

        starting = equity[0]
        ending = equity[-1]

        if starting == 0:
            return 0.0

        return (
            (ending - starting)
            / starting
        ) * 100

    # ---------------------------------------------------------
    # Report
    # ---------------------------------------------------------

    def report(self):
        return {
            "expectancy": self.expectancy(),
            "max_consecutive_losses":
                self.max_consecutive_losses(),
            "sharpe_ratio":
                self.sharpe_ratio(),
            "max_drawdown_percent":
                self.max_drawdown_percent(),
            "total_return_percent":
                self.total_return_percent(),
        }
