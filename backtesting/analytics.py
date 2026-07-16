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



    def report(self):

        return {

            "expectancy":
                round(
                    self.expectancy(),
                    2
                ),

            "max_consecutive_losses":
                self.consecutive_losses()

        }
