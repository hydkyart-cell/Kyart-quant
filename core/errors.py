from datetime import datetime


class ErrorHandler:

    @staticmethod
    def handle(error):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[ERROR] [{now}] {error}")


if __name__ == "__main__":
    try:
        number = 10 / 0
    except Exception as e:
        ErrorHandler.handle(e)
