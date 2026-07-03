import time

from core.market_engine import MarketEngine
from core.price_buffer import PriceBuffer
from analytics.indicators import Indicators

engine = MarketEngine("btcusdt")
buffer = PriceBuffer(max_size=100)

engine.start()

print("Waiting for live market data...")

while not engine.is_connected():
    time.sleep(0.5)

print("Connected!\n")

while True:

    price = engine.get_latest_price()

    if price is not None:

        buffer.add(price)

        prices = buffer.get_prices()

        sma = Indicators.sma(prices, 10)
        ema = Indicators.ema(prices, 10)
        vol = Indicators.volatility(prices, 10)

        print("-" * 40)
        print(f"Price      : {price}")

        if sma is not None:
            print(f"SMA (10)   : {sma:.2f}")
            print(f"EMA (10)   : {ema:.2f}")
            print(f"Volatility : {vol:.4f}")
        else:
            print("Collecting data...")

    time.sleep(1)
