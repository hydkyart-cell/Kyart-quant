import time
from rich.live import Live
from rich.table import Table

from core.market_engine import MarketEngine
from core.engine import TradingEngine
from notifications import TelegramNotifier


class KyartApp:

    def __init__(self):
        self.market = MarketEngine(symbol="btcusdt")
        self.engine = TradingEngine()
        self.telegram = TelegramNotifier()

        self.last_sent_signal = None

        # Notification protection
        self.last_notification_time = 0
        self.notification_cooldown = 900  # 15 minutes


    def start_market(self):
        self.market.start()


    def render(self, snapshot):

        table = Table(title="KYART QUANT LIVE TERMINAL")

        table.add_column("Metric")
        table.add_column("Value")

        table.add_row("Price", str(snapshot["price"]))
        table.add_row("Signal", str(snapshot["signal"]))
        table.add_row("Action", str(snapshot["action"]))

        table.add_row("", "")

        p = snapshot["portfolio"]

        table.add_row("Cash", str(p["cash"]))
        table.add_row("Position", str(p["position"]))
        table.add_row("Equity", str(p["equity"]))
        table.add_row("Realized PnL", str(p["realized"]))
        table.add_row("Unrealized PnL", str(p["unrealized"]))

        table.add_row("", "")

        table.add_row("SMA", str(snapshot["sma"]))
        table.add_row("EMA", str(snapshot["ema"]))
        table.add_row("Volatility", str(snapshot["volatility"]))

        return table


    def run(self):

        self.start_market()

        self.telegram.send(
            "🟢 Kyart Quant started successfully."
        )


        with Live(
            self.render({
                "price": 0,
                "signal": "INIT",
                "action": "INIT",
                "sma": 0,
                "ema": 0,
                "volatility": 0,
                "portfolio": {
                    "cash": 10000,
                    "position": 0,
                    "equity": 10000,
                    "realized": 0,
                    "unrealized": 0
                }
            }),
            refresh_per_second=4,
            screen=True
        ) as live:


            while True:

                price = self.market.get_latest_price()


                if price is None:
                    time.sleep(0.2)
                    continue


                snapshot = self.engine.update(price)


                live.update(
                    self.render(snapshot)
                )


                # New BUY/SELL signals only
                if (
                    snapshot["signal"] in ["BUY", "SELL"]
                    and snapshot["signal"] != self.last_sent_signal
                ):

                    self.telegram.send(
                        f"""
📊 Kyart Quant Signal

Signal: {snapshot['signal']}
Price: {price}
Action: {snapshot['action']}
"""
                    )

                    self.last_sent_signal = snapshot["signal"]


                # Controlled system notifications
                elif (
                    snapshot["send_notification"]
                    and time.time() - self.last_notification_time >= self.notification_cooldown
                ):

                    p = snapshot["portfolio"]

                    self.telegram.send(
                        f"""
🟢 Kyart Quant Update

Price: {snapshot['price']}
Signal: {snapshot['signal']}
Action: {snapshot['action']}

Portfolio:
Cash: {p['cash']}
Position: {p['position']}
Equity: {p['equity']}

Indicators:
SMA: {snapshot['sma']}
EMA: {snapshot['ema']}
Volatility: {snapshot['volatility']}
"""
                    )

                    self.last_notification_time = time.time()


                time.sleep(0.25)



if __name__ == "__main__":
    KyartApp().run()
