from app.db import db
from datetime import datetime,timezone

def uct_now():
    return datetime.now(timezone.utc)

class User(db.Model):
  __tablename__="user"

  id = db.Column(db.Integer,primary_key=True, autoincrement=True)
  full_name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(500),nullable=False,unique=True)
  password = db.Column(db.Text,nullable=False)
  terms_accepted = db.Column(db.Boolean, default=False, nullable=False)
  created_at = db.Column(db.DateTime(timezone=True),default=uct_now,nullable=False)
  updated_at = db.Column(db.DateTime(timezone=True),default=uct_now,nullable=False)
  is_active = db.Column(db.Boolean, default=True, nullable=False)