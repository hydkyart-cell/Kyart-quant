import time
from datetime import datetime

from core.models.candle import Candle


class CandleEngine:
    """
    Builds OHLC candles from live price ticks.

    Default timeframe:
    15 minutes
    """

    def __init__(self, timeframe=900, symbol="BTCUSDT"):

        self.timeframe = timeframe
        self.symbol = symbol

        self.current_candle = None
        self.completed_candles = []


    def update(self, price):

        now = time.time()


        if self.current_candle is None:

            self.current_candle = {

                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "start_time": now

            }

            return None



        candle = self.current_candle


        candle["high"] = max(
            candle["high"],
            price
        )

        candle["low"] = min(
            candle["low"],
            price
        )

        candle["close"] = price



        if now - candle["start_time"] >= self.timeframe:


            completed = Candle(

                symbol=self.symbol,
                timeframe=f"{self.timeframe // 60}m",

                timestamp=datetime.fromtimestamp(
                    candle["start_time"]
                ),

                open=candle["open"],
                high=candle["high"],
                low=candle["low"],
                close=candle["close"],
                volume=0

            )


            self.completed_candles.append(
                completed
            )


            self.current_candle = {

                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "start_time": now

            }


            return completed



        return None



    def load_history(self, candles):

        self.completed_candles.extend(candles)



    def latest(self):

        if not self.completed_candles:

            return None


        return self.completed_candles[-1]



    def status(self):

        if self.current_candle is None:

            return {

                "state": "WAITING",
                "remaining": self.timeframe

            }


        elapsed = (
            time.time()
            -
            self.current_candle["start_time"]
        )


        remaining = max(
            0,
            self.timeframe - elapsed
        )


        return {

            "state": "BUILDING",

            "remaining": int(
                remaining
            )

        }
