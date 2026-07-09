import time

from rich.live import Live
from rich.table import Table

from core.market_engine import MarketEngine
from core.engine import TradingEngine
from notifications import TelegramNotifier


class KyartApp:

    def __init__(self):

        self.market = MarketEngine(
            symbol="btcusdt"
        )

        self.engine = TradingEngine()

        self.telegram = TelegramNotifier()

        self.last_sent_event = None



    def start_market(self):

        self.market.start()



    def render(self, snapshot):

        table = Table(
            title="KYART QUANT LIVE TERMINAL"
        )

        table.add_column("Metric")
        table.add_column("Value")


        table.add_row(
            "Price",
            str(snapshot["price"])
        )

        table.add_row(
            "Signal",
            str(snapshot["signal"])
        )

        table.add_row(
            "Action",
            str(snapshot["action"])
        )


        table.add_row("", "")


        candle_count = snapshot.get(
            "candle_count",
            0
        )


        table.add_row(
            "Candle Count",
            f"{candle_count}/20"
        )


        if candle_count < 20:

            table.add_row(
                "Market State",
                "WARMUP"
            )

        else:

            table.add_row(
                "Market State",
                "READY"
            )



        candle_status = snapshot.get(
            "candle_status",
            {}
        )


        table.add_row(
            "Candle Status",
            str(
                candle_status.get(
                    "state",
                    "UNKNOWN"
                )
            )
        )


        remaining = candle_status.get(
            "remaining",
            0
        )


        minutes = remaining // 60

        seconds = remaining % 60


        table.add_row(
            "Time Remaining",
            f"{minutes}m {seconds}s"
        )


        table.add_row("", "")


        p = snapshot["portfolio"]


        table.add_row(
            "Cash",
            str(p["cash"])
        )

        table.add_row(
            "Position",
            str(p["position"])
        )

        table.add_row(
            "Equity",
            str(p["equity"])
        )

        table.add_row(
            "Realized PnL",
            str(p["realized"])
        )

        table.add_row(
            "Unrealized PnL",
            str(p["unrealized"])
        )


        table.add_row("", "")


        table.add_row(
            "SMA",
            str(snapshot["sma"])
        )

        table.add_row(
            "EMA",
            str(snapshot["ema"])
        )

        table.add_row(
            "Volatility",
            str(snapshot["volatility"])
        )


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
                "candle_count": 0,
                "candle_status": {
                    "state": "WAITING",
                    "remaining": 0
                },
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



                snapshot = self.engine.update(
                    price
                )


                live.update(
                    self.render(snapshot)
                )



                event = snapshot["action"]


                if (
                    event != self.last_sent_event
                    and event in [
                        "OPEN_LONG",
                        "CLOSE_LONG",
                        "OPEN_SHORT",
                        "CLOSE_SHORT"
                    ]
                ):


                    self.telegram.send(
                        f"""
📊 Kyart Quant Trade Event

Action: {snapshot['action']}
Signal: {snapshot['signal']}
Price: {snapshot['price']}
"""
                    )


                    self.last_sent_event = event



                if snapshot["send_notification"]:

                    p = snapshot["portfolio"]

                    candle = snapshot.get(
                        "candle_status",
                        {}
                    )


                    self.telegram.send(
                        f"""
🟢 Kyart Quant Update

Price: {snapshot['price']}
Signal: {snapshot['signal']}
Action: {snapshot['action']}

Candle:
{candle.get('state')}
Remaining:
{candle.get('remaining')} seconds

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


                time.sleep(0.25)



if __name__ == "__main__":

    KyartApp().run()
