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


    def load(
        self,
        symbol="BTCUSDT",
        interval="15m",
        limit=300
    ):

        raw_candles = self.connector.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit
        )

        candles = []

        for candle in raw_candles:

            if isinstance(candle, Candle):

                candles.append(candle)

                continue


            timestamp_ms = candle.get(
                "time"
            )

            if timestamp_ms is None:

                timestamp_ms = candle.get(
                    "timestamp"
                )


            if timestamp_ms is None:

                raise ValueError(
                    "Historical candle has no timestamp"
                )


            timestamp = datetime.fromtimestamp(
                timestamp_ms / 1000
            )


            candles.append(
                Candle(

                    symbol=symbol,

                    timeframe=interval,

                    timestamp=timestamp,

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

    print(
        f"Loaded {len(candles)} candles"
    )

    if candles:

        print(
            "First:",
            candles[0]
        )

        print(
            "Last:",
            candles[-1]
        )
