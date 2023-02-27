import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash, get_flashed_messages
from flask_migrate import Migrate
from models import db, Account, Customer, Transaction, User
from utils import seed_data
from forms import CreateCustomerForm
import datetime

load_dotenv()
database_uri = os.environ.get('DATABASE_URI')
secret_key = os.environ.get('SECRET_KEY')

app = Flask(__name__)
migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = str(database_uri)
app.config['SECRET_KEY'] = str(secret_key)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customer/create', methods=['GET', 'POST'])
def create_customer():
    form = CreateCustomerForm()
    if form.validate_on_submit():
        try:
            customer = Customer(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                street_address=form.street_address.data,
                city=form.city.data,
                zipcode=form.zipcode.data,
                country=form.country.data,
                country_code=form.country_code.data,
                birthday=form.birthday.data,
                national_id=form.national_id.data,
                telephone_country_code=form.telephone_country_code.data,
                telephone=form.phone_number.data,
                email_address=form.email_address.data,
            )
            account = Account(account_type='Personal', created=datetime.datetime.now(), balance=0)
            customer.accounts.append(account)
            db.session.add(customer)
            db.session.add(account)
            db.session.commit()
            flash('Customer successfully created.')
            return redirect(url_for('index'))
        except:
            flash(f'Something went wrong.')
    return render_template('create_customer.html', form=form)

@app.route('/customer/<int:customer_id>')
def customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    accounts = Account.query.filter_by(customer_id=customer_id).all()
    return render_template('customer.html', customer=customer, accounts=accounts)

@app.route('/customer/<int:customer_id>/account/<int:account_id>')
def account(customer_id, account_id):
    account = Account.query.get_or_404(account_id)
    transactions = Transaction.query.filter_by(account_id=account_id).all()
    return render_template('account.html', account=account, transactions=transactions)

@app.route('/api/customer_data')
def customer_data():
    query = Customer.query

    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Customer.id.like(f'%{search}%'),
            Customer.first_name.like(f'%{search}%'),
            Customer.last_name.like(f'%{search}%'),
            Customer.email_address.like(f'%{search}%'),
            Customer.street_address.like(f'%{search}%'),
            Customer.country.like(f'%{search}%'),
            Customer.city.like(f'%{search}%'),
            Customer.zipcode.like(f'%{search}%')
        ))
    total_filtered = query.count()

    order = []
    i = 0
    while True:
        column_index = request.args.get(f'order[{i}][column]')
        if column_index is None:
            break

        column_name = request.args.get(f'columns[{column_index}][data]')
        if column_name not in ['id', 'first_name', 'last_name', 'email_address', 'country', 'city']:
            column_name = 'id'

        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        column = getattr(Customer, column_name)
        if descending:
            column = column.desc()
        order.append(column)
        i += 1
    if order:
        query = query.order_by(*order)

    pagination_start = request.args.get('start', type=int)
    pagination_length = request.args.get('length', type=int)
    query = query.offset(pagination_start).limit(pagination_length)

    return {
        'data': [customer.to_dict() for customer in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Customer.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route('/api/<int:customer_id>')
def customer_id_data(customer_id):
    customer = Customer.query.get_or_404(customer_id)

@app.route('/api/account_data')
def account_data():
    query = Account.query

    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Customer.id.like(f'%{search}%'),
            Customer.first_name.like(f'%{search}%'),
            Customer.last_name.like(f'%{search}%'),
            Customer.email_address.like(f'%{search}%'),
            Customer.country.like(f'%{search}%'),
            Customer.city.like(f'%{search}%')
        ))
    total_filtered = query.count()

    order = []
    i = 0
    while True:
        column_index = request.args.get(f'order[{i}][column]')
        if column_index is None:
            break

        column_name = request.args.get(f'columns[{column_index}][data]')
        if column_name not in ['id', 'first_name', 'last_name', 'email_address', 'country', 'city']:
            column_name = 'id'

        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        column = getattr(Customer, column_name)
        if descending:
            column = column.desc()
        order.append(column)
        i += 1
    if order:
        query = query.order_by(*order)

    pagination_start = request.args.get('start', type=int)
    pagination_length = request.args.get('length', type=int)
    query = query.offset(pagination_start).limit(pagination_length)

    return {
        'data': [customer.to_dict() for customer in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Customer.query.count(),
        'draw': request.args.get('draw', type=int),
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data(db)
        app.run(debug=True)
