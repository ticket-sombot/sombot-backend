class Resp(object):
    def __init__(self, responseCode, errorCode, data, message=None):
        self.status = {
            "code": responseCode,
            "errorCode": errorCode,
            "error": message
        }
        self.data = data

    def parse(self):
        return self.__dict__
