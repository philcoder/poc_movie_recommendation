from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'phil.poc.ia'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:phil.poc.ia@postgres-service:5432/poc_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models