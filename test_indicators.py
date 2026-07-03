from analytics.indicators import Indicators

prices = [
    100,101,102,103,104,
    105,106,107,108,109,
    110,111,112,113,114,
    115,116,117,118,119
]

print("SMA:", Indicators.sma(prices, 10))
print("EMA:", round(Indicators.ema(prices, 10), 2))
print("Volatility:", round(Indicators.volatility(prices, 10), 2))
