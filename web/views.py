import csv
import os

import sqlalchemy
from flask import render_template, flash, url_for, request, redirect

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from web import app
from .forms import UploadForm, CreateForm, ChoiceUpdateForm, UpdateForm
from .models import Companies, db

POSTS_PER_PAGE = 20
FORMULS_TEMPLATE = {'P/E': 'market_price / net_profit',
                    'P/S': 'market_price / sales',
                    'P/B': 'market_price / assets',
                    'ND/EBITDA': 'net_debt / ebitda',
                    'ROE': 'net_profit / equity',
                    'ROA': 'net_profit / assets',
                    'L/A': 'liabilities / assets'}


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
    if request.method == 'POST':
        if form.validate_on_submit():
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
                               formuls_temlate=FORMULS_TEMPLATE,
                               current_page='/companies')


@app.route('/create', methods=['GET', 'POST'])
def create_comp_page():
    form = CreateForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            ticker_query = db.session.query(Companies).filter_by(
                ticker=form.data['ticker']).first()
            name_query = db.session.query(Companies).filter_by(
                name=form.data['name']).first()
            if not ticker_query and not name_query:
                db.session.add(
                    Companies(**{k: v for (k, v) in form.data.items() if
                                 k != 'submit' and k != 'csrf_token'}))
                db.session.commit()
                flash("Компания успешно добавлена")
            else:
                flash("Такая компания уже существует!")
    return render_template('investing/create.html', form=form,
                           current_page='/create')


@app.route('/update', methods=['GET', 'POST'])
def update_page():
    form = ChoiceUpdateForm()
    companies = Companies.query.all()
    tickers = ['']
    tickers += [company.ticker for company in companies]
    form.ticker.choices = tickers
    if request.method == 'POST':
        if form.validate_on_submit():
            selected_ticker = form.ticker.data
            return redirect(
                url_for('update_comp_page', ticker=selected_ticker))
    return render_template('investing/update.html', form=form,
                           current_page='/update')


@app.route('/update/<ticker>', methods=['GET', 'POST'])
def update_comp_page(ticker):
    form = UpdateForm()
    query = Companies.query.filter_by(ticker=ticker).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            name_query = db.session.query(Companies).filter_by(
                name=form.data['name']).first()
            if name_query.ticker == query.ticker:
                Companies.query.filter_by(ticker=ticker).update(
                    {k: v for (k, v) in form.data.items() if
                     k != 'submit' and k != 'csrf_token'})
                db.session.commit()
                flash("Компания успешно обновлена")
            else:
                flash("Компания c таким именем уже существует!")
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
