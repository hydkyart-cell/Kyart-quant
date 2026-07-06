import requests

from config import TOKEN, CHAT_ID


class TelegramNotifier:

    def __init__(self, token=TOKEN, chat_id=CHAT_ID):

        self.token = token
        self.chat_id = chat_id

        self.url = (
            f"https://api.telegram.org/"
            f"bot{self.token}/sendMessage"
        )


    def send(self, message):

        try:

            response = requests.post(
                self.url,
                data={
                    "chat_id": self.chat_id,
                    "text": message
                },
                timeout=10
            )

            return response.json()


        except Exception as e:

            print("Telegram error:", e)

            return None
