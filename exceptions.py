class ApiException(Exception):
    def __init__(self, msg, code=500):
        self.msg = msg
        self.code = code

    def __str__(self):
        return "msg: {msg} code: {code}".format(msg=self.msg, code=self.code)
