from dataclasses import dataclass
from app.model import db
from datetime import datetime
import string, random

def gen_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=24))

@dataclass
class User(db.Model):
    id: str
    phone_number: str
    name: str
    password: str
    status: str

    id = db.Column(db.String(48), primary_key=True, default=gen_id)
    phone_number = db.Column(db.String(11))
    name = db.Column(db.String(64))
    password = db.Column(db.String(128))
    status = db.Column(db.String(16), default="ACTIVE")
    date = db.Column(db.DateTime, default=datetime.utcnow)


# actions
from flask import abort

def db_commit(obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception:
        db.session.rollback()
        abort(400)

