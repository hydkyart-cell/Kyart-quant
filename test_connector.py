import time

from connectors.binance import BinanceConnector

market = BinanceConnector("btcusdt")

market.start()

while not market.is_connected():
    time.sleep(1)

print("Connected!")

while True:

    price = market.latest_price()

    if price:
        print(price)

    time.sleep(1)
