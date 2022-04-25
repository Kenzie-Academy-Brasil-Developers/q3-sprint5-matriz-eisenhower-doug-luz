from flask import Flask
import os
from dotenv import load_dotenv
from app.configs import database, migrate
from app import routes 
load_dotenv()


def create_app():
    
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = bool(os.getenv('TRACK_MODIFICATIONS'))
    app.config['JSON_SORT_KEYS'] = bool(os.getenv('SORT_KEYS'))

    database.init_app(app)
    migrate.init_app(app)
    routes.init_app(app)
    return app