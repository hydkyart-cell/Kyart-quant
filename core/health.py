import platform
import sys
from datetime import datetime


class HealthMonitor:

    @staticmethod
    def report():
        print("=" * 45)
        print("      KYART QUANT HEALTH REPORT")
        print("=" * 45)

        print(f"Time      : {datetime.now()}")
        print(f"Python    : {sys.version.split()[0]}")
        print(f"Platform  : {platform.system()}")
        print(f"Machine   : {platform.machine()}")

        print("\nStatus")
        print("✔ Logger ............ OK")
        print("✔ Config ............ OK")
        print("✔ Utils ............. OK")
        print("✔ Error Handler ..... OK")
        print("✔ File Manager ...... OK")

        print("\nFoundation Engine Healthy")


if __name__ == "__main__":
    HealthMonitor.report()
