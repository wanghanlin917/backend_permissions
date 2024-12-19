from rest_framework import exceptions


class ExtraException(exceptions.APIException):
    def __init__(self, detail=None, ret_code=None, code=None):
        super().__init__(detail, code)
        self.ret_code = ret_code
