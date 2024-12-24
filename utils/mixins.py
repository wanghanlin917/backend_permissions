from rest_framework.response import Response


class ListPageNumberModelMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        print('类型',type(queryset))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                "code": 0,
                "data": {"total": queryset.count(), 'page_size': self.paginator.page_size, "data": serializer.data}
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "code": 0,
            "data": serializer.data
        })
