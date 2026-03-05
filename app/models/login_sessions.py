from app.db import db
from datetime import datetime,timezone

def uct_now():
    return datetime.now(timezone.utc)

class Login_Sessions():
  __tablename__="login_sessions"

  id = db.Column(db.Integer,primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  session_token = db.Column(db.String(255), unique=True, nullable=False)
  login_time = db.Column(db.DateTime, default=datetime.utcnow)
  logout_time = db.Column(db.DateTime, nullable=True)
  ip_address = db.Column(db.String(45), nullable=True)
  user_agent = db.Column(db.Text, nullable=True)
  is_active = db.Column(db.Boolean, default=True)