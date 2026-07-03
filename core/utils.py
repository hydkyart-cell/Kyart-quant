from datetime import datetime
import uuid


class Utils:

    @staticmethod
    def timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())[:8]

    @staticmethod
    def banner():
        print("=" * 45)
        print("        KYART QUANT FOUNDATION")
        print("=" * 45)


if __name__ == "__main__":
    Utils.banner()
    print("Time :", Utils.timestamp())
    print("ID   :", Utils.generate_id())
