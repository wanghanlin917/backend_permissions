from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.request import Request


class Login(APIView):
    def get(self, request):
        return Response({"code": 0, 'message': 'Login'})

    def post(self, request):
        return Response({"code": 0, 'message': 'Login', 'token': "54gd54g6dg56 "})


class UserInfo(APIView):
    def get(self, request):
        return Response({"code": 0, "data": {"user": "jk", "menus": [3]}})
