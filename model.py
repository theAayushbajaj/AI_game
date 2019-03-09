from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit
from flask_migrate import Migrate
import os
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ROOT_DIR+'/database.db'
app.config['SECRET_KEY'] = 'ascvasjhcvdsv'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    score_type = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer)
    record_date = db.Column(db.Date, default=datetime.now().date())

    def __repr__(self):
        return 'User Email : ' + str(self.email)


class Individuals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return 'User Email : ' + str(self.email)


class Schools(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_email = db.Column(db.String(100), nullable=False)
    individual_email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'School Email : ' + str(self.school_email)

class Parents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_email = db.Column(db.String(100), nullable=False)
    child_email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'Parent Email : ' + str(self.parent_email)