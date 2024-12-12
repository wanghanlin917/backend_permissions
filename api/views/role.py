from api.models import Role
from utils.viewsets import ModelViewSet
from rest_framework import serializers
from api import models


class RoleViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'


class RoleView(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = RoleViewSerializers
