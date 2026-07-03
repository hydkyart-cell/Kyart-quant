def generate_signal(market_data):
    """
    Very basic trading strategy.
    """
    price = market_data["price"]

    # naive baseline (temporary logic)
    baseline = 1.10

    if price > baseline:
        return "BUY"
    elif price < baseline:
        return "SELL"
    else:
        return "HOLD"
