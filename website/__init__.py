import os
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

# Create flask app 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'chattyroom.db')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

socketio = SocketIO(app)
db = SQLAlchemy(app)

if __name__ == '__main__':
  socketio.run(app, host="127.0.0.1")

from website import routes
