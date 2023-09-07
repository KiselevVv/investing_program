from web import db


class Companies(db.Model):
    """
    Модель для представления данных о компаниях.

    attr:
        ticker (db.String): Уникальный символьный идентификатор компании.
        name (db.String): Имя компании (уникальное).
        sector (db.String): Сектор, к которому принадлежит компания.
        ebitda (db.Float): EBITDA компании.
        sales (db.Float): Объем продаж компании.
        net_profit (db.Float): Чистая прибыль компании.
        market_price (db.Float): Рыночная цена акций компании.
        net_debt (db.Float): Чистый долг компании.
        assets (db.Float): Активы компании.
        equity (db.Float): Собственный капитал компании.
        cash_equivalents (db.Float): Денежные эквиваленты компании.
        liabilities (db.Float): Обязательства компании.
    """
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
