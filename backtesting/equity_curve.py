class EquityCurve:
    """
    Tracks portfolio equity progression during backtests.
    """

    def __init__(self, results):

        self.results = results


    def values(self):

        return [
            result["equity"]
            for result in self.results
        ]


    def starting_equity(self):

        if not self.results:
            return 0

        return self.results[0]["equity"]


    def final_equity(self):

        if not self.results:
            return 0

        return self.results[-1]["equity"]


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
                )

        }
