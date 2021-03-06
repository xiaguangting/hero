# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-08 13:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_disabled', models.BooleanField(default=False, verbose_name='\u662f\u5426\u7981\u7528')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('code', models.CharField(max_length=32, verbose_name='\u722c\u866bCODE')),
                ('num', models.IntegerField(default=1, verbose_name='\u6570\u91cf')),
                ('minute', models.CharField(default='*', max_length=16, verbose_name='\u5206\u949f')),
                ('hour', models.CharField(default='*', max_length=16, verbose_name='\u5c0f\u65f6')),
                ('day', models.CharField(default='*', max_length=16, verbose_name='\u5929')),
                ('month', models.CharField(default='*', max_length=16, verbose_name='\u6708')),
                ('week', models.CharField(default='*', max_length=16, verbose_name='\u5468')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spider.Site', verbose_name='\u7ad9\u70b9')),
            ],
            options={
                'verbose_name': '\u63a7\u5236',
                'verbose_name_plural': '\u63a7\u5236',
            },
        ),
    ]
