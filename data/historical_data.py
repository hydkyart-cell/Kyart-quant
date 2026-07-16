from datetime import datetime

from connectors.binance_history import BinanceHistoryConnector
from core.models.candle import Candle


class HistoricalDataLoader:
    """
    Loads historical market candles from Binance
    and converts them into KQ Candle objects.
    """

    def __init__(self):
        self.connector = BinanceHistoryConnector()


    def load(self, symbol="BTCUSDT", interval="15m", limit=300):
        """
        Fetch historical candles and normalize them.
        """

        raw_candles = self.connector.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
        )


        candles = []


        for candle in raw_candles:

            if isinstance(candle, Candle):

                candles.append(candle)

                continue


            candles.append(
                Candle(

                    symbol=symbol,

                    timeframe=interval,

                    timestamp=datetime.fromtimestamp(
                        candle.get(
                            "timestamp",
                            datetime.utcnow().timestamp()
                        )
                    ),

                    open=float(
                        candle["open"]
                    ),

                    high=float(
                        candle["high"]
                    ),

                    low=float(
                        candle["low"]
                    ),

                    close=float(
                        candle["close"]
                    ),

                    volume=float(
                        candle.get(
                            "volume",
                            0
                        )
                    )

                )
            )


        return candles



if __name__ == "__main__":

    loader = HistoricalDataLoader()

    candles = loader.load()

    print(f"Loaded {len(candles)} candles")

    print(candles[0])
