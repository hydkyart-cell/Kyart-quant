class Portfolio:

    def __init__(self, starting_balance=10000):

        self.cash = float(starting_balance)
        self.position = 0
        self.entry_price = None

        self.realized_pnl = 0.0
        self.trade_count = 0

    def buy(self, price):

        if self.position == 0:

            self.position = 1
            self.entry_price = price
            self.trade_count += 1

            return "BUY EXECUTED"

        return "ALREADY IN POSITION"

    def sell(self, price):

        if self.position == 1:

            profit = price - self.entry_price

            self.cash += profit

            self.realized_pnl += profit

            self.position = 0
            self.entry_price = None

            return f"SELL EXECUTED | PnL: {profit:.2f}"

        return "NO POSITION"

    def unrealized_pnl(self, current_price):

        if self.position == 0:
            return 0.0

        return current_price - self.entry_price

    def summary(self, current_price):

        return {
            "cash": round(self.cash,2),
            "position": self.position,
            "entry": self.entry_price,
            "unrealized": round(
                self.unrealized_pnl(current_price),2
            ),
            "realized": round(self.realized_pnl,2),
            "trades": self.trade_count
        }
