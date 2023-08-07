import csv
import os

from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
app.config['SECRET_KEY'] = os.urandom(10)
app.config["DEBUG"] = True
UPLOAD_FOLDER = 'static/files'
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


class UploadForm(FlaskForm):
    csv_file = FileField('CSV File', validators=[DataRequired()])
    submit = SubmitField('Upload')


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


@app.route('/companies', methods=['GET'])
def companies_page():
    companies_query = db.session.query(Companies).all()
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


@app.route('/companies/<ticker>', methods=['GET'])
def company_info_page(ticker):
    query = Companies.query.filter_by(ticker=ticker).first()
    if query:
        return render_template('company_info.html', query=query, values=get_formuls(ticker))


if __name__ == '__main__':
    app.run()
