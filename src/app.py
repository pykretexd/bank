import os
from dotenv import load_dotenv
from flask import Flask, render_template, url_for
from flask_migrate import Migrate
from models import db, Account, Customer, Transaction, User
from utils import seed_data

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
    customers = Customer.query.all()
    return render_template('index.html', customers=customers)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data(db)
        app.run(debug=True)
