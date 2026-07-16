class BacktestPortfolio:
    """
    Simulated portfolio for backtesting.
    """

    def __init__(
        self,
        starting_cash=10000,
        stop_loss=0.01,
        take_profit=0.03
    ):

        self.cash = starting_cash
        self.position = 0

        self.entry_price = None

        self.stop_loss_percent = stop_loss
        self.take_profit_percent = take_profit

        self.stop_loss_price = None
        self.take_profit_price = None

        self.trades = []


    def buy(self, price):

        if self.position == 0:

            self.position = self.cash / price

            self.entry_price = price

            self.stop_loss_price = (
                price * (1 - self.stop_loss_percent)
            )

            self.take_profit_price = (
                price * (1 + self.take_profit_percent)
            )

            self.cash = 0


    def check_exit(self, price):

        if self.position > 0:

            if price <= self.stop_loss_price:

                self.sell(
                    price,
                    reason="STOP LOSS"
                )

                return True


            if price >= self.take_profit_price:

                self.sell(
                    price,
                    reason="TAKE PROFIT"
                )

                return True


        return False


    def sell(self, price, reason="SIGNAL"):

        if self.position > 0:

            value = self.position * price

            profit = value - (
                self.position * self.entry_price
            )

            self.cash = value

            self.trades.append({

                "entry": self.entry_price,

                "exit": price,

                "profit": profit,

                "reason": reason

            })

            self.position = 0

            self.entry_price = None

            self.stop_loss_price = None

            self.take_profit_price = None


    def equity(self, price):

        if self.position > 0:

            return self.position * price

        return self.cash
