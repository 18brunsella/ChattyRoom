from website import app, db, socketio
from flask import render_template, request, flash, redirect, url_for, session
from website.models import User, Messages
from flask_socketio import SocketIO
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Chatty Room Home Page 
@app.route('/')
def home():
  return render_template("home.html")

# Chatty Room Exiting page 
@app.route('/exitRoom/<int:user_id>')
def exitRoom(user_id):
  user_to_delete = User.query.get_or_404(user_id)
  try: 
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
  except:
    flash("Whoops there was a problem deleting the user, try again.")

# Chatty Room Main Chat Room Page 
@app.route('/chatRoom', methods=["GET", "POST"])
def room():
  # If the request is a POST method
  if request.method == "POST":
    username = request.form.get("username")
    # Deleting a user 
    #db.session.query(User).delete()
    # db.session.commit()

    # Get all the users with the same name (it is not allowed)
    user_exists = User.query.filter_by(user_name=username).first()

    # If user_exists is None 
    if user_exists:
      # Redirects to the home page with error = 1 (name already taken)
      return render_template('home.html', error=1)
    
    # Creating new user row
    new_user = User(user_name=username)

    # Push to Database with our new user
    try:
      db.session.add(new_user)
      db.session.commit()

      session.permanent = True
      session.modified = True
      return render_template('chatroom.html', name=username, id=new_user.id)
    # Any error is printed for now 
    except SQLAlchemyError as e:
      print(e)
  else:
    return render_template('chatroom.html')

# Handling messages received by the server (sent from client)
@socketio.on("message")
def handle_message(message):
  print("Received Message: " + str(message))
  # If message is not user connected then emit the message out to the clients 
  if message['message'] != "User connected!":
    print(message['message'])

    # Add a message to the database with the userid and message
    new_message = Messages(message_line=message['message'], user_id=message['id'])

    # Try and except to add and commit new message into table 
    try:
      db.session.add(new_message)
      db.session.commit()
    except SQLAlchemyError as e:
      print(e)

    socketio.emit("response", message)

