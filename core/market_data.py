import random

_last_price = 100

def get_market_snapshot():
    global _last_price

    # random walk (more realistic than pure chaos)
    change = random.uniform(-0.8, 0.8)
    _last_price = max(1, _last_price + change)

    bid = _last_price - random.uniform(0.05, 0.2)
    ask = _last_price + random.uniform(0.05, 0.2)

    return {
        "symbol": "KYARTUSD",
        "price": round(_last_price, 2),
        "volume": random.randint(1000, 5000),
        "bid": round(bid, 2),
        "ask": round(ask, 2),
    }
