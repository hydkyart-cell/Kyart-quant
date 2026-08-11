from strategy.signal_engine import SignalEngine

engine = SignalEngine()

price = 65000
sma = 64500
ema = 64800
ema200 = 62000
atr = 500

signal = engine.generate(
    price,
    sma,
    ema,
    ema200,
    atr
)

print("Signal:", signal)
