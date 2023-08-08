import csv
import os

from flask import Flask, render_template, flash, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, FloatField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
app.config['SECRET_KEY'] = os.urandom(10)
app.config["DEBUG"] = True
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

POSTS_PER_PAGE = 20


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


class UploadForm(FlaskForm):
    csv_file = FileField('CSV файл', validators=[DataRequired()])
    submit = SubmitField('Загрузить')


class CreateForm(FlaskForm):
    ticker = StringField('ticker', validators=[DataRequired()])
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
    submit = SubmitField('Добавить')


@app.route('/', methods=['GET', 'POST'])
def index_page():
    form = UploadForm()
    if form.validate_on_submit():
        csv_file = form.csv_file.data
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                 csv_file.filename)
        csv_file.save(file_path)
        with open(file_path, 'r') as file:
            data = list(csv.DictReader(file))
            for dic in data:
                for column_name, row_value in dic.items():
                    if row_value == '':
                        dic[column_name] = None
                if not db.session.query(Companies).filter_by(
                        ticker=Companies(**dic).ticker).first():
                    db.session.add(Companies(**dic))
            db.session.commit()
        os.remove(file_path)
        flash("CSV файл успешно загружен!")
    # else:
    #     flash("Неверный тип файла")
    return render_template('index.html', form=form)


# @app.route('/search', methods=['GET', 'POST'])
# def search_page():


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
        return render_template('companies.html', search=search, query=query)
    return render_template('companies.html', query=companies_query)


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
        # if query != None:
        #     values[k] = db.session.query(v).filter(Companies.ticker == ticker_query).one()[0]:.2f}
        # else:
        #     print(f'{k} = {db.session.query(v).filter(Companies.ticker == ticker_query).one()[0]}')
    return values


@app.route('/companies/<ticker>', methods=['GET', 'POST'])
def company_info_page(ticker):
    query = Companies.query.filter_by(ticker=ticker).first()
    if query:
        if request.method == 'POST':
            db.session.delete(query)
            db.session.commit()
            return redirect('/')
        return render_template('company_info.html', query=query,
                               values=get_formuls(ticker))


@app.route('/create', methods=['GET', 'POST'])
def create_comp_page():
    form = CreateForm()
    if form.validate_on_submit():
        db.session.add(Companies(**{k:v for (k,v) in form.data.items() if k != 'submit' and k != 'csrf_token'}))
        db.session.commit()
        flash("Компания успешно добавлена")
    return render_template('create.html', form=form)


if __name__ == '__main__':
    app.run()
