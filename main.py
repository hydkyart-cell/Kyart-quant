from rich.live import Live
from rich.table import Table
import time

from core.market_data import get_market_snapshot
from core.strategy import SimpleStrategy
from risk.risk_engine import RiskEngine

strategy = SimpleStrategy(window=5)
risk = RiskEngine()


def render_dashboard(data, signal, account):

    table = Table(title="KYART QUANT TERMINAL")

    table.add_column("Metric")
    table.add_column("Value")

    spread = round(data["ask"] - data["bid"], 4)

    table.add_row("Symbol", data["symbol"])
    table.add_row("Price", str(data["price"]))
    table.add_row("Bid", str(data["bid"]))
    table.add_row("Ask", str(data["ask"]))
    table.add_row("Spread", str(spread))
    table.add_row("Volume", str(data["volume"]))

    table.add_row("")

    table.add_row("Signal", signal)
    table.add_row("Action", account["action"])
    table.add_row("Position", str(account["position"]))
    table.add_row("Balance", f"${account['balance']:.2f}")

    return table


def run():

    first = get_market_snapshot()
    signal = strategy.update(first["price"])
    account = risk.process_signal(signal, first["price"])

    with Live(render_dashboard(first, signal, account),
              refresh_per_second=4,
              screen=True) as live:

        while True:

            market = get_market_snapshot()

            signal = strategy.update(market["price"])

            account = risk.process_signal(signal, market["price"])

            live.update(render_dashboard(market, signal, account))

            time.sleep(0.25)


if __name__ == "__main__":
    run()
