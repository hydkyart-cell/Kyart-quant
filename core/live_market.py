import json
import websocket

SYMBOL = "btcusdt"

class LiveMarket:

    def __init__(self):
        self.price = None

    def on_message(self, ws, message):
        data = json.loads(message)
        self.price = float(data["c"])

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("Disconnected")

    def on_open(self, ws):
        print("Connected")

    def start(self):

        socket = f"wss://stream.binance.com:9443/ws/{SYMBOL}@ticker"

        ws = websocket.WebSocketApp(
            socket,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

        ws.run_forever()
