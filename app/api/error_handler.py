from app.common.error import ErrorCode, ResponseCode
from app.common.response import Resp
from app import app


@app.errorhandler(400)
def not_found(e):
    return Resp(ResponseCode.INTERNAL_ERROR, ErrorCode.REQURED_FIELD_MISSING, None, "Your request data is missing field or invalid").parse(), e.code


@app.errorhandler(403)
def not_found(e):
    return Resp(ResponseCode.INTERNAL_ERROR, ErrorCode.UNAUTHORIZED, None, "Your request is unauthorized").parse(), e.code


@app.errorhandler(404)
def not_found(e):
    return Resp(ResponseCode.INTERNAL_ERROR, ErrorCode.NOT_FOUND, None, "Your request route not found").parse(), e.code


@app.errorhandler(500)
def not_found(e):
    return Resp(ResponseCode.INTERNAL_ERROR, ErrorCode.INTERNAL_SERVER_ERROR, None, "Our server is currently down").parse(), e.code
