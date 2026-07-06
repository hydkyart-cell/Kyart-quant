def generate_signal(market_data):

    price = market_data["price"]

    sma = market_data.get("sma")
    ema = market_data.get("ema")

    if sma is None or ema is None:
        return "HOLD"

    if price > sma and price > ema:
        return "BUY"

    elif price < sma and price < ema:
        return "SELL"

    return "HOLD"
