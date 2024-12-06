from rest_framework import exceptions


class ExtraException(exceptions.APIException):
    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        self.ret_code = code
