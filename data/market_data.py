import random
from datetime import datetime

def get_latest_price(symbol="EURUSD"):
    """
    Mock market data generator (temporary)
    """
    base_prices = {
        "EURUSD": 1.10,
        "GBPUSD": 1.27,
        "USDJPY": 150.0
    }

    base = base_prices.get(symbol, 1.0)

    # simulate tiny market movement
    change = random.uniform(-0.001, 0.001)
    price = round(base + change, 5)

    return {
        "symbol": symbol,
        "price": price,
        "timestamp": datetime.utcnow().isoformat()
    }
