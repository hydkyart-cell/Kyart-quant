from data.historical_data import HistoricalDataLoader
from backtesting.backtester import Backtester
from analytics.indicators import Indicators
from backtesting.trade_report import TradeReport
from backtesting.performance import PerformanceAnalyzer
from backtesting.analytics import BacktestAnalytics
from backtesting.equity_curve import EquityCurve
from backtesting.equity_export import EquityExporter


print("\n=== KYART QUANT BACKTEST ===")


loader = HistoricalDataLoader()

candles = loader.load(
    symbol="BTCUSDT",
    interval="15m",
    limit=300
)


print(
    f"Loaded {len(candles)} candles"
)


prices = []

indicator_data = []


for candle in candles:

    prices.append(
        candle.close
    )

    indicator_data.append({

        "sma": Indicators.sma(
            prices,
            14
        ),

        "ema": Indicators.ema(
            prices,
            14
        ),

        "volatility": Indicators.volatility(
            prices,
            14
        )

    })


backtester = Backtester(
    starting_cash=10000
)


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



exporter = EquityExporter(
    results
)


file = exporter.export_csv()


print(
    "\nEquity exported:",
    file
)
