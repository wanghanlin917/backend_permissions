from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from utils.viewsets import GenericViewSet
from utils.exception import ExtraException
from utils.jwt_auth import create_token
from utils.auth import JwtAuthentication, JwtParamAuthentication, DenyAuthentication

from rest_framework.request import Request


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Admin
        fields = ['id', 'username', 'password']


class LoginView(CreateModelMixin, GenericViewSet):
    queryset = models.Admin.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = models.Admin.objects.filter(username=serializer.data['username']).first()
        # print("token", token)
        admin_object = models.Admin.objects.filter(**serializer.data).first()
        if not admin_object:
            raise ExtraException("用户名或密码错误", ret_code=9999)
        token = create_token({"user_id": instance.id, "username": instance.username})
        return Response({"token": token})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Admin
        filter = "__all__"


class UserInfo(ListModelMixin, GenericViewSet):
    authentication_classes = [JwtAuthentication, JwtParamAuthentication, DenyAuthentication]
    queryset = models.Admin.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        username = request.user["username"]
        admin_object = queryset.filter(username=username).first()
        # print(admin_object)
        # result =  admin_object.objects.prefetch_related('roles__permissions')
        result = admin_object.roles.permissions.values('id', 'title', 'name',
                                                       'method', 'router_id')
        # 提取路由
        routers = set()
        permissions = {}
        folder_dict = {}
        router_dict = {}
        for item in result:
            if item['name'] not in permissions:
                permissions[item['name']] = [item["method"], ]
            else:
                permissions[item['name']].append(item["method"])
            routers.add(item['router_id'])
        for index in routers:
            route = models.Router.objects.filter(id=index).first()
            router_dict[index] = route.name
            folder_id = route.folder_id
            # print("一级菜单", route.folder.title)
            if folder_id not in folder_dict:
                folder_dict[folder_id] = {
                    "title": route.folder.title,
                    "icon": route.folder.icon,
                    "child": []
                }
                if route.is_menu:
                    folder_dict[folder_id]["child"].append({
                        "title": route.title,
                        "frontpath": route.name
                    })
            else:
                if route.is_menu:
                    folder_dict[folder_id]["child"].append({
                        "title": route.title,
                        "frontpath": route.name
                    })
        print(permissions)
        return Response(
            {"menus": folder_dict.values(), "permissions": permissions, "routers": router_dict.values()})

        # return Response({"user": "jk", "menus": [{
        #     "title": "权限管理",
        #     "icon": "user",
        #     "meta": {"order": 3},
        #     "child": [{"title": "菜单", "frontpath": "/menu"}, {"title": "角色", "frontpath": "/role"},
        #               {"title": "用户", "frontpath": "/user"}]
        # }, {"title": "vip管理", "icon": "flag", "meta": {"order": 2}}, {"title": "hahahaha", "meta": {"order": 1}}]})

        # def get(self, request):
        #     return Response({"code": 0, "data": {"user": "jk", "menus": [{
        #         "title": "权限管理",
        #         "icon": "user",
        #         "meta": {"order": 3},
        #         "child": [{"title": "菜单", "frontpath": "/menu"}, {"title": "角色", "frontpath": "/role"},
        #                   {"title": "用户", "frontpath": "/user"}]
        #     }, {"title": "vip管理", "icon": "flag", "meta": {"order": 2}}, {"title": "hahahaha", "meta": {"order": 1}}]}})
