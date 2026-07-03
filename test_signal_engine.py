from strategy.signal_engine import SignalEngine

engine = SignalEngine()

tests = [
    (105,100,102),
    (101,100,99),
    (95,100,98),
    (92,100,99),
    (100,100,100),
]

for price,sma,ema in tests:

    signal = engine.generate(price,sma,ema)

    print(price,sma,ema,"->",signal)
