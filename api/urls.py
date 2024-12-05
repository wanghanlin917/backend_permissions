from django.urls import path
from .views.login import Login,UserInfo

urlpatterns = [
    path('user/login', Login.as_view()),
    path('user/userinfo',UserInfo.as_view())

]
