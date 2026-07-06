class PaperTrader:

    def __init__(self):
        self.portfolio = {
            "cash": 10000,
            "position": 0,
            "equity": 10000,
            "realized": 0,
            "unrealized": 0
        }

    def buy(self, price):
        self.portfolio["position"] += 1
        self.portfolio["cash"] -= price

    def sell(self, price):
        self.portfolio["position"] -= 1
        self.portfolio["cash"] += price

    def get_portfolio(self):
        return self.portfolio
