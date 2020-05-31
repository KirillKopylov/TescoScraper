import os
from sqlalchemy import create_engine
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))
database_url = os.environ.get('DB_CONNECTION') + '://' + os.environ.get('DB_USERNAME') + ':' + os.environ.get(
    'DB_PASSWORD') + '@' + os.environ.get('DB_HOST') + ':' + os.environ.get('DB_PORT') + '/' + os.environ.get(
    'DB_DATABASE')
engine = create_engine(database_url)
