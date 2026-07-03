import time

from core.market_engine import MarketEngine
from core.price_buffer import PriceBuffer
from analytics.indicators import Indicators
from strategy.signal_engine import SignalEngine
from execution.portfolio import Portfolio


market = MarketEngine("btcusdt")
buffer = PriceBuffer(500)
signals = SignalEngine()
portfolio = Portfolio(10000)

market.start()

print("Starting Kyart Quant...")

while not market.is_connected():
    time.sleep(0.5)

print("Connected to live market.")

last_signal = "WAIT"

while True:

    price = market.get_latest_price()

    if price is not None:

        buffer.add(price)

        prices = buffer.get_prices()

        sma = Indicators.sma(prices, 20)
        ema = Indicators.ema(prices, 20)

        signal = signals.generate(price, sma, ema)

        if signal != last_signal:

            if signal in ("BUY", "STRONG BUY"):
                action = portfolio.buy(price)

            elif signal in ("SELL", "STRONG SELL"):
                action = portfolio.sell(price)

            else:
                action = "-"

            print("=" * 60)
            print(f"Price   : {price:.2f}")
            print(f"SMA20   : {sma}")
            print(f"EMA20   : {ema}")
            print(f"Signal  : {signal}")
            print(f"Action  : {action}")
            print(portfolio.summary(price))

            last_signal = signal

    time.sleep(1)
