import os
from dotenv import load_dotenv

load_dotenv()

username = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
host = os.environ['MYSQL_HOST']
database_name = os.environ['MYSQL_NAME']

class ConfigDebug():
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{host}/{database_name}'
    SECRET_KEY = str(password)
