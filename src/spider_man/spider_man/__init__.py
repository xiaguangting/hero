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
models = import_module('spider.models')


def get_site(site_id):
    try:
        site = models.Site.objects.filter(id=site_id)[0]
    except:
        site = None
    return site


def get_task(site):
    task_qs = models.Task.objects.filter(site=site, is_disabled=False).order_by('-priority')
    task_qs.update(status=2)
    return task_qs


def is_exist(table, site, third_id):
    models_name = None
    if table == TABLE_MAP.get(u"视频"):
        models_name = "Video"
    if models_name:
        result = getattr(models, models_name).objects.filter(third_id=third_id, site=site)
        if result.exists():
            return True


def get_tag(name):
    tag_qs = models.Tag.objects.filter(name=name)
    if tag_qs:
        tag = tag_qs[0]
    else:
        tag = models.Tag.objects.create(name=name)
    return tag


def batch_video_tag_relation(video_tag_relation_list):
    models.VideoTag.objects.bulk_create(video_tag_relation_list)


def alter_task_status(task_id_list, status):
    models.Task.objects.filter(id__in=task_id_list).update(status=status)


def alter_attribute(model_name, id_list, alter_dict):
    getattr(models, model_name).objects.filter(pk__in=id_list).update(**alter_dict)


def get_user(task, third_id, name, avatar=None, description=None, fans_num=None, contact=None, address=None):
    if not third_id or not name:
        return
    user_qs = models.User.objects.filter(site=task.site, third_id=third_id)
    if user_qs:
        user = user_qs[0]
    else:
        user = models.User.objects.create(
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
