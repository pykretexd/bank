import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash, get_flashed_messages
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Account, Customer, Transaction, User
from utils import check_valid_withdraw, seed_data
from forms import CreateCustomerForm, WithdrawForm, DepositForm, TransferForm, LoginUserForm, SignupUserForm, UpdateUserForm
import datetime

load_dotenv()
database_uri = os.environ.get('DATABASE_URI')
secret_key = os.environ.get('SECRET_KEY')

app = Flask(__name__)
migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = str(database_uri)
app.config['SECRET_KEY'] = str(secret_key)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    balance = 0
    for account in accounts:
        balance += account.balance

    return render_template('customer.html', customer=customer, accounts=accounts, balance=balance)

@app.route('/customer/<int:customer_id>/withdraw', methods=['GET', 'POST'])
def withdraw(customer_id):
    form = WithdrawForm()
    form.account.choices = [(account.id, account.balance) for account in Account.query.filter_by(customer_id=customer_id).all()]
    
    if form.validate_on_submit():
        account = Account.query.get_or_404(form.account.data)
        try:
            check_valid_withdraw(account.balance, form.amount.data)
        except Exception as e:
            flash(str(e))
        new_balance = account.balance - form.amount.data
        transaction = Transaction(type='Credit', operation='Bank withdrawal', date=datetime.datetime.now(), amount=form.amount.data, new_balance=new_balance)
        account.transactions.append(transaction)
        account.balance = transaction.new_balance
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction successfully executed.')
        return redirect(url_for('customer', customer_id=customer_id))

    return render_template('withdraw.html', form=form)

@app.route('/customer/<int:customer_id>/deposit', methods=['GET', 'POST'])
def deposit(customer_id):
    form = DepositForm()
    form.account.choices = [(account.id, account.balance) for account in Account.query.filter_by(customer_id=customer_id).all()]

    if form.validate_on_submit():
        account = Account.query.get_or_404(form.account.data)
        new_balance = account.balance + form.amount.data
        if form.amount.data <= 0:
            flash('Invalid amount.')
        else:
            transaction = Transaction(type='Debit', operation='Deposit cash', date=datetime.datetime.now(), amount=form.amount.data, new_balance=new_balance)
            account.transactions.append(transaction)
            account.balance = transaction.new_balance
            db.session.add(transaction)
            db.session.commit()
            flash('Transaction successfully executed.')
            return redirect(url_for('customer', customer_id=customer_id))

    return render_template('deposit.html', form=form)

@app.route('/customer/<int:customer_id>/transfer', methods=['GET', 'POST'])
def transfer(customer_id):
    form = TransferForm()
    form.account.choices = [(account.id, account.balance) for account in Account.query.filter_by(customer_id=customer_id).all()]

    if form.validate_on_submit():
        account = Account.query.get_or_404(form.account.data)
        try:
            target = Account.query.get_or_404(form.target.data)
        except:
            flash('Something unexpected happened. Please try again.')
            return render_template('transfer.html')
        try:
            check_valid_withdraw(account.balance, form.amount.data)
        except Exception as e:
            flash(str(e))
            return render_template('transfer.html', form=form)

        account_new_balance = account.balance - form.amount.data
        account_transaction = Transaction(type='Credit', operation='Transfer', date=datetime.datetime.now(), amount=form.amount.data, new_balance=account_new_balance)
        account.transactions.append(account_transaction)
        account.balance = account_transaction.new_balance

        target_new_balance = target.balance + form.amount.data
        target_transaction = Transaction(type='Debit', operation='Transfer', date=datetime.datetime.now(), amount=form.amount.data, new_balance=target_new_balance)
        target.transactions.append(target_transaction)
        target.balance = target_new_balance

        db.session.add(account_transaction)
        db.session.add(target_transaction)
        db.session.commit()
        flash('Transfer was successful.')
        return redirect(url_for('customer', customer_id=customer_id))

    return render_template('transfer.html', form=form)

@app.route('/customer/<int:customer_id>/account/<int:account_id>', methods=['GET'])
def account(customer_id, account_id):
    account = Account.query.get_or_404(account_id)
    return render_template('account.html', account=account)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user is None:
            password_hash = generate_password_hash(form.password.data, 'sha256')
            new_user = User(email_address=form.email_address.data, hashed_password=password_hash)
            cashier_role = Role.query.filter_by(name='Cashier').first()
            cashier_role.users.append(new_user)

            db.session.add(new_user)
            db.session.commit()

            flash('Sign up successful!')
            return redirect(url_for('login'))
        else:
            flash('Email address has already been signed up.')
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user:
            if check_password_hash(user.hashed_password, form.password.data):
                login_user(user)
                flash('Log in successful!')
                return redirect(url_for('index'))
            else:
                flash('Credentials did not match, please try again.')
        else:
            flash('User does not exist.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('index'))

@app.route('/update_customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def update_customer(customer_id):
    form = UpdateUserForm()
    customer_to_update = Customer.query.get_or_404(customer_id)

    if form.validate_on_submit():
        customer_to_update.first_name = form.first_name.data
        customer_to_update.last_name = form.last_name.data
        customer_to_update.street_address = form.street_address.data
        customer_to_update.city = form.city.data
        customer_to_update.zipcode = form.zipcode.data
        customer_to_update.country = form.country.data
        customer_to_update.country_code = form.country_code.data
        customer_to_update.birthday = form.birthday.data
        customer_to_update.national_id = form.national_id.data
        customer_to_update.telephone_country_code = form.telephone_country_code.data
        customer_to_update.telephone = form.phone_number.data
        customer_to_update.email_address = form.email_address.data

        try:
            db.session.commit()
            flash('Customer successfully updated.')
            return render_template('update_customer.html', form=form, customer_to_update=customer_to_update)
        except:
            flash('Something unexpected happened, please try again.')
            return render_template('update_customer.html', form=form, customer_to_update=customer_to_update)
    
    return render_template('update_customer.html', form=form, customer_to_update=customer_to_update)

@app.route('/delete_customer/<int:customer_id>')
@login_required
def delete_customer(customer_id):
    if current_user.is_authenticated:
        try:
            customer_to_delete = Customer.query.get_or_404(customer_id)
            accounts = Account.query.filter_by(customer_id=customer_to_delete.id).all()
            for account in accounts:
                transactions = Transaction.query.filter_by(account_id=account.id).all()
                for transaction in transactions:
                    db.session.delete(transaction)
                db.session.delete(account)
            db.session.delete(customer_to_delete)
            db.session.commit()
            flash(f'Customer #{customer_id} has successfully been deleted.')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Something unexpected happened, please try again. {str(e)}')
            return redirect(url_for('customer', customer_id=customer_id))
    else:
        flash('You cannot perform this action.')
        return redirect(url_for('index'))

@app.route('/api/customers')
def customers():
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

@app.route('/api/accounts/<int:account_id>')
def account_data(account_id):
    query = Transaction.query.filter_by(account_id=account_id)
    
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Transaction.id.like(f'%{search}%'),
        ))
    total_filtered = query.count()

    order = []
    i = 0
    while True:
        column_index = request.args.get(f'order[{i}][column]')
        if column_index is None:
            break

        column_name = request.args.get(f'columns[{column_index}][data]')
        if column_name not in ['id']:
            column_name = 'id'

        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        column = getattr(Transaction, column_name)
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
        'data': [transaction.to_dict() for transaction in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Transaction.query.filter_by(account_id=account_id).count(),
        'draw': request.args.get('draw', type=int),
    }


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data(db)
        app.run(debug=True)
