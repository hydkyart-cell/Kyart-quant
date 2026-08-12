import csv


class EquityExporter:
    """
    Exports timestamped equity curve data.
    """

    def __init__(
        self,
        results
    ):

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

            writer = csv.writer(
                file
            )

            writer.writerow([
                "timestamp",
                "price",
                "equity"
            ])

            for index, result in enumerate(
                self.results
            ):

                writer.writerow([
                    result.get(
                        "timestamp",
                        index
                    ),
                    result.get(
                        "price",
                        ""
                    ),
                    result.get(
                        "equity",
                        ""
                    )
                ])

        return filename
