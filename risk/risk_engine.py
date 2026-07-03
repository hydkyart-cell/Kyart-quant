class RiskEngine:
    def __init__(self):
        self.balance = 10000.0
        self.position = 0
        self.entry_price = None
        self.max_position = 1

    def process_signal(self, signal, price):
        action = "NONE"

        if signal == "BUY" and self.position == 0:
            self.position = 1
            self.entry_price = price
            action = "OPEN LONG"

        elif signal == "SELL" and self.position == 1:
            profit = price - self.entry_price
            self.balance += profit
            self.position = 0
            self.entry_price = None
            action = f"CLOSE LONG ({profit:.2f})"

        return {
            "balance": round(self.balance, 2),
            "position": self.position,
            "action": action
        }
