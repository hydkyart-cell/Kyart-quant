from data.historical_data import HistoricalDataLoader
from backtesting.backtester import Backtester
from analytics.indicators import Indicators
from backtesting.trade_report import TradeReport
from backtesting.performance import PerformanceAnalyzer
from backtesting.analytics import BacktestAnalytics
from backtesting.equity_curve import EquityCurve


print("\n=== KYART QUANT BACKTEST ===")


loader = HistoricalDataLoader()

candles = loader.load(
    limit=300
)


print(
    f"Loaded {len(candles)} candles"
)


prices = [
    candle.close
    for candle in candles
]


indicator_data = []


for i in range(len(prices)):

    history = prices[:i+1]

    indicator_data.append({

        "sma":
            Indicators.sma(
                history,
                14
            ),

        "ema":
            Indicators.ema(
                history,
                14
            ),

        "volatility":
            Indicators.volatility(
                history,
                14
            )

    })


backtester = Backtester()


results = backtester.run(
    candles,
    indicator_data
)


portfolio = backtester.portfolio


TradeReport(
    portfolio.trades
).display()



performance = PerformanceAnalyzer(
    results,
    portfolio.trades
)


print("\n=== PERFORMANCE ===")

for key, value in performance.report().items():

    print(
        f"{key}: {value}"
    )



analytics = BacktestAnalytics(
    portfolio.trades,
    results
)


print("\n=== QUANT ANALYTICS ===")

for key, value in analytics.report().items():

    print(
        f"{key}: {value}"
    )



curve = EquityCurve(
    results
)


print("\n=== EQUITY CURVE ===")

for key, value in curve.summary().items():

    print(
        f"{key}: {value}"
    )
