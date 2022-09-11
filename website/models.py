from website import db
from datetime import datetime

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
