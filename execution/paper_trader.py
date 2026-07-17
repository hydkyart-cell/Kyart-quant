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

        self.max_exposure = 0.20

        self.stop_loss_percent = 0.005
        self.take_profit_percent = 0.01



    def buy(self, price):

        equity = self.portfolio["equity"]

        max_position_value = equity * self.max_exposure

        current_position_value = (
            self.portfolio["position"] * price
        )


        if current_position_value >= max_position_value:
            return False


        available_room = (
            max_position_value - current_position_value
        )


        quantity = available_room / price


        if quantity <= 0:
            return False


        cost = quantity * price


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
        self.portfolio["cash"] -= cost


        self.update_equity(price)

        return True



    def check_risk_exit(self, price):

        if self.portfolio["position"] <= 0:
            return False


        change = (
            price - self.average_entry_price
        ) / self.average_entry_price


        if change <= -self.stop_loss_percent:
            return self.sell(price)


        if change >= self.take_profit_percent:
            return self.sell(price)


        return False



    def sell(self, price):

        position = self.portfolio["position"]


        if position <= 0:
            return False


        proceeds = position * price


        cost = (
            position *
            self.average_entry_price
        )


        profit_loss = proceeds - cost


        self.portfolio["cash"] += proceeds

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
