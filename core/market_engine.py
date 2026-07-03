import json
import threading
import time
from collections import deque

import websocket


class MarketEngine:
    """
    Live Market Data Engine

    Maintains:
        - latest price
        - price history
        - connection status
    """

    def __init__(self,
                 symbol="btcusdt",
                 history_size=1000):

        self.symbol = symbol.lower()

        self.connected = False

        self.latest_price = None

        self.last_update = None

        self.prices = deque(maxlen=history_size)

        self.ws = None

    # -----------------------------
    # WebSocket Callbacks
    # -----------------------------

    def on_open(self, ws):
        self.connected = True
        print(f"[CONNECTED] {self.symbol.upper()}")

    def on_close(self, ws, status, message):
        self.connected = False
        print("[DISCONNECTED]")

    def on_error(self, ws, error):
        print(error)

    def on_message(self, ws, message):

        data = json.loads(message)

        price = float(data["c"])

        self.latest_price = price

        self.last_update = time.time()

        self.prices.append(price)

    # -----------------------------
    # Connection
    # -----------------------------

    def connect(self):

        url = (
            f"wss://stream.binance.com:9443/ws/"
            f"{self.symbol}@ticker"
        )

        self.ws = websocket.WebSocketApp(
            url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error,
        )

        self.ws.run_forever()

    def start(self):

        thread = threading.Thread(
            target=self.connect,
            daemon=True
        )

        thread.start()

    # -----------------------------
    # Public API
    # -----------------------------

    def get_latest_price(self):
        return self.latest_price

    def get_price_history(self):
        return list(self.prices)

    def is_connected(self):
        return self.connected
