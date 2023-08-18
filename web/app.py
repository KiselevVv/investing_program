import csv
import os

import sqlalchemy
from flask import Flask, render_template, flash, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from wtforms import FileField, SubmitField, StringField, FloatField, \
    SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
app.config['SECRET_KEY'] = os.urandom(10)
app.config["DEBUG"] = True
UPLOAD_FOLDER = 'web/static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)


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


with app.app_context():
    db.create_all()
    db.session.commit()

POSTS_PER_PAGE = 20

formuls_temlate = {'P/E': 'market_price / net_profit',
                   'P/S': 'market_price / sales',
                   'P/B': 'market_price / assets',
                   'ND/EBITDA': 'net_debt / ebitda',
                   'ROE': 'net_profit / equity',
                   'ROA': 'net_profit / assets',
                   'L/A': 'liabilities / assets'}


class UploadForm(FlaskForm):
    csv_file = FileField('CSV файл', validators=[DataRequired()])
    submit = SubmitField('Загрузить')


class CreateForm(FlaskForm):
    ticker = StringField(
        'ticker',
        validators=[DataRequired()],
        render_kw={"placeholder": "AAA"}
    )
    name = StringField(
        'name',
        validators=[DataRequired()],
        render_kw={"placeholder": "Aple"}
    )
    sector = StringField(
        'sector',
        validators=[DataRequired()],
        render_kw={"placeholder": "Electronic Technology"}
    )
    ebitda = FloatField(
        'ebitda',
        validators=[DataRequired()],
        render_kw={"placeholder": "0.2134213"}
    )
    sales = FloatField(
        'sales',
        validators=[DataRequired()],
        render_kw={"placeholder": "0.2134213"}
    )
    net_profit = FloatField(
        'net_profit',
        validators=[DataRequired()],
        render_kw={"placeholder": "0.2134213"}
    )
    market_price = FloatField(
        'market_price',
        validators=[DataRequired()],
        render_kw={"placeholder": "0.2134213"}
    )
    net_debt = FloatField(
        'net_debt',
        validators=[DataRequired()],
        render_kw={"placeholder": "0.2134213"}
    )
    assets = FloatField(
        'assets',
        validators=[DataRequired()],
        render_kw={"placeholder": "0.2134213"}
    )
    equity = FloatField(
        'equity',
        validators=[DataRequired()],
        render_kw={"placeholder": "0.2134213"}
    )
    cash_equivalents = FloatField(
        'cash_equivalents',
        validators=[DataRequired()],
        render_kw={"placeholder": "0.2134213"}
    )
    liabilities = FloatField(
        'liabilities',
        validators=[DataRequired()],
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


def load_to_db(file_path):
    with open(file_path, 'r') as file:
        data = list(csv.DictReader(file))
        for dic in data:
            for column_name, row_value in dic.items():
                if row_value == '':
                    dic[column_name] = None
            try:
                query = db.session.query(Companies).filter_by(
                    ticker=Companies(**dic).ticker
                )
                if not query.first():
                    db.session.add(Companies(**dic))
                else:
                    query.update(dic)
            except (TypeError, sqlalchemy.exc.IntegrityError):
                db.session.rollback()
                return False
        db.session.commit()
        return True


@app.route('/', methods=['GET', 'POST'])
def index_page():
    form = UploadForm()
    if form.validate_on_submit():
        filename = form.csv_file.data.filename
        if filename.split('.')[-1] == 'csv':
            csv_file = form.csv_file.data
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                     csv_file.filename)
            csv_file.save(file_path)
            if load_to_db(file_path):
                flash("CSV файл успешно загружен!")
            else:
                flash("CSV файл имеет неверную структуру!")
            os.remove(file_path)
        else:
            flash("Неверный тип файла")
    return render_template('investing/index.html', form=form, current_page='/')


