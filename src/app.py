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

@app.route('/', methods=['GET'], defaults={'page': 1})
@app.route('/<int:page>', methods=['GET'])
def index(page):
    page = page
    customer_count = Customer.query.count()
    customers = Customer.query.paginate(page=page, per_page=50)
    return render_template('index.html', customer_count=customer_count, customers=customers)

@app.route('/profile/<int:id>', methods=['GET'])
def profile(id):
    customer = Customer.query.get_or_404(id)
    return render_template('profile.html', customer=customer)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data(db)
        app.run()
