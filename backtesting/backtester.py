from core.decision_engine import DecisionEngine
from backtesting.portfolio import BacktestPortfolio


class Backtester:
    """
    Replays historical candles through KQ decision logic.
    """

    def __init__(self, starting_cash=10000):

        self.decision = DecisionEngine()

        self.portfolio = BacktestPortfolio(
            starting_cash
        )

        self.results = []


    def run(self, candles, indicator_data):

        for candle, indicators in zip(
            candles,
            indicator_data
        ):

            market_data = {

                "price": candle.close,

                "sma": indicators["sma"],

                "ema": indicators["ema"],

                "volatility": indicators["volatility"],

                "candle": candle

            }


            signal = self.decision.decide(
                market_data
            )


            # Risk management exits first
            # Checks stop loss and take profit

            self.portfolio.check_exit(
                candle.close
            )


            if signal == "BUY":

                self.portfolio.buy(
                    candle.close
                )


            elif signal == "SELL":

                self.portfolio.sell(
                    candle.close,
                    reason="SIGNAL"
                )


            self.results.append({

                "timestamp": candle.timestamp,

                "price": candle.close,

                "signal": signal,

                "equity": self.portfolio.equity(
                    candle.close
                )

            })


        return self.results
