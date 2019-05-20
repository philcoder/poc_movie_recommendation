from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'phil.poc.ia'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:phil.poc.ia@postgres-service:5432/poc_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
#sent to index all protect urls
login.login_view = 'index'

from app import routes, models