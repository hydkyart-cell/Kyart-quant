class RiskManager:

    def __init__(
        self,
        max_risk_per_trade=0.005,
        max_portfolio_risk=0.06,
        max_position_size=0.20,
        daily_drawdown_limit=0.02
    ):

        self.max_risk_per_trade = max_risk_per_trade
        self.max_portfolio_risk = max_portfolio_risk
        self.max_position_size = max_position_size
        self.daily_drawdown_limit = daily_drawdown_limit


    def calculate_position_size(
        self,
        cash,
        price
    ):

        allowed_capital = cash * self.max_position_size

        quantity = allowed_capital / price

        return quantity


    def check_trade(
        self,
        portfolio,
        action
    ):

        if action == "BUY":

            if portfolio["cash"] <= 0:
                return False

            return True


        if action == "SELL":

            if portfolio["position"] <= 0:
                return False

            return True


        return False
