from dataclasses import dataclass
from app.model import db
from datetime import datetime
import string, random

def gen_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=24))

@dataclass
class PaymentMethod(db.Model):
    id: str
    bakong_id: str

    id = db.Column(db.String(48), primary_key=True, default=gen_id)
    bakong_id = db.Column(db.String(32))

@dataclass
class User(db.Model):
    id: str
    phone_number: str
    name: str
    password: str
    role: str
    status: str

    id = db.Column(db.String(48), primary_key=True, default=gen_id)
    phone_number = db.Column(db.String(11))
    name = db.Column(db.String(64))
    password = db.Column(db.String(128))
    role = db.Column(db.String(16), default="USER")
    status = db.Column(db.String(16), default="ACTIVE")
    date = db.Column(db.DateTime, default=datetime.utcnow)


@dataclass
class Event(db.Model):
    id: str
    name: str
    description: str
    price: int
    date: str

    id = db.Column(db.String(48), primary_key=True, default=gen_id)
    name = db.Column(db.String(128))
    description = db.Column(db.String(1024))
    price = db.Column(db.Integer)
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

