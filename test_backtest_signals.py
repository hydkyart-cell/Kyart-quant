from data.historical_data import HistoricalDataLoader
from analytics.indicators import Indicators
from analytics.atr import ATR
from core.decision_engine import DecisionEngine


print("\n=== KQ BACKTEST SIGNAL DIAGNOSTIC ===")


loader = HistoricalDataLoader()

candles = loader.load(
    symbol="BTCUSDT",
    interval="15m",
    limit=300
)


print(f"Loaded candles: {len(candles)}")


prices = []

atr_engine = ATR(
    period=14
)

decision = DecisionEngine()

previous_close = None

signal_counts = {}

examples = []


for candle in candles:

    prices.append(
        candle.close
    )


    sma = Indicators.sma(
        prices,
        14
    )

    ema = Indicators.ema(
        prices,
        14
    )

    ema200 = Indicators.ema(
        prices,
        200
    )

    atr = atr_engine.update(
        candle.high,
        candle.low,
        previous_close
    )


    market_data = {

        "price": candle.close,

        "sma": sma,

        "ema": ema,

        "ema200": ema200,

        "atr": atr,

        "candle": candle

    }


    signal = decision.decide(
        market_data
    )


    signal_counts[signal] = (
        signal_counts.get(signal, 0) + 1
    )


    if signal != "HOLD" and len(examples) < 10:

        examples.append({

            "time": candle.timestamp,

            "price": round(
                candle.close,
                2
            ),

            "sma": round(
                sma,
                2
            ) if sma is not None else None,

            "ema": round(
                ema,
                2
            ) if ema is not None else None,

            "ema200": round(
                ema200,
                2
            ) if ema200 is not None else None,

            "atr": round(
                atr,
                2
            ) if atr is not None else None,

            "signal": signal

        })


    previous_close = candle.close


print("\n=== SIGNAL COUNTS ===")

for signal, count in signal_counts.items():

    print(
        f"{signal}: {count}"
    )


print("\n=== NON-HOLD EXAMPLES ===")

if not examples:

    print("No non-HOLD signals generated.")

else:

    for example in examples:

        print(example)


print("\n=== END DIAGNOSTIC ===")
