from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse


class AuthMiddleware(MiddlewareMixin):
    # def process_request(self, request):
    #     print(request)
    #     return request
    def process_request(self, request):
        if request.method == "OPTIONS":
            return HttpResponse("")

    def process_respon(self, request, response):
        # 任意网址
        response["Access-Control-Allow-Origin"] = "*"
        # 任意的请求方式
        response["Access-Control-Allow-Methods"] = "*"
        # 允许任意的请求头
        response["Access-Control-Allow-Headers"] = "*"
        return response
