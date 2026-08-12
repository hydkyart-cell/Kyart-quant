from data.historical_data import HistoricalDataLoader
from backtesting.backtester import Backtester
from analytics.indicators import Indicators
from analytics.atr import ATR
from backtesting.trade_report import TradeReport
from backtesting.performance import PerformanceAnalyzer
from backtesting.analytics import BacktestAnalytics
from backtesting.equity_curve import EquityCurve
from backtesting.equity_export import EquityExporter
from backtesting.entry_diagnostics import EntryDiagnostics


print("\n=== KYART QUANT BACKTEST ===")


# =========================================================
# LOAD HISTORICAL DATA
# =========================================================

loader = HistoricalDataLoader()

candles = loader.load(
    symbol="BTCUSDT",
    interval="15m",
    limit=3000
)

print(
    f"Loaded {len(candles)} candles"
)


# =========================================================
# BUILD INDICATORS
# =========================================================

prices = []

indicator_data = []

atr_engine = ATR(
    period=14
)

previous_close = None


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

    volatility = Indicators.volatility(
        prices,
        14
    )

    atr = atr_engine.update(
        candle.high,
        candle.low,
        previous_close
    )

    indicator_data.append({

        "sma": sma,

        "ema": ema,

        "ema200": ema200,

        "atr": atr,

        "volatility": volatility

    })

    previous_close = candle.close


# =========================================================
# RUN BACKTEST
# =========================================================

backtester = Backtester(
    starting_cash=10000
)

results = backtester.run(
    candles,
    indicator_data
)

portfolio = backtester.portfolio


# =========================================================
# EXECUTION DIAGNOSTICS
# =========================================================

print("\n=== EXECUTION DIAGNOSTICS ===")

for key, value in (
    backtester.report_diagnostics().items()
):

    print(
        f"{key}: {value}"
    )


# =========================================================
# TRADE HISTORY
# =========================================================

print("\n=== TRADE HISTORY ===")

TradeReport(
    portfolio.trades
).display()


# =========================================================
# ENTRY QUALITY DIAGNOSTICS
# =========================================================

EntryDiagnostics(
    portfolio.trades
).display()


# =========================================================
# PERFORMANCE
# =========================================================

performance = PerformanceAnalyzer(
    portfolio.trades
)

print("\n=== PERFORMANCE ===")

print(
    f"Total Profit: "
    f"{performance.total_profit():.2f}"
)

print(
    f"Win Rate: "
    f"{performance.win_rate():.2f}%"
)

print(
    f"Profit Factor: "
    f"{performance.profit_factor():.2f}"
)

print(
    f"Expectancy: "
    f"{performance.expectancy():.2f}"
)

print(
    f"Max Drawdown: "
    f"{performance.max_drawdown():.2f}"
)


# =========================================================
# QUANT ANALYTICS
# =========================================================

analytics = BacktestAnalytics(
    portfolio.trades,
    results
)

print("\n=== QUANT ANALYTICS ===")

for key, value in analytics.report().items():

    print(
        f"{key}: {value}"
    )


# =========================================================
# EQUITY CURVE
# =========================================================

curve = EquityCurve(
    results
)

print("\n=== EQUITY CURVE ===")

for key, value in curve.summary().items():

    print(
        f"{key}: {value}"
    )


# =========================================================
# EXPORT
# =========================================================

exporter = EquityExporter(
    results
)

file = exporter.export_csv()

print(
    "\nEquity exported:",
    file
)
