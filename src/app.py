import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from models import db
from utils import seed_data

load_dotenv()
database_uri = os.environ.get('DATABASE_URI')
secret_key = os.environ.get('SECRET_KEY')

app = Flask(__name__)
migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = str(database_uri)
app.config['SECRET_KEY'] = str(secret_key)
db.init_app(app)

with app.app_context():
    db.create_all()
    seed_data(db)
