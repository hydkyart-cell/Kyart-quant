from execution.portfolio import Portfolio


class PaperTrader:
    """
    Simulated execution engine.
    Executes approved orders and updates the Portfolio.
    """

    def __init__(self, portfolio=None):
        self.portfolio = portfolio or Portfolio()
        self.trade_history = []

    def buy(self, price, quantity=1):

        cost = price * quantity

        if self.portfolio.cash < cost:
            return False, "Insufficient cash."

        self.portfolio.open_position(quantity, price)

        self.trade_history.append({
            "side": "BUY",
            "price": price,
            "quantity": quantity,
        })

        return True, "BUY executed."

    def sell(self, price, quantity=1):

        if self.portfolio.position < quantity:
            return False, "No open position."

        pnl = self.portfolio.close_position(quantity, price)

        self.trade_history.append({
            "side": "SELL",
            "price": price,
            "quantity": quantity,
            "pnl": round(pnl, 2),
        })

        return True, f"SELL executed. PnL: {pnl:.2f}"

    def summary(self, current_price):

        return self.portfolio.summary(current_price)
