from django.urls import path
from .views.login import LoginView, UserInfo
from .views.permission_management import FolderView, RouteView, PermissionView, RoleView, AdminView
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'folder', FolderView, basename='folder')
router.register('route', RouteView, basename='route')
router.register('permission', PermissionView, basename='permission')
router.register('role', RoleView, basename='role')
router.register('admin', AdminView, basename='admin')
router.register('user/login', LoginView, basename='login')
router.register('user/userinfo', UserInfo, basename='userinfo')

urlpatterns = [
]

urlpatterns += router.urls
