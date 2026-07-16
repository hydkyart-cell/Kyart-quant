from data.historical_data import HistoricalDataLoader
from analytics.indicators import Indicators
from backtesting.backtester import Backtester
from backtesting.performance import PerformanceAnalyzer
from backtesting.trade_report import TradeReport


print("=== KYART QUANT BACKTEST ===")


loader = HistoricalDataLoader()

candles = loader.load()


print(f"Loaded {len(candles)} candles")


indicator_data = []

prices = []


for candle in candles:

    prices.append(candle.close)


    indicator_data.append({

        "sma": Indicators.sma(
            prices,
            20
        ),

        "ema": Indicators.ema(
            prices,
            20
        ),

        "volatility": Indicators.volatility(
            prices,
            20
        )

    })


backtester = Backtester(
    starting_cash=10000
)


results = backtester.run(
    candles,
    indicator_data
)


trades = backtester.portfolio.trades


TradeReport(
    trades
).display()


performance = PerformanceAnalyzer(
    results,
    trades
)


print("\n=== PERFORMANCE ===")


for key, value in performance.report().items():

    print(f"{key}: {value}")
