import time


class CandleEngine:
    """
    Builds OHLC candles from live price ticks.

    Default timeframe:
    15 minutes
    """

    def __init__(self, timeframe=900):

        self.timeframe = timeframe

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


            completed = candle.copy()


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



    def latest(self):

        if not self.completed_candles:

            return None


        return self.completed_candles[-1]



    def status(self):

        """
        Returns current candle progress.
        """

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