@app.route('/companies', methods=['GET', 'POST'])
@app.route('/companies/<int:page>', methods=['GET', 'POST'])
def companies_page(page=1):
    companies_query = db.session.query(Companies).paginate(page=page,
                                                           per_page=POSTS_PER_PAGE,
                                                           error_out=False)
    if request.method == 'POST':
        search = request.form.get("comp_name")
        query = db.session.query(Companies).filter(
            Companies.name.like(f'%{search}%')).paginate(page=page,
                                                         per_page=POSTS_PER_PAGE,
                                                         error_out=False)
        return render_template('investing/companies.html', search=search,
                               query=query, current_page='/companies')
    return render_template('investing/companies.html', query=companies_query,
                           current_page='/companies')


def get_formuls(ticker):
    formuls = {'P/E': Companies.market_price / Companies.net_profit,
               'P/S': Companies.market_price / Companies.sales,
               'P/B': Companies.market_price / Companies.assets,
               'ND/EBITDA': Companies.net_debt / Companies.ebitda,
               'ROE': Companies.net_profit / Companies.equity,
               'ROA': Companies.net_profit / Companies.assets,
               'L/A': Companies.liabilities / Companies.assets}
    values = {}
    for k, v in formuls.items():
        query = db.session.query(v).filter(Companies.ticker == ticker).one()[0]
        values[k] = query
    return values


@app.route('/companies/<ticker>', methods=['GET', 'POST'])
def company_info_page(ticker):
    query = Companies.query.filter_by(ticker=ticker).first()
    if query:
        if request.method == 'POST':
            db.session.delete(query)
            db.session.commit()
            return redirect('/')
        return render_template('investing/company_info.html', query=query,
                               values=get_formuls(ticker),
                               formuls_temlate=formuls_temlate,
                               current_page='/companies')


@app.route('/create', methods=['GET', 'POST'])
def create_comp_page():
    form = CreateForm()
    if form.validate_on_submit():
        db.session.add(Companies(**{k: v for (k, v) in form.data.items() if
                                    k != 'submit' and k != 'csrf_token'}))
        db.session.commit()
        flash("Компания успешно добавлена")
    return render_template('investing/create.html', form=form,
                           current_page='/create')


@app.route('/update', methods=['GET', 'POST'])
def update_page():
    form = ChoiceUpdateForm()
    companies = Companies.query.all()
    tickers = ['']
    tickers += [company.ticker for company in companies]
    form.ticker.choices = tickers
    if form.validate_on_submit():
        selected_ticker = form.ticker.data
        return redirect(url_for('update_comp_page', ticker=selected_ticker))
        # db.session.add(Companies(**{k: v for (k, v) in form.data.items() if
        #                             k != 'submit' and k != 'csrf_token'}))
        # db.session.commit()
        # flash("Компания успешно добавлена")
    return render_template('investing/update.html', form=form,
                           current_page='/update')


@app.route('/update/<ticker>', methods=['GET', 'POST'])
def update_comp_page(ticker):
    form = UpdateForm()
    query = Companies.query.filter_by(ticker=ticker).first()
    if form.validate_on_submit():
        Companies.query.filter_by(ticker=ticker).update(
            {k: v for (k, v) in form.data.items() if
             k != 'submit' and k != 'csrf_token'})
        db.session.commit()
        flash("Компания успешно обновлена")
    return render_template('investing/update.html', form=form, ticker=ticker,
                           query=query, current_page='/update')


@app.route('/top', methods=['GET'])
def top_comp_page():
    query_nd_ebitda = db.session.query(Companies).order_by(
        desc(Companies.net_debt / Companies.ebitda)).limit(10).all()
    query_roe = db.session.query(Companies).order_by(
        desc(Companies.net_profit / Companies.equity)).limit(10).all()
    query_roa = db.session.query(Companies).order_by(
        desc(Companies.net_profit / Companies.assets)).limit(10).all()
    return render_template('investing/top.html',
                           query_nd_ebitda=query_nd_ebitda,
                           query_roe=query_roe, query_roa=query_roa,
                           current_page='/top')


if __name__ == '__main__':
    app.run()
