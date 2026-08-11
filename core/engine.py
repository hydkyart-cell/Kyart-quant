import time
from datetime import datetime

from analytics.indicators import Indicators
from analytics.atr import ATR
from core.price_buffer import PriceBuffer
from core.candle_engine import CandleEngine
from core.decision_engine import DecisionEngine
from execution.paper_trader import PaperTrader
from risk.risk_engine import RiskEngine
from data.historical_data import HistoricalDataLoader


class TradingEngine:

    def __init__(self):

        self.buffer = PriceBuffer()

        self.candles = CandleEngine(
            timeframe=900,
            symbol="BTCUSDT"
        )

        self.indicators = Indicators()

        self.atr = ATR(period=14)

        self.load_history()

        self.decision = DecisionEngine()

        self.risk = RiskEngine()

        self.trader = PaperTrader()

        self.minimum_candles = 20

        self.last_notification = None

        self.notification_interval = 15 * 60


    def load_history(self):

        try:

            loader = HistoricalDataLoader()

            candles = loader.load(
                symbol="BTCUSDT",
                interval="15m",
                limit=300
            )

            closes = []

            for candle in candles:

                if hasattr(candle, "close"):

                    closes.append(
                        candle.close
                    )

                else:

                    closes.append(
                        candle["close"]
                    )

            self.buffer.load(closes)

            self.candles.load_history(candles)

            # Warm up ATR using historical OHLC data.
            for i in range(1, len(candles)):

                self.atr.update(
                    candles[i].high,
                    candles[i].low,
                    candles[i - 1].close
                )

            print(
                f"[HISTORY] Loaded {len(candles)} candles"
            )

        except Exception as error:

            print(
                f"[HISTORY] Failed: {error}"
            )


    def update(self, price):

        completed_candle = self.candles.update(price)

        portfolio = self.trader.get_portfolio()

        position = portfolio["position"]

        if position > 0:

            action = "HOLD_LONG"

        else:

            action = "WAIT_CANDLE"


        signal = "HOLD"

        sma = None

        ema = None

        ema200 = None

        atr = None

        volatility = None


        if completed_candle:

            close_price = completed_candle.close

            self.buffer.add(
                close_price
            )

            previous_candle = None

            if len(self.candles.completed_candles) >= 2:

                previous_candle = (
                    self.candles.completed_candles[-2]
                )

            if previous_candle is not None:

                atr = self.atr.update(
                    completed_candle.high,
                    completed_candle.low,
                    previous_candle.close
                )

        else:

            # Use the most recently calculated ATR
            # while the current candle is still building.
            if self.atr.values:

                atr = sum(
                    self.atr.values
                ) / len(
                    self.atr.values
                )


        candle_count = len(
            self.buffer.get_prices()
        )


        if candle_count >= self.minimum_candles:

            prices = self.buffer.get_prices()

            sma = self.indicators.sma(
                prices
            )

            ema = self.indicators.ema(
                prices
            )

            ema200 = self.indicators.ema(
                prices,
                period=200
            )

            volatility = self.indicators.volatility(
                prices
            )


            market_data = {

                "price": price,

                "sma": sma,

                "ema": ema,

                "ema200": ema200,

                "atr": atr,

                "volatility": volatility,

                "candle": completed_candle,

                "timestamp": datetime.utcnow().isoformat()

            }


            signal = self.decision.decide(
                market_data
            )


            if signal == "BUY":

                if position == 0:

                    if self.risk.allow_trade(
                        market_data,
                        portfolio
                    ):

                        self.trader.buy(
                            price
                        )

                        action = "OPEN_LONG"


            elif signal == "SELL":

                if position > 0:

                    action = "HOLD_LONG"


        else:

            action = "WAIT_WARMUP"


        portfolio = self.trader.get_portfolio()

        current_time = time.time()

        send_notification = False


        if (
            self.last_notification is None
            or current_time - self.last_notification
            >= self.notification_interval
        ):

            send_notification = True

            self.last_notification = current_time


        candle_status = self.candles.status()


        return {

            "price": price,

            "signal": signal,

            "action": action,

            "sma": sma,

            "ema": ema,

            "ema200": ema200,

            "atr": atr,

            "volatility": volatility,

            "candle_count": candle_count,

            "candle_status": candle_status,

            "portfolio": portfolio,

            "send_notification": send_notification

        }
