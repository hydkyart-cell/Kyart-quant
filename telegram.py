import requests


class TelegramBot:

    def __init__(self, token, chat_id):

        self.url = (
            f"https://api.telegram.org/bot{token}/sendMessage"
        )

        self.chat_id = chat_id


    def send(self, text):

        try:

            requests.post(
                self.url,
                data={
                    "chat_id": self.chat_id,
                    "text": text
                },
                timeout=10
            )

        except Exception as e:

            print(
                f"[TELEGRAM ERROR] {e}"
            )
