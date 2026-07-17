class PerformanceAnalyzer:
    def __init__(self, trades):
        self.trades = trades

    def total_profit(self):
        return sum(t["profit"] for t in self.trades)

    def win_rate(self):
        if not self.trades:
            return 0

        wins = 0

        for trade in self.trades:
            if trade["profit"] > 0:
                wins += 1

        return (wins / len(self.trades)) * 100

    def profit_factor(self):
        profit = 0
        loss = 0

        for trade in self.trades:
            if trade["profit"] > 0:
                profit += trade["profit"]
            else:
                loss += abs(trade["profit"])

        if loss == 0:
            return 0

        return profit / loss

    def expectancy(self):
        if not self.trades:
            return 0

        return self.total_profit() / len(self.trades)

    def max_drawdown(self):
        equity = 0
        peak = 0
        max_drawdown = 0

        for trade in self.trades:
            equity += trade["profit"]

            if equity > peak:
                peak = equity

            drawdown = peak - equity

            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return max_drawdown
