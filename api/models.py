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


class Permission(models.Model):
    """权限"""
    title = models.CharField(verbose_name="标题", max_length=32)
    name = models.CharField(verbose_name="API代码", max_length=32)
    method_choices = (
        ('GET', "GET"),
        ('POST', "POST"),
        ('PUT', "PUT"),
        ('PATCH', "PATCH"),
        ('DELETE', "DELETE"),
    )
    method = models.CharField(verbose_name="方法", max_length=32, choices=method_choices)
    router = models.ForeignKey(verbose_name="关联路由", to=Router, on_delete=models.PROTECT)


class Role(models.Model):
    """角色表"""
    title = models.CharField(verbose_name="角色", max_length=32)
    permissions = models.ManyToManyField(verbose_name="权限", to=Permission, blank=True)


class Admin(models.Model):
    """用户表"""
    name = models.CharField(verbose_name="员工姓名", max_length=32)
    username = models.CharField(verbose_name="登录账号", max_length=32)
    phoneNumber = models.CharField(verbose_name="联系方式", max_length=11)
    password = models.CharField(verbose_name="密码", max_length=32)
    createTime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True, blank=True)
    roles = models.ForeignKey(verbose_name="角色", to=Role, on_delete=models.PROTECT)
    # roles = models.ManyToManyField(verbose_name="角色", to=Role, on_delete=models.PROTECT)
