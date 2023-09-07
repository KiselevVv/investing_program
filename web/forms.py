from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import (FileField, SubmitField, StringField, FloatField,
                     SelectField)
from wtforms.validators import (DataRequired, Length, Optional)

from web.validators import ticker_check, isalpha_check


class MyFloatField(FloatField):
    """
    Класс для кастомного поля формы, преобразующего ввод в float.
    """
    def process_formdata(self, valuelist):
        """
        Преобразует ввод пользователя в float.
        :param valuelist: Список значений поля.
        :return: ValueError: Если ввод не может быть преобразован в float.
        """
        if valuelist:
            try:
                self.data = float(valuelist[0])
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Неверный формат'))


class UploadForm(FlaskForm):
    """
    Форма загрузки CSV файла.
    attr:
        csv_file (FileField): Поле для выбора файла.
        submit (SubmitField): Кнопка отправки формы.
    """
    csv_file = FileField('CSV файл', validators=[
        FileRequired(),
        FileAllowed(['csv'])
    ])
    submit = SubmitField('Загрузить')


class CreateForm(FlaskForm):
    """
    Форма создания компании.

    attr:
        ticker (StringField): Поле для ввода тикера.
        name (StringField): Поле для ввода имени компании.
        sector (StringField): Поле для ввода сектора компании.
        ebitda (MyFloatField): Поле для ввода EBITDA.
        sales (MyFloatField): Поле для ввода продаж.
        net_profit (MyFloatField): Поле для ввода чистой прибыли.
        market_price (MyFloatField): Поле для ввода рыночной цены.
        net_debt (MyFloatField): Поле для ввода чистого долга.
        assets (MyFloatField): Поле для ввода активов.
        equity (MyFloatField): Поле для ввода собственного капитала.
        cash_equivalents (MyFloatField): Поле для ввода денежных эквивалентов.
        liabilities (MyFloatField): Поле для ввода обязательств.
        submit (SubmitField): Кнопка отправки формы.
    """
    ticker = StringField(
        'ticker',
        validators=[DataRequired(),
                    Length(min=-1, max=30, message='Максимальная длина 30'),
                    ticker_check],
        render_kw={"placeholder": "AAA"}
    )
    name = StringField(
        'name',
        validators=[DataRequired(),
                    Length(min=-1, max=80, message='Максимальная длина 80'),
                    isalpha_check],
        render_kw={"placeholder": "Aple"}
    )
    sector = StringField(
        'sector',
        validators=[DataRequired(),
                    Length(min=-1, max=80, message='Максимальная длина 80'),
                    isalpha_check],
        render_kw={"placeholder": "Electronic Technology"}
    )
    ebitda = MyFloatField(
        'ebitda',
        validators=[Optional()],
        render_kw={"placeholder": "335342"}
    )
    sales = MyFloatField(
        'sales',
        validators=[Optional()],
        render_kw={"placeholder": "0.2134213"}
    )
    net_profit = MyFloatField(
        'net_profit',
        validators=[Optional()],
        render_kw={"placeholder": "335342"}
    )
    market_price = MyFloatField(
        'market_price',
        validators=[Optional()],
        render_kw={"placeholder": "0.2134213"}
    )
    net_debt = MyFloatField(
        'net_debt',
        validators=[Optional()],
        render_kw={"placeholder": "335342"}
    )
    assets = MyFloatField(
        'assets',
        validators=[Optional()],
        render_kw={"placeholder": "0.2134213"}
    )
    equity = MyFloatField(
        'equity',
        validators=[Optional()],
        render_kw={"placeholder": "335342"}
    )
    cash_equivalents = MyFloatField(
        'cash_equivalents',
        validators=[Optional()],
        render_kw={"placeholder": "0.2134213"}
    )
    liabilities = MyFloatField(
        'liabilities',
        validators=[Optional()],
        render_kw={"placeholder": "335342"}
    )
    submit = SubmitField('Добавить')


class ChoiceUpdateForm(FlaskForm):
    """
    Форма выбора компании для обновления.

    attr:
        ticker (SelectField): Поле для выбора тикера компании.
        submit (SubmitField): Кнопка отправки формы.
    """
    ticker = SelectField('ticker', choices=[], validators=[DataRequired()])
    submit = SubmitField('Выбрать')


class UpdateForm(FlaskForm):
    """
    Форма обновления информации о компании.

    attr:
        ticker (StringField): Поле для ввода тикера (только для чтения).
        name (StringField): Поле для ввода имени компании.
        sector (StringField): Поле для ввода сектора компании.
        ebitda (MyFloatField): Поле для ввода EBITDA.
        sales (MyFloatField): Поле для ввода продаж.
        net_profit (MyFloatField): Поле для ввода чистой прибыли.
        market_price (MyFloatField): Поле для ввода рыночной цены.
        net_debt (MyFloatField): Поле для ввода чистого долга.
        assets (MyFloatField): Поле для ввода активов.
        equity (MyFloatField): Поле для ввода собственного капитала.
        cash_equivalents (MyFloatField): Поле для ввода денежных эквивалентов.
        liabilities (MyFloatField): Поле для ввода обязательств.
        submit (SubmitField): Кнопка отправки формы.
    """
    ticker = StringField(
        'ticker',
        validators=[DataRequired()],
        render_kw={'readonly': True}
    )
    name = StringField(
        'name',
        validators=[DataRequired(),
                    Length(min=-1, max=80, message='Максимальная длина 80'),
                    isalpha_check],
    )
    sector = StringField(
        'sector',
        validators=[DataRequired(),
                    Length(min=-1, max=80, message='Максимальная длина 80'),
                    isalpha_check],
    )
    ebitda = MyFloatField('ebitda', validators=[Optional()])
    sales = MyFloatField('sales', validators=[Optional()])
    net_profit = MyFloatField('net_profit', validators=[Optional()])
    market_price = MyFloatField('market_price', validators=[Optional()])
    net_debt = MyFloatField('net_debt', validators=[Optional()])
    assets = MyFloatField('assets', validators=[Optional()])
    equity = MyFloatField('equity', validators=[Optional()])
    cash_equivalents = MyFloatField('cash_equivalents',
                                    validators=[Optional()])
    liabilities = MyFloatField('liabilities', validators=[Optional()])
    submit = SubmitField('Обновить данные')
