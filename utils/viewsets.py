from rest_framework.viewsets import GenericViewSet as DrfGenericViewSet
from rest_framework import mixins
from rest_framework.views import APIView

from utils.mixins import ListPageNumberModelMixin


class GenericViewSet(DrfGenericViewSet):
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if response.exception:
            return response
        # print("dddd", response.data)
        response.data = {'code': 0, 'data': response.data}
        # print("ssss", response.data)
        return response


class ModelViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                   mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    pass



