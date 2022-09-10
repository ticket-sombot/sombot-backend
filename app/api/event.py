from datetime import datetime
from flask import Blueprint, jsonify, request, abort
from app.helper import validation_req, generate_token, token_required
from app.model.database import Event, db, db_commit
from app.common import ResponseCode, ErrorCode, Resp
import re

event = Blueprint("event", __name__, url_prefix="/api/event")

pattern = re.compile("(^(((0[1-9]|1[0-9]|2[0-8])[\/](0[1-9]|1[012]))|((29|30|31)[\/](0[13578]|1[02]))|((29|30)[\/](0[4,6,9]|11)))[\/](19|[2-9][0-9])\d\d$)|(^29[\/]02[\/](19|[2-9][0-9])(00|04|08|12|16|20|24|28|32|36|40|44|48|52|56|60|64|68|72|76|80|84|88|92|96)$)")


@event.route("/", methods=["GET"])
@token_required
def get_event_detail():
    event = Event.query.first()
    data = event if event else []
    return jsonify(Resp(ResponseCode.INTERNAL_SUCCESS, None, data, message="Event queried").parse())


@event.route("/create", methods=["POST"])
@token_required
def create_event():
    req = request.json

    validated = validation_req(req, "name", "description", "price", "date")

    if not validated:
        abort(400)

    name = req.get("name")
    description = req.get("description")
    price = req.get("price")
    date = req.get("date")

    if not pattern.match(date):
        abort(400)

    event_date = datetime.strptime(date, "%d/%m/%Y")

    event = Event(name=name, description=description,
                  price=price, date=event_date)
    db_commit(event)

    return jsonify(Resp(ResponseCode.INTERNAL_SUCCESS, None, None, message="Successfully create event").parse())


@event.route("/update/<id>", methods=["POST"])
@token_required
def update_event(id):
    event = Event.query.filter(Event.id == id).first()

    if not event:
        return jsonify(Resp(ResponseCode.INTERNAL_ERROR, ErrorCode.EVENT_NOT_EXIST, None, message="Event is not existed in our system").parse())

    req = request.json

    validated = validation_req(req, "name", "description", "price", "date")

    if not validated:
        abort(400)

    name = req.get("name")
    description = req.get("description")
    price = req.get("price")
    date = req.get("date")

    if not pattern.match(date):
        abort(400)

    event_date = datetime.strptime(date, "%d/%m/%Y")

    event.name = name
    event.description = description
    event.price = price
    event.date = event_date

    db.session.commit()

    return jsonify(Resp(ResponseCode.INTERNAL_SUCCESS, None, None, message="Successfully update event").parse())


@event.route("/delete/<id>", methods=["POST"])
@token_required
def delete_event(id):
    event = Event.query.filter(Event.id == id)

    if not event.first():
        return jsonify(Resp(ResponseCode.INTERNAL_ERROR, ErrorCode.EVENT_NOT_EXIST, None, message="Event is not existed in our system").parse())

    event.delete()
    db.session.commit()

    return jsonify(Resp(ResponseCode.INTERNAL_SUCCESS, None, None, message="Successfully delete event").parse())
