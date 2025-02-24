from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from utils.jwt_auth import parse_payload
from utils.exception import ExtraException


class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if request.method == "OPTIONS":
            return
        authorization = request.META.get('HTTP_AUTHORIZATION')
        status, info_error = parse_payload(authorization)
        if not status:
            raise exceptions.AuthenticationFailed({"code": 401, "message": info_error})
            # raise ExtraException(info_error, ret_code=401)
            # return 'hbdjdh'
        return (info_error, authorization)

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return 'API realm="API"'


class JwtParamAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 1.读取请求头的token
        authorization = request.query_params.get('token')
        # 2.token验证
        status, info_or_error = parse_payload(authorization)
        # 3.校验失败，继续往后走
        if not status:
            return
        # 4.校验成功继续往后 request.user request.auth
        return (info_or_error, authorization)

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return 'API realm="API"'


class DenyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        raise exceptions.AuthenticationFailed({'code': 8888, 'msg': "认证失败"})

    def authenticate_header(self, request):
        return 'API realm="API"'
