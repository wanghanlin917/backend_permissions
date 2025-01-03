# Generated by Django 5.1.4 on 2024-12-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_delete_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='员工姓名')),
                ('username', models.CharField(max_length=32, verbose_name='登录账号')),
                ('phoneNumber', models.CharField(max_length=11, verbose_name='联系方式')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('createTime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('roles', models.ManyToManyField(blank=True, to='api.role', verbose_name='角色')),
            ],
        ),
    ]