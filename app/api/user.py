from crypt import methods
from flask import Blueprint, jsonify, request, abort
from app.helper import validation_req, generate_token, token_required
from app.model.database import User, PaymentMethod ,db, db_commit
from app.common import ResponseCode, ErrorCode, Resp
from werkzeug.security import generate_password_hash, check_password_hash

user = Blueprint("user", __name__, url_prefix="/api/user")


@user.route("/payment", methods=["POST"])
@token_required
def update_payment_method():
    req = request.json

    validated = validation_req(req, "bakongID")

    if not validated:
        abort(400)

    bakong_id = req.get("bakongID")

    bakong_data = bakong_id.split("@")

    if len(bakong_data) != 2:
        abort(400)

    payment_method = PaymentMethod(bakong_id=bakong_id)
    db_commit(payment_method)

    data = {"paymentMethod": "Bakong KHQR", "BakongID": bakong_id}

    return jsonify(Resp(ResponseCode.INTERNAL_SUCCESS, None, data, message="Successfully add Bakong Account").parse())


@user.route("/signup", methods=["POST"])
def create_user():
    req = request.json

    validated = validation_req(req, "phoneNumber", "name", "password")

    if not validated:
        abort(400)

    phone_number = req.get("phoneNumber")
    name = req.get("name")
    password = req.get("password")
    is_admin = req.get("isAdmin")

    existed_user = User.query.filter(User.phone_number == phone_number).first()

    if existed_user:
        return jsonify(Resp(ResponseCode.INTERNAL_ERROR, ErrorCode.USER_EXISTED, None, message="Phone number already signed up before").parse())

    hash_pw = generate_password_hash(password)

    user_role = "USER"

    if is_admin:
        user_role = "ADMIN"

    user = User(phone_number=phone_number, name=name,
                password=hash_pw, role=user_role)
    db_commit(user)

    access_token = generate_token({"phoneNumber": phone_number, "name": name})

    data = {"access_token": access_token}

    return jsonify(Resp(ResponseCode.INTERNAL_SUCCESS, None, data, message="Successfully signed up").parse())


@user.route("/login", methods=["POST"])
def login():
    req = request.json

    validated = validation_req(req, "phoneNumber", "password")

    if not validated:
        abort(400)

    phone_number = req.get("phoneNumber")
    password = req.get("password")

    existed_user = User.query.filter(User.phone_number == phone_number).first()

    if not existed_user:
        return jsonify(Resp(ResponseCode.INTERNAL_ERROR, ErrorCode.USER_NOT_EXISTED, None, message="User is not existed in our system").parse())

    is_correct_pw = check_password_hash(existed_user.password, password)

    if not is_correct_pw:
        return jsonify(Resp(ResponseCode.INTERNAL_ERROR, ErrorCode.UNAUTHORIZED, None, message="You have entered wrong password").parse())

    access_token = generate_token(
        {"phoneNumber": phone_number, "name": existed_user.name})

    data = {"access_token": access_token}

    return jsonify(Resp(ResponseCode.INTERNAL_SUCCESS, None, data, message="Successfully logged in").parse())
