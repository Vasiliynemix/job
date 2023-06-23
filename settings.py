import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

DB_HOST_TEST = os.environ.get('DB_HOST_TEST')
DB_PORT_TEST = os.environ.get('DB_PORT_TEST')
DB_NAME_TEST = os.environ.get('DB_NAME_TEST')
DB_USER_TEST = os.environ.get('DB_USER_TEST')
DB_PASS_TEST = os.environ.get('DB_PASS_TEST')

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_AUTH_KEY = os.environ.get('SECRET_AUTH_KEY')
SECRET_AUTH_MANAGER_KEY = os.environ.get('SECRET_AUTH_MANAGER_KEY')

DEV_HOST = os.environ.get('DEV_HOST')
DEV_PORT = os.environ.get('DEV_PORT')
