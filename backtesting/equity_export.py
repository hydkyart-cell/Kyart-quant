import csv


class EquityExporter:
    """
    Exports equity curve data for analysis.
    """


    def __init__(self, results):

        self.results = results



    def export_csv(
        self,
        filename="equity_curve.csv"
    ):

        with open(
            filename,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)


            writer.writerow(
                [
                    "timestamp",
                    "price",
                    "equity"
                ]
            )


            for result in self.results:

                writer.writerow(
                    [
                        result["timestamp"],
                        result["price"],
                        result["equity"]
                    ]
                )


        return filename
