# -*- coding:utf-8 -*-
import os
import sys
from importlib import import_module

import django

from spider_man.settings import TABLE_MAP

sys.path.append(os.path.join(os.path.abspath('.'), '..', 'captain_america'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'captain_america.settings'
django.setup()

# captain_america
spider_models = import_module('spider.models')
warehouse_models = import_module('warehouse.models')


def get_site(site_id):
    try:
        site = spider_models.Site.objects.filter(id=site_id)[0]
    except:
        site = None
    return site


def get_task(site):
    task_qs = spider_models.Task.objects.filter(site=site, is_disabled=False).order_by('-priority')
    task_qs.update(status=2)
    return task_qs


def get_tag(name):
    tag_qs = warehouse_models.Tag.objects.filter(name=name)
    if tag_qs:
        tag = tag_qs[0]
    else:
        tag = warehouse_models.Tag.objects.create(name=name)
    return tag


def get_user(task, third_id, name, avatar=None, description=None, fans_num=None, contact=None, address=None):
    if not third_id or not name:
        return
    user_qs = warehouse_models.User.objects.filter(site=task.site, third_id=third_id)
    if user_qs:
        user = user_qs[0]
    else:
        user = warehouse_models.User.objects.create(
            task=task,
            site=task.site,
            third_id=third_id,
            name=name,
            avatar=avatar,
            description=description,
            fans_num=fans_num,
            contact=contact,
            address=address
        )
    return user


def is_exist(table, site, third_id):
    models_name = None
    if table == TABLE_MAP.get(u"视频"):
        models_name = "Video"
    if models_name:
        result = getattr(warehouse_models, models_name).objects.filter(third_id=third_id, site=site)
        if result.exists():
            return True
