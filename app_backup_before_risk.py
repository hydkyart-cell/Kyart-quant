import time

from core.market_engine import MarketEngine
from core.price_buffer import PriceBuffer
from analytics.indicators import Indicators
from strategy.signal_engine import SignalEngine
from execution.paper_trader import PaperTrader


market = MarketEngine("btcusdt")
buffer = PriceBuffer(500)
signals = SignalEngine()
trader = PaperTrader()


market.start()

print("Starting Kyart Quant...")


while not market.is_connected():
    time.sleep(0.5)


print("Connected to live market.")


last_signal = "WAIT"


while True:

    price = market.get_latest_price()

    if price is not None:


        # Risk management check
        risk_exit = trader.check_risk_exit(price)

        if risk_exit:

            print("=" * 60)
            print("RISK EXIT TRIGGERED")
            print(f"Price   : {price:.2f}")
            print(f"Portfolio: {trader.get_portfolio()}")


        buffer.add(price)

        prices = buffer.get_prices()


        sma = Indicators.sma(
            prices,
            20
        )


        ema = Indicators.ema(
            prices,
            20
        )


        ema200 = Indicators.ema(
            prices,
            200
        )


        signal = signals.generate(
            price,
            sma,
            ema,
            ema200
        )


        if signal != last_signal:


            if signal in ("BUY", "STRONG BUY"):

                action = trader.buy(price)


            elif signal in ("SELL", "STRONG SELL"):

                action = trader.sell(price)


            else:

                action = "-"



            print("=" * 60)
            print(f"Price   : {price:.2f}")
            print(f"SMA20   : {sma}")
            print(f"EMA20   : {ema}")
            print(f"EMA200  : {ema200}")
            print(f"Signal  : {signal}")
            print(f"Action  : {action}")
            print(f"Portfolio: {trader.get_portfolio()}")


            last_signal = signal


    time.sleep(1)
