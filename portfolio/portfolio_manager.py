class PortfolioManager:

    def __init__(self, starting_cash=10000):

        self.portfolio = {
            "cash": starting_cash,
            "position": 0,
            "average_price": 0,
            "equity": starting_cash,
            "realized": 0,
            "unrealized": 0,
            "daily_loss": 0
        }


    def update_position(self, quantity, price):

        old_position = self.portfolio["position"]

        total_cost = (
            self.portfolio["average_price"] * old_position
        ) + (
            price * quantity
        )

        new_position = old_position + quantity


        if new_position != 0:
            self.portfolio["average_price"] = (
                total_cost / new_position
            )
        else:
            self.portfolio["average_price"] = 0


        self.portfolio["position"] = new_position


    def update_equity(self, price):

        position_value = (
            self.portfolio["position"] * price
        )

        self.portfolio["equity"] = (
            self.portfolio["cash"] + position_value
        )


    def get_portfolio(self):

        return self.portfolio
