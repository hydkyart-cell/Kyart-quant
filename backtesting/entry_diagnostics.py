class EntryDiagnostics:

    def __init__(self, trades):
        self.trades = trades

    def display(self):

        print("\n=== ENTRY QUALITY DIAGNOSTICS ===")

        if not self.trades:
            print("No completed trades.")
            return

        total = len(self.trades)

        print(f"Completed trades: {total}")
        print()

        # -----------------------------------------------------
        # MFE / MAE
        # -----------------------------------------------------

        print("MFE / MAE")

        mfe_values = [
            float(t.get("mfe_percent", 0))
            for t in self.trades
        ]

        mae_values = [
            float(t.get("mae_percent", 0))
            for t in self.trades
        ]

        avg_mfe = sum(mfe_values) / total
        avg_mae = sum(mae_values) / total

        print(
            f"Average MFE: {avg_mfe:.2f}%"
        )

        print(
            f"Average MAE: {avg_mae:.2f}%"
        )

        print()

        # -----------------------------------------------------
        # MFE THRESHOLDS
        # -----------------------------------------------------

        thresholds = [
            0.5,
            1.0,
            1.5,
            2.0,
            3.0
        ]

        print(
            "Maximum favorable excursion reach:"
        )

        for threshold in thresholds:

            reached = sum(
                1
                for t in self.trades
                if float(
                    t.get("mfe_percent", 0)
                ) >= threshold
            )

            percentage = (
                reached /
                total *
                100
            )

            print(
                f"+{threshold:.1f}%: "
                f"{reached}/{total} "
                f"({percentage:.1f}%)"
            )

        print()

        # -----------------------------------------------------
        # TRADE-BY-TRADE
        # -----------------------------------------------------

        print(
            "Trade-by-trade entry quality:"
        )

        for i, trade in enumerate(
            self.trades,
            start=1
        ):

            metadata = trade.get(
                "entry_metadata",
                {}
            )

            print(
                f"\nTrade #{i}"
            )

            print(
                "Signal: "
                f"{metadata.get('signal', 'N/A')}"
            )

            print(
                "Entry: "
                f"{float(trade.get('entry', 0)):.4f}"
            )

            print(
                "Profit: "
                f"{float(trade.get('profit', 0)):.2f}"
            )

            print(
                "Exit: "
                f"{trade.get('reason', 'N/A')}"
            )

            print(
                "MFE: "
                f"{float(trade.get('mfe_percent', 0)):.2f}%"
            )

            print(
                "MAE: "
                f"{float(trade.get('mae_percent', 0)):.2f}%"
            )

            print(
                "MFE Capture: "
                f"{float(trade.get('mfe_capture_percent', 0)):.2f}%"
            )

            print(
                "ATR: "
                f"{float(metadata.get('atr', 0)):.4f}"
            )

            distance = metadata.get(
                "ema200_distance_percent",
                metadata.get(
                    "ema200_distance_pct",
                    0
                )
            )

            print(
                "EMA200 distance: "
                f"{float(distance):.2f}%"
            )

            candle = metadata.get(
                "candle_direction",
                metadata.get(
                    "candle",
                    "N/A"
                )
            )

            print(
                "Candle: "
                f"{candle}"
            )

            holding = trade.get(
                "holding_period"
            )

            if holding is not None:

                print(
                    "Holding candles: "
                    f"{holding}"
                )
