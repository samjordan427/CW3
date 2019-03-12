from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, static_folder="static")

app.config['SECRET_KEY'] = 'ec4e4c914bf29e11cc501a402d3ba0781031295f209414db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1834256:Chocolate64@csmysql.cs.cf.ac.uk:3306/c1834256'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes
