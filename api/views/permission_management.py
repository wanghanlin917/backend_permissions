# from rest_framework import exceptions
# from rest_framework.views import APIView
# from rest_framework.viewsets import GenericViewSet
# from rest_framework.views import exception_handler
from rest_framework.filters import BaseFilterBackend
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework.response import Response
from api import models

from utils.viewsets import ModelViewSet
from utils.handlers import exception_handler
from utils.exception import ExtraException


class FolderViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Folder
        fields = '__all__'


class FolderView(ModelViewSet):
    queryset = models.Folder.objects.all()
    serializer_class = FolderViewSerializers

    def perform_destroy(self, instance):
        if models.Router.objects.filter(folder=instance).exists():
            raise ExtraException("无法删除，请先处理下级数据")
        instance.delete()


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Router
        fields = '__all__'


class RouterFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        folder = request.query_params.get('folder')
        if folder:
            queryset = queryset.filter(folder_id=folder)
        return queryset


class RouteView(ModelViewSet):
    queryset = models.Router.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [RouterFilterBackend]

    def perform_destroy(self, instance):
        if models.Permission.objects.filter(route=instance).exists():
            raise ExtraException("无法删除，请先处理下级数据")


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = '__all__'


class PermissionFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        route = request.query_params.get('router')
        if route:
            queryset = queryset.filter(router_id=route)
        return queryset


class PermissionView(ModelViewSet):
    queryset = models.Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [PermissionFilterBackend]

    @action(detail=False, methods=['get'], url_path='total', url_name='total')
    def total(self, request):
        # 1.获取目录
        folder_queryset = models.Folder.objects.all().values('id', 'title')
        folder_dict = {}
        for item in folder_queryset:
            item['id'] = f"folder-{item['id']}"
            item['children'] = []
            folder_dict[item['id']] = item
        # 2.获取路由
        router_queryset = models.Router.objects.all().values('id', 'title', "folder_id", "is_menu")
        router_dict = {}
        for item in router_queryset:
            item['id'] = f"router_{item['id']}"
            item['children'] = []
            if item['is_menu']:
                item['title'] = f"{item['title']}(菜单)"
            router_dict[item['id']] = item
            folder_id = f"folder-{item['folder_id']}"
            folder_dict[folder_id]['children'].append(item)
        # 3.获取权限
        permission_queryset = models.Permission.objects.all().values('id', 'title', 'router_id')
        for item in permission_queryset:
            router_id = f"router_{item['router_id']}"
            router_dict[router_id]['children'].append(item)
        return Response(folder_dict.values())


class RoleViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'


class RoleView(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = RoleViewSerializers
    # @
