class PerformanceAnalyzer:
    """
    Calculates backtest performance metrics.
    """

    def __init__(self, results, trades):

        self.results = results
        self.trades = trades


    def total_return(self):

        if not self.results:
            return 0

        start = self.results[0]["equity"]

        end = self.results[-1]["equity"]

        return (
            (end - start) / start
        ) * 100



    def total_trades(self):

        return len(self.trades)



    def winning_trades(self):

        return [
            trade
            for trade in self.trades
            if trade["profit"] > 0
        ]



    def losing_trades(self):

        return [
            trade
            for trade in self.trades
            if trade["profit"] <= 0
        ]



    def win_rate(self):

        total = self.total_trades()

        if total == 0:
            return 0

        return (
            len(self.winning_trades())
            /
            total
        ) * 100



    def average_win(self):

        winners = self.winning_trades()

        if not winners:
            return 0

        return sum(
            trade["profit"]
            for trade in winners
        ) / len(winners)



    def average_loss(self):

        losers = self.losing_trades()

        if not losers:
            return 0

        return sum(
            trade["profit"]
            for trade in losers
        ) / len(losers)



    def profit_factor(self):

        gross_profit = sum(
            trade["profit"]
            for trade in self.winning_trades()
        )

        gross_loss = abs(
            sum(
                trade["profit"]
                for trade in self.losing_trades()
            )
        )


        if gross_loss == 0:

            return 0


        return gross_profit / gross_loss



    def best_trade(self):

        if not self.trades:
            return 0

        return max(
            trade["profit"]
            for trade in self.trades
        )



    def worst_trade(self):

        if not self.trades:
            return 0

        return min(
            trade["profit"]
            for trade in self.trades
        )



    def max_drawdown(self):

        peak = 0

        drawdown = 0


        for result in self.results:

            equity = result["equity"]

            peak = max(
                peak,
                equity
            )


            current = peak - equity


            drawdown = max(
                drawdown,
                current
            )


        return drawdown



    def report(self):

        return {

            "return_percent":
                round(
                    self.total_return(),
                    2
                ),

            "total_trades":
                self.total_trades(),

            "win_rate":
                round(
                    self.win_rate(),
                    2
                ),

            "average_win":
                round(
                    self.average_win(),
                    2
                ),

            "average_loss":
                round(
                    self.average_loss(),
                    2
                ),

            "profit_factor":
                round(
                    self.profit_factor(),
                    2
                ),

            "best_trade":
                round(
                    self.best_trade(),
                    2
                ),

            "worst_trade":
                round(
                    self.worst_trade(),
                    2
                ),

            "max_drawdown":
                round(
                    self.max_drawdown(),
                    2
                )

        }
