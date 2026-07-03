import time

from core.market_engine import MarketEngine

engine = MarketEngine("btcusdt")

engine.start()

while True:

    if engine.is_connected():

        print(
            "Price:",
            engine.get_latest_price(),
            "History:",
            len(engine.get_price_history())
        )

    time.sleep(1)
