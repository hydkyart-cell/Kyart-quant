class TradeReport:
    """
    Displays individual backtest trades.
    """

    def __init__(self, trades):

        self.trades = trades


    def display(self):

        print("\n=== TRADE HISTORY ===")


        if not self.trades:

            print("No trades executed")

            return


        for index, trade in enumerate(
            self.trades,
            start=1
        ):

            print(
                f"""
Trade #{index}

Entry:  {trade['entry']}
Exit:   {trade['exit']}
Profit: {round(trade['profit'], 2)}
Reason: {trade.get('reason', 'UNKNOWN')}
"""
            )
