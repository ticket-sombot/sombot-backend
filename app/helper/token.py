import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from app.helper.token_helper import get_token, token_validation


def generate_token(data):
    secret_key = os.environ.get("ACCESS_TOKEN_SECRET")
    expire_duration = int(os.environ.get("EXPIRE_DURATION_ACCESS"))

    token_duration = timedelta(days=expire_duration)

    exp = datetime.utcnow() + token_duration
    payload = {
        'exp': exp,
        'iat': datetime.utcnow(),
        'data': data
    }
    encoded_token = jwt.encode(payload, secret_key, algorithm="HS256")
    return encoded_token


def is_valid_token(token):
    secret_key = os.environ.get("ACCESS_TOKEN_SECRET")

    try:
        jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
        return True
    except:
        return False


def token_required(inner_function):
    @wraps(inner_function)
    def decorator(*args, **kwargs):

        token_validation()

        return inner_function(*args, **kwargs)
    return decorator


def decode_token(req):
    token_data = get_token()
    if token_data:
        return token_data[req]
    return None
