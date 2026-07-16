import math


class BacktestAnalytics:
    """
    Advanced quantitative performance metrics.
    """


    def __init__(self, trades, results):

        self.trades = trades
        self.results = results



    def expectancy(self):

        if not self.trades:
            return 0


        wins = [
            t["profit"]
            for t in self.trades
            if t["profit"] > 0
        ]


        losses = [
            t["profit"]
            for t in self.trades
            if t["profit"] <= 0
        ]


        win_rate = len(wins) / len(self.trades)

        loss_rate = len(losses) / len(self.trades)


        average_win = (
            sum(wins) / len(wins)
            if wins else 0
        )


        average_loss = (
            sum(losses) / len(losses)
            if losses else 0
        )


        return (
            (win_rate * average_win)
            +
            (loss_rate * average_loss)
        )



    def consecutive_losses(self):

        max_losses = 0

        current = 0


        for trade in self.trades:

            if trade["profit"] <= 0:

                current += 1

                max_losses = max(
                    max_losses,
                    current
                )

            else:

                current = 0


        return max_losses



    def returns(self):

        equity = []


        for result in self.results:

            equity.append(
                result["equity"]
            )


        returns = []


        for i in range(
            1,
            len(equity)
        ):

            if equity[i-1] != 0:

                returns.append(
                    (equity[i] - equity[i-1])
                    /
                    equity[i-1]
                )


        return returns



    def sharpe_ratio(self):

        returns = self.returns()


        if len(returns) < 2:

            return 0


        average = sum(returns) / len(returns)


        variance = sum(
            (r - average) ** 2
            for r in returns
        ) / len(returns)


        deviation = math.sqrt(
            variance
        )


        if deviation == 0:

            return 0


        return (
            average / deviation
        ) * math.sqrt(
            252
        )



    def drawdown_percent(self):

        if not self.results:

            return 0


        peak = self.results[0]["equity"]

        max_drawdown = 0


        for result in self.results:

            equity = result["equity"]


            if equity > peak:

                peak = equity


            drawdown = (
                peak - equity
            ) / peak * 100


            max_drawdown = max(
                max_drawdown,
                drawdown
            )


        return max_drawdown



    def report(self):

        return {

            "expectancy":
                round(
                    self.expectancy(),
                    2
                ),

            "max_consecutive_losses":
                self.consecutive_losses(),

            "sharpe_ratio":
                round(
                    self.sharpe_ratio(),
                    2
                ),

            "max_drawdown_percent":
                round(
                    self.drawdown_percent(),
                    2
                )

        }
