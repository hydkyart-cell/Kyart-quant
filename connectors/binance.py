from core.market_engine import MarketEngine
from connectors.base import MarketConnector


class BinanceConnector(MarketConnector):

    def __init__(self, symbol="btcusdt"):
        self.engine = MarketEngine(symbol)

    def start(self):
        self.engine.start()

    def stop(self):
        pass

    def latest_price(self):
        return self.engine.get_latest_price()

    def is_connected(self):
        return self.engine.is_connected()

    def history(self):
        return self.engine.get_price_history()
