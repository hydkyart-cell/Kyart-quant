import requests
import time


class BinanceHistoryConnector:
    """
    Binance REST historical candle connector.

    Supports pagination so KQ can load more than
    Binance's 1000-candle single-request limit.
    """

    BASE_URL = "https://api.binance.com/api/v3/klines"

    def get_klines(
        self,
        symbol="BTCUSDT",
        interval="15m",
        limit=1000
    ):

        symbol = symbol.upper()

        all_candles = []

        remaining = limit

        end_time = None

        while remaining > 0:

            batch_limit = min(
                remaining,
                1000
            )

            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": batch_limit
            }

            if end_time is not None:

                params["endTime"] = end_time


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

                    break

                except requests.exceptions.RequestException as error:

                    print(
                        f"Binance connection attempt "
                        f"{attempt + 1}/{attempts} failed"
                    )

                    if attempt < attempts - 1:

                        time.sleep(3)

                    else:

                        raise error


            if not raw_data:

                break


            batch = []

            for item in raw_data:

                batch.append({

                    "timestamp": item[0],

                    "open": float(item[1]),

                    "high": float(item[2]),

                    "low": float(item[3]),

                    "close": float(item[4]),

                    "volume": float(item[5])

                })


            all_candles = batch + all_candles

            remaining -= len(batch)


            if len(batch) < batch_limit:

                break


            oldest_timestamp = batch[0]["timestamp"]

            end_time = oldest_timestamp - 1


            time.sleep(0.15)


        return all_candles[-limit:]
