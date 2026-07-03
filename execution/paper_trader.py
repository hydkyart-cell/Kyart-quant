class PaperTrader:
    def __init__(self, starting_balance=10000):
        self.balance = starting_balance
        self.position = None

    def execute(self, signal, price, symbol):
        if signal == "NO_TRADE":
            return "No action taken"

        if self.position is None:
            self.position = {
                "symbol": symbol,
                "entry_price": price,
                "side": signal
            }
            return f"Opened {signal} at {price}"

        # close position logic
        pnl = 0
        if self.position["side"] == "BUY":
            pnl = price - self.position["entry_price"]
        else:
            pnl = self.position["entry_price"] - price

        self.balance += pnl
        self.position = None

        return f"Closed trade. PnL: {round(pnl, 5)} | Balance: {round(self.balance, 2)}"
def dashboard(self):
    stats = self.stats()

    print("\n" + "="*40)
    print(" KYART QUANT DASHBOARD")
    print("="*40)
    print(f"Balance     : {round(self.balance, 2)}")
    print(f"Trades      : {stats['total_trades']}")
    print(f"Wins        : {stats['wins']}")
    print(f"Losses      : {stats['losses']}")
    print(f"Win Rate    : {stats['win_rate']}")
    print("="*40 + "\n")
