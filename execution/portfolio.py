class Portfolio:
    """
    Stores the account state.
    Does NOT execute trades.
    """

    def __init__(self, starting_cash=10000):

        self.starting_cash = float(starting_cash)
        self.cash = float(starting_cash)

        self.position = 0
        self.entry_price = None

        self.realized_pnl = 0.0
        self.trade_count = 0

    def open_position(self, quantity, price):

        self.position += quantity
        self.entry_price = price
        self.cash -= quantity * price

    def close_position(self, quantity, price):

        if quantity > self.position:
            raise ValueError("Cannot close more than current position.")

        pnl = (price - self.entry_price) * quantity

        self.cash += quantity * price

        self.position -= quantity

        if self.position == 0:
            self.entry_price = None

        self.realized_pnl += pnl
        self.trade_count += 1

        return pnl

    def unrealized_pnl(self, current_price):

        if self.position == 0:
            return 0.0

        return (current_price - self.entry_price) * self.position

    def equity(self, current_price):

        return self.cash + self.position * current_price

    def summary(self, current_price):

        return {
            "cash": round(self.cash, 2),
            "equity": round(self.equity(current_price), 2),
            "position": self.position,
            "entry": self.entry_price,
            "realized": round(self.realized_pnl, 2),
            "unrealized": round(self.unrealized_pnl(current_price), 2),
            "trades": self.trade_count,
        }
