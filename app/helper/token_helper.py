from flask import request, abort
import jwt, os


def token_validation():
    header = request.headers
    _token = None
    secret_key = os.environ.get("ACCESS_TOKEN_SECRET")

    if 'Authorization' in header:
        token_with_head = header['Authorization'].split(" ")

        if len(token_with_head) != 2 or token_with_head[0] != "Bearer":
            abort(403)

        _token = token_with_head[1]

    if not _token:
        abort(403)

    try:
        jwt.decode(_token.encode(), secret_key, algorithms=["HS256"])
    except:
        return abort(403)


def get_token():
    secret_key = os.environ.get("ACCESS_TOKEN_SECRET")

    token = request.headers['Authorization'].split(" ")[1]
    data = None

    try:
        data = jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
    except:
        return None
    return data["data"]

