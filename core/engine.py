import time
from datetime import datetime

from analytics.indicators import Indicators
from core.price_buffer import PriceBuffer
from execution.paper_trader import PaperTrader
from risk.risk_engine import RiskEngine
from strategy.signal_engine import SignalEngine


class TradingEngine:

    def __init__(self):

        self.buffer = PriceBuffer()
        self.signals = SignalEngine()
        self.risk = RiskEngine()
        self.trader = PaperTrader()

        # 15-minute execution gate
        self.timeframe_seconds = 15 * 60
        self.last_decision_time = 0

        # candle-like storage (tick aggregation)
        self.candle_prices = []

    def _can_trade(self):
        return (time.time() - self.last_decision_time) >= self.timeframe_seconds

    def _update_candle(self, price):
        self.candle_prices.append(price)

        # prevent memory explosion
        if len(self.candle_prices) > 2000:
            self.candle_prices.pop(0)

    def _get_window(self):
        return self.candle_prices[-20:]

    def update(self, price):

        self.buffer.add(price)
        self._update_candle(price)

        window = self._get_window()

        sma = Indicators.sma(window, 20)
        ema = Indicators.ema(window, 20)
        vol = Indicators.volatility(window, 20)

        signal = self.signals.generate(price, sma, ema)

        action = "WAITING"

        # 15-minute execution rule
        if self._can_trade():

            if signal in ("BUY", "STRONG BUY"):

                result = self.risk.validate_trade(
                    cash=self.trader.cash,
                    price=price,
                    quantity=1,
                )

                if result.approved:
                    ok, action = self.trader.buy(price)
                else:
                    action = result.reason

            elif signal in ("SELL", "STRONG SELL"):

                ok, action = self.trader.sell(price)

            else:
                action = "NO TRADE"

            self.last_decision_time = time.time()

        return {
            "price": price,
            "sma": sma,
            "ema": ema,
            "volatility": vol,
            "signal": signal,
            "action": action,

            # 🧠 TIME INTEGRATION (what you asked for)
            "timestamp": datetime.utcnow().isoformat(),
            "seconds_since_trade": round(time.time() - self.last_decision_time, 2),

            "portfolio": self.trader.summary(price),
        }
