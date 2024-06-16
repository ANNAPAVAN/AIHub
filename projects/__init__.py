from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_login import LoginManager # type: ignore
from dotenv import load_dotenv
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)

login_manager = LoginManager(app)

login_manager.login_view = "login"
login_manager.login_message_category = "info"


from projects import routes