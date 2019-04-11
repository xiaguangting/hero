# -*- coding: utf-8 -*-
import json

import django
import requests

from captain_america.settings import FUNSHION_IMG_SERVER

django.setup()
# start
from multiprocessing import Process, Pool

from django.core.management.base import BaseCommand

from push.models import Task
from warehouse.models import Video


class Command(BaseCommand):
    help = 'Push'
    task_dict = {}

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # 扫描推送任务表
        pool = Pool(4)
        while True:
            task_qs = Task.objects.filter(is_disabled=False)
            for i in task_qs:
                pool.apply_async(sub_process_func, args=(i,))
            pool.close()
            pool.join()
            print 'bingo'


def sub_process_func(task):
    if task.type == Task.VIDEO:
        video_push(task)


def video_push(task):
    filter_fields, update_fields = {}, {}
    if task.target == Task.LINDA:
        push_func = linda_push
        status_fields = 'push_status_linda'
    else:
        return
    video_qs = Video.objects.filter(site=task.site, channel=task.channel, **{status_fields: Video.WAIT_PUSH})
    if video_qs:
        video_qs = video_qs.order_by('create_time')
        push_qs = video_qs[:100]  # 获取数据
        Video.objects.filter(id__in=[i.id for i in push_qs]).update(**{status_fields: Video.BEING_PUSH})  # 修改推送状态
        for i in push_qs:  # 执行推送
            try:
                result = push_func(i)
                if not result:
                    assert False, 'Failed to push'
            except:
                status_value = Video.WAIT_PUSH
            else:
                status_value = Video.FINISH_PUSH
            setattr(i, status_fields, status_value)
            i.save()


def pic_download(url):
    # pic_stream = requests.get(url).content
    # resp = requests.post(FUNSHION_IMG_SERVER, data=pic_stream, timeout=5)
    # pic_id = json.loads(resp.text).get('oid', '')
    pic_id = 'The picture service is not available'  # tmp
    return pic_id


def linda_push(video_object):
    if video_object.oid:
        return _linda_push(video_object)
    else:
        pic_id = pic_download(video_object.cover)
        if pic_id:
            video_object.oid = pic_id
            video_object.save()
            return _linda_push(video_object)


def _linda_push(video_object):
    return True
