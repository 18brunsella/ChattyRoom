import os
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

# Create flask app 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'chattyroom.db')
socketio = SocketIO(app)
db = SQLAlchemy(app)

# Create user table
class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  user_name = db.Column(db.String(200), unique=True, nullable=False)

# Create messages table 
class Messages(db.Model):
  __tablename__ = 'messages'
  id = db.Column(db.Integer, primary_key=True)
  message_line = db.Column(db.String(250), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Chatty Room Home Page 
@app.route('/')
def home():
  return render_template("home.html")

# Chatty Room Main Chat Room Page 
@app.route('/chatRoom', methods=["GET", "POST"])
def room():
  # If the request is a POST method
  if request.method == "POST":
    username = request.form.get("username")
    # Get all the users with the same name (it is not allowed)
    # user_exists = User.query.filter_by(user_name=username).first()

    # If user_exists is None 
    # if user_exists:
      # Redirects to the home page with error = 1 (name already taken)
      # return redirect(url_for('home', error=1))
    
    # Creating new user row
    #new_user = User(user_name=username)
    User.query.delete() #filter_by(id=1).deleteall()
    users = User.query.all()
    
    for user in users:
      print(user.user_name)
    if not users:
      print("wait its empty")

    # Push to Database with our new user
    #try:
      #db.session.add(new_user)
      #db.session.commit()
    return render_template('chatroom.html', name=username)
    # Any error is printed for now 
    #except SQLAlchemyError as e:
      #print(e)
  else:
    return render_template('chatroom.html')

# Handling messages received by the server (sent from client)
@socketio.on("message")
def handle_message(message):
  print("Received Message: " + str(message))
  if message != "User connected!":
    socketio.emit("response", message)

if __name__ == '__main__':
  socketio.run(app, host="127.0.0.1")

