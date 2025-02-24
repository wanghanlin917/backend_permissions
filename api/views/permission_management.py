# from rest_framework import exceptions
# from rest_framework.views import APIView
from utils.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
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
        if models.Permission.objects.filter(router=instance).exists():
            raise ExtraException("无法删除，请先处理下级数据")
        instance.delete()


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

    @action(detail=True, methods=['get'], url_path='permission', url_name='permission')
    def permission(self, request, pk):
        print("pk参数",pk)
        instance = self.get_object()
        permission = instance.permissions.all()
        permission_list = [item.id for item in permission]
        # print(permission_list)
        return Response(permission_list)

    @action(detail=True, methods=['post'], url_path='update/permission', url_name='update_permission')
    def update_permission(self, request, pk):
        # 获取权限列表
        permission_id_list = request.data.get('permissions')
        print(permission_id_list)
        # permission_id_list = list(set(permission_id_list))
        instance = self.get_object()
        instance.permissions.set(permission_id_list)
        return Response('ok')


from rest_framework.pagination import PageNumberPagination
from utils.mixins import ListPageNumberModelMixin
from rest_framework.filters import BaseFilterBackend


# from rest_framework.mixins import ListModelMixin
# from rest_framework import viewsets
# from rest_framework.mixins import ListModelMixin


class AdminPaginator(PageNumberPagination):
    page = 1
    page_size = 5
    # print(page_size)
    # page_size_query_param = 'page_size',
    # max_page_size = 100


class AdminFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        username = request.query_params.get('username')
        print("username", username)
        if username:
            queryset = queryset.filter(name=username)
        return queryset


class AdminRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = ['id', 'title']


class AdminSerializer(serializers.ModelSerializer):
    roles_display = AdminRoleSerializer(source='roles', read_only=True)
    createTime = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = models.Admin
        fields = ['id', 'name', 'username', 'password', 'phoneNumber', 'createTime', 'roles', 'roles_display']

    extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        print("参数", attrs)
        return attrs


class AdminView(ListPageNumberModelMixin,CreateModelMixin,GenericViewSet):
    queryset = models.Admin.objects.all().order_by('-id')
    serializer_class = AdminSerializer
    pagination_class = AdminPaginator
    filter_backends = [AdminFilter,]

    # def get(self, request, *args, **kwargs):
    #     """
    #     处理 GET 请求，返回分页结果。
    #     """
    #     return self.list(request, *args, **kwargs)
