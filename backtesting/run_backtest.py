from data.historical_data import HistoricalDataLoader
from backtesting.backtester import Backtester
from backtesting.trade_report import TradeReport
from backtesting.performance import PerformanceAnalyzer
from backtesting.analytics import BacktestAnalytics
from analytics.indicators import Indicators


print("\n=== KYART QUANT BACKTEST ===")


# Load historical candles

loader = HistoricalDataLoader()

candles = loader.load()

print(f"Loaded {len(candles)} candles")


# Prepare indicator data

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



# Run backtest

backtester = Backtester()

results = backtester.run(
    candles,
    indicator_data
)


trades = backtester.portfolio.trades



# Trade report

report = TradeReport(
    trades
)

report.display()



# Performance report

performance = PerformanceAnalyzer(
    results,
    trades
)


print("\n=== PERFORMANCE ===")

for key, value in performance.report().items():

    print(
        f"{key}: {value}"
    )



# Advanced analytics

analytics = BacktestAnalytics(
    trades,
    results
)


print("\n=== QUANT ANALYTICS ===")

for key, value in analytics.report().items():

    print(
        f"{key}: {value}"
    )
