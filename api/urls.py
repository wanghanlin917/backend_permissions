from django.urls import path
from .views.login import Login, UserInfo
from .views.permission_management import FolderView, RouteView, PermissionView,RoleView
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'folder', FolderView, basename='folder')
router.register('route', RouteView, basename='route')
router.register('permission', PermissionView, basename='permission')
router.register('role', RoleView, basename='role')

urlpatterns = [
    path('user/login', Login.as_view()),
    path('user/userinfo', UserInfo.as_view()),

]

urlpatterns += router.urls
