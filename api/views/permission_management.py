from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.views import exception_handler
from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers
from api import models

from utils.viewsets import ModelViewSet


class FolderViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Folder
        fields = '__all__'


class FolderView(ModelViewSet):
    queryset = models.Folder.objects.all()
    serializer_class = FolderViewSerializers



