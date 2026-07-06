class RiskEngine:

    def __init__(self):
        # Kyart Quant risk rules
        self.max_positions = 30

        # Maximum loss allowed on a single trade
        self.max_risk_per_trade = 0.005   # 0.5%

        # Maximum total portfolio risk
        self.max_portfolio_risk = 0.06    # 6%

        # Maximum daily drawdown
        self.max_daily_drawdown = 0.02    # 2%

        # Maximum exposure per asset
        self.max_asset_exposure = 0.20    # 20%

        # Maximum sector exposure
        self.max_sector_exposure = 0.40   # 40%


    def allow_trade(self, market_data, portfolio):

        price = market_data.get("price", 0)

        # Basic market validation
        if price <= 0:
            return False


        equity = portfolio.get("equity", 0)
        position = portfolio.get("position", 0)
        cash = portfolio.get("cash", 0)


        # Account protection
        if equity <= 0:
            return False


        # Position limit protection
        if abs(position) >= self.max_positions:
            return False


        # Calculate current exposure
        current_exposure = abs(position * price) / equity


        # Prevent over concentration
        if current_exposure >= self.max_asset_exposure:
            return False


        # Available capital check
        if cash <= 0:
            return False


        # Maximum allowed risk per trade
        risk_amount = equity * self.max_risk_per_trade


        if risk_amount <= 0:
            return False


        # Daily drawdown protection
        daily_loss = portfolio.get("daily_loss", 0)

        if daily_loss >= equity * self.max_daily_drawdown:
            return False


        return True
