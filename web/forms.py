from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, SubmitField, StringField, FloatField, \
    SelectField
from wtforms.validators import DataRequired, Length

from web.validators import ticker_check, isalpha_check, isdigit_check


class UploadForm(FlaskForm):
    csv_file = FileField('CSV файл', validators=[
        FileRequired(),
        FileAllowed(['csv'])
    ])
    submit = SubmitField('Загрузить')


class CreateForm(FlaskForm):
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
    ebitda = FloatField(
        'ebitda',
        validators=[isdigit_check],
        render_kw={"placeholder": "0.2134213"}
    )
    sales = FloatField(
        'sales',
        validators=[isdigit_check],
        render_kw={"placeholder": "0.2134213"}
    )
    net_profit = FloatField(
        'net_profit',
        validators=[isdigit_check],
        render_kw={"placeholder": "0.2134213"}
    )
    market_price = FloatField(
        'market_price',
        validators=[isdigit_check],
        render_kw={"placeholder": "0.2134213"}
    )
    net_debt = FloatField(
        'net_debt',
        validators=[isdigit_check],
        render_kw={"placeholder": "0.2134213"}
    )
    assets = FloatField(
        'assets',
        validators=[isdigit_check],
        render_kw={"placeholder": "0.2134213"}
    )
    equity = FloatField(
        'equity',
        validators=[isdigit_check],
        render_kw={"placeholder": "0.2134213"}
    )
    cash_equivalents = FloatField(
        'cash_equivalents',
        validators=[isdigit_check],
        render_kw={"placeholder": "0.2134213"}
    )
    liabilities = FloatField(
        'liabilities',
        validators=[isdigit_check],
        render_kw={"placeholder": "0.2134213"}
    )
    submit = SubmitField('Добавить')


class ChoiceUpdateForm(FlaskForm):
    ticker = SelectField('ticker', choices=[], validators=[DataRequired()])
    submit = SubmitField('Выбрать')


class UpdateForm(FlaskForm):
    ticker = StringField('ticker', validators=[DataRequired()],
                         render_kw={'readonly': True})
    name = StringField('name', validators=[DataRequired()])
    sector = StringField('sector', validators=[DataRequired()])
    ebitda = FloatField('ebitda', validators=[DataRequired()])
    sales = FloatField('sales', validators=[DataRequired()])
    net_profit = FloatField('net_profit', validators=[DataRequired()])
    market_price = FloatField('market_price', validators=[DataRequired()])
    net_debt = FloatField('net_debt', validators=[DataRequired()])
    assets = FloatField('assets', validators=[DataRequired()])
    equity = FloatField('equity', validators=[DataRequired()])
    cash_equivalents = FloatField('cash_equivalents',
                                  validators=[DataRequired()])
    liabilities = FloatField('liabilities', validators=[DataRequired()])
    submit = SubmitField('Обновить данные')