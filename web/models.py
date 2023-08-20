from web import db


class Companies(db.Model):
    ticker = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    sector = db.Column(db.String(80), nullable=False)
    ebitda = db.Column(db.Float, nullable=True)
    sales = db.Column(db.Float, nullable=True)
    net_profit = db.Column(db.Float, nullable=True)
    market_price = db.Column(db.Float, nullable=True)
    net_debt = db.Column(db.Float, nullable=True)
    assets = db.Column(db.Float, nullable=True)
    equity = db.Column(db.Float, nullable=True)
    cash_equivalents = db.Column(db.Float, nullable=True)
    liabilities = db.Column(db.Float, nullable=True)
