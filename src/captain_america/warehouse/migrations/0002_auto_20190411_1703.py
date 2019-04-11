# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-11 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='push_status',
        ),
        migrations.AddField(
            model_name='video',
            name='push_status_linda',
            field=models.PositiveSmallIntegerField(choices=[(1, '\u5f85\u63a8\u9001'), (2, '\u63a8\u9001\u4e2d'), (3, '\u5df2\u63a8\u9001')], default=1, verbose_name='\u63a8\u9001\u72b6\u6001(Linda)'),
        ),
    ]