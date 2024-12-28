from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from rest_framework.mixins import CreateModelMixin
from utils.viewsets import GenericViewSet

from rest_framework.request import Request


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Admin
        fields = ['username', 'password']
    # def get(self, request):
    #     return Response({"code": 0, 'message': 'Login'})
    #
    # def post(self, request):
    #     return Response({"code": 0, 'message': 'Login', 'token': "54gd54g6dg56 "})


class LoginView(CreateModelMixin, GenericViewSet):
    queryset = models.Admin.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        return Response("....")


class UserInfo(APIView):
    def get(self, request):
        return Response({"code": 0, "data": {"user": "jk", "menus": [{
            "title": "权限管理",
            "icon": "user",
            "child": [{"title": "菜单", "frontpath": "/menu"}, {"title": "角色", "frontpath": "/role"},
                      {"title": "用户", "frontpath": "/user"}]
        }, {"title": "vip管理", "icon": "flag"}]}})
