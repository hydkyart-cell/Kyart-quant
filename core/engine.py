import time
from datetime import datetime

from analytics.indicators import Indicators
from core.price_buffer import PriceBuffer
from core.candle_engine import CandleEngine
from core.decision_engine import DecisionEngine
from execution.paper_trader import PaperTrader
from risk.risk_engine import RiskEngine


class TradingEngine:

    def __init__(self):

        self.buffer = PriceBuffer()

        self.candle = CandleEngine()
        self.decision = DecisionEngine()

        self.indicators = Indicators()
        self.risk = RiskEngine()
        self.trader = PaperTrader()

        self.last_signal = None

        self.last_notification = None
        self.notification_interval = 15 * 60


    def update(self, price):

        # Store incoming price
        self.buffer.add(price)

        prices = self.buffer.get_prices()


        # Indicators
        sma = self.indicators.sma(prices)
        ema = self.indicators.ema(prices)
        volatility = self.indicators.volatility(prices)


        # Build 15 minute candle
        candle = self.candle.update(price)


        market_data = {

            "price": price,

            "sma": sma,

            "ema": ema,

            "volatility": volatility,

            "candle": candle,

            "timestamp": datetime.utcnow().isoformat()

        }


        # Conservative decision engine
        signal = self.decision.decide(
            market_data
        )


        action = "HOLD"


        portfolio = self.trader.get_portfolio()


        # Risk controlled execution

        if signal == "BUY":

            if self.risk.allow_trade(
                market_data,
                portfolio
            ):

                self.trader.buy(price)

                action = "OPEN_LONG"


        elif signal == "SELL":

            if self.risk.allow_trade(
                market_data,
                portfolio
            ):

                self.trader.sell(price)

                action = "OPEN_SHORT"


        # Refresh portfolio

        portfolio = self.trader.get_portfolio()


        # Notification timer

        current_time = time.time()

        send_notification = False


        if (
            self.last_notification is None
            or current_time - self.last_notification >= self.notification_interval
        ):

            send_notification = True

            self.last_notification = current_time


        return {

            "price": price,

            "signal": signal,

            "action": action,

            "sma": sma,

            "ema": ema,

            "volatility": volatility,

            "candle": candle,

            "portfolio": portfolio,

            "send_notification": send_notification

        }
