from django.db import models


class Folder(models.Model):
    """一级菜单(目录)"""
    title = models.CharField(verbose_name="名称", max_length=32)
    icon = models.CharField(verbose_name="图表", max_length=32)


class Router(models.Model):
    """二级菜单(路由)"""
    title = models.CharField(verbose_name="标题", max_length=32)
    name = models.CharField(verbose_name="路由名称", max_length=32)
    is_menu = models.BooleanField(verbose_name="是否是菜单", default=True)
    folder = models.ForeignKey(verbose_name="菜单目录", to=Folder, on_delete=models.PROTECT)
