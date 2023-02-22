from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__= 'Customers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    street_address = db.Column(db.String(50), unique=False, nullable=False)
    city = db.Column(db.String(50), unique=False, nullable=False)
    zipcode = db.Column(db.String(10), unique=False, nullable=False)
    country = db.Column(db.String(30), unique=False, nullable=False)
    country_code = db.Column(db.String(2), unique=False, nullable=False)
    birthday = db.Column(db.Date, unique=False, nullable=False)
    national_id = db.Column(db.String(20), unique=False, nullable=False)
    telephone_country_code = db.Column(db.Integer, unique=False, nullable=False)
    telephone = db.Column(db.String(20), unique=False, nullable=False)
    email_address = db.Column(db.String(50), unique=False, nullable=False)
    accounts = db.relationship('Account', backref='Customer',lazy=True)

class Account(db.Model):
    __tablename__= 'Accounts'
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(10), unique=False, nullable=False)
    created = db.Column(db.DateTime, unique=False, nullable=False)
    balance = db.Column(db.Integer, unique=False, nullable=False)
    transactions = db.relationship('Transaction', backref='Account',
     lazy=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'), nullable=False)

class Transaction(db.Model):
    __tablename__= 'Transactions'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), unique=False, nullable=False)
    operation = db.Column(db.String(50), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    amount = db.Column(db.Integer, unique=False, nullable=False)
    new_balance = db.Column(db.Integer, unique=False, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('Accounts.id'), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(50), unique=False, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)
