from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'phil.poc.ia'

from app import routes