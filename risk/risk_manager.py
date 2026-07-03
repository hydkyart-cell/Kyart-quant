def apply_risk(signal, market_data):
    """
    Simple risk filter.
    Prevents over-trading and adds basic sanity.
    """

    price = market_data["price"]

    # fake risk rule: avoid trading too close to baseline
    baseline = 1.10
    distance = abs(price - baseline)

    if distance < 0.0005:
        return "NO_TRADE"

    return signal
