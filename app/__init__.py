from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'cake-by-the-ocean'
login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
