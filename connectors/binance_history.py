import requests
import time


class BinanceHistoryConnector:
    """
    Binance REST historical candle connector.
    """

    BASE_URL = "https://api.binance.com/api/v3/klines"


    def get_klines(
        self,
        symbol="BTCUSDT",
        interval="15m",
        limit=300
    ):

        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": limit
        }


        attempts = 3


        for attempt in range(attempts):

            try:

                response = requests.get(
                    self.BASE_URL,
                    params=params,
                    timeout=30
                )

                response.raise_for_status()

                raw_data = response.json()

                candles = []


                for item in raw_data:

                    candles.append({

                        "time": item[0],

                        "open": float(item[1]),

                        "high": float(item[2]),

                        "low": float(item[3]),

                        "close": float(item[4]),

                        "volume": float(item[5])

                    })


                return candles


            except requests.exceptions.RequestException as error:

                print(
                    f"Binance connection attempt {attempt + 1}/{attempts} failed"
                )

                if attempt < attempts - 1:

                    time.sleep(3)

                else:

                    raise error
