# from rest_framework import exceptions
# from rest_framework.views import APIView
# from rest_framework.viewsets import GenericViewSet
from rest_framework.views import exception_handler
from rest_framework.filters import BaseFilterBackend
from rest_framework import serializers
from api import models

from utils.viewsets import ModelViewSet
from utils.handlers import exception_handler


class FolderViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Folder
        fields = '__all__'


class FolderView(ModelViewSet):
    queryset = models.Folder.objects.all()
    serializer_class = FolderViewSerializers

    def perform_destroy(self, instance):
        if models.Router.objects.filter(folder=instance).exists():
            raise exception_handler("无法删除，请先处理下级数据")
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
