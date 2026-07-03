import time

from rich.live import Live
from rich.table import Table

from core.market_engine import MarketEngine
from core.engine import TradingEngine


class KyartApp:

    def __init__(self):

        self.market = MarketEngine(symbol="btcusdt")
        self.engine = TradingEngine()

        self.last_price = None

    def start_market(self):

        # runs Binance websocket in background thread
        self.market.start()

    def render(self, snapshot):

        table = Table(title="KYART QUANT LIVE TERMINAL")

        table.add_column("Metric")
        table.add_column("Value")

        table.add_row("Price", str(snapshot["price"]))
        table.add_row("Signal", snapshot["signal"])
        table.add_row("Action", snapshot["action"])

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

        with Live(self.render({
            "price": 0,
            "signal": "WAITING",
            "action": "INIT",
            "sma": 0,
            "ema": 0,
            "volatility": 0,
            "portfolio": {
                "cash": 0,
                "position": 0,
                "equity": 0,
                "realized": 0,
                "unrealized": 0
            }
        }), refresh_per_second=4, screen=True) as live:

            while True:

                price = self.market.get_latest_price()

                if price is None:
                    time.sleep(0.2)
                    continue

                snapshot = self.engine.update(price)

                live.update(self.render(snapshot))

                time.sleep(0.25)


if __name__ == "__main__":
    app = KyartApp()
    app.run()
