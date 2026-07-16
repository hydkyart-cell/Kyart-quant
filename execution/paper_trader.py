class PaperTrader:

    def __init__(self):

        self.portfolio = {
            "cash": 10000,
            "position": 0,
            "equity": 10000,
            "realized": 0,
            "unrealized": 0
        }

        self.average_entry_price = 0



    def buy(self, price, risk_fraction=0.95):

        cash = self.portfolio["cash"]

        amount_to_use = cash * risk_fraction


        if amount_to_use <= 0:
            return False


        quantity = amount_to_use / price


        current_position = self.portfolio["position"]


        total_cost = (
            current_position * self.average_entry_price
            +
            quantity * price
        )


        new_position = current_position + quantity


        self.average_entry_price = (
            total_cost / new_position
        )


        self.portfolio["position"] = new_position


        self.portfolio["cash"] -= (
            quantity * price
        )


        # Do not touch realized PnL here
        self.update_equity(price)

        return True



    def sell(self, price):

        position = self.portfolio["position"]


        if position <= 0:
            return False


        proceeds = position * price


        cost = (
            position
            *
            self.average_entry_price
        )


        profit_loss = proceeds - cost


        self.portfolio["cash"] += proceeds


        # Only update realized when closing
        self.portfolio["realized"] += profit_loss


        self.portfolio["position"] = 0

        self.portfolio["unrealized"] = 0

        self.average_entry_price = 0


        self.update_equity(price)

        return True



    def update_equity(self, price):

        position = self.portfolio["position"]


        position_value = position * price


        self.portfolio["equity"] = (
            self.portfolio["cash"]
            +
            position_value
        )


        if position > 0:

            self.portfolio["unrealized"] = (
                price - self.average_entry_price
            ) * position

        else:

            self.portfolio["unrealized"] = 0



    def get_portfolio(self):

        return self.portfolio
