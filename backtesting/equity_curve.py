class EquityCurve:
    """
    Tracks portfolio equity progression during backtests.
    """

    def __init__(
        self,
        results,
        starting_equity=10000
    ):

        self.results = results
        self.starting_equity_value = starting_equity


    def values(self):

        values = [
            self.starting_equity_value
        ]

        values.extend(
            result["equity"]
            for result in self.results
        )

        return values


    def starting_equity(self):

        return self.starting_equity_value


    def final_equity(self):

        values = self.values()

        if not values:
            return 0

        return values[-1]


    def peak_equity(self):

        values = self.values()

        if not values:
            return 0

        return max(values)


    def lowest_equity(self):

        values = self.values()

        if not values:
            return 0

        return min(values)


    def total_return_percent(self):

        starting = self.starting_equity()
        ending = self.final_equity()

        if starting == 0:
            return 0

        return (
            (ending - starting)
            / starting
            * 100
        )


    def summary(self):

        return {

            "starting_equity":
                round(
                    self.starting_equity(),
                    2
                ),

            "final_equity":
                round(
                    self.final_equity(),
                    2
                ),

            "peak_equity":
                round(
                    self.peak_equity(),
                    2
                ),

            "lowest_equity":
                round(
                    self.lowest_equity(),
                    2
                ),

            "total_return_percent":
                round(
                    self.total_return_percent(),
                    2
                )

        }
