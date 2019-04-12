# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from six import python_2_unicode_compatible

from captain_america.settings import MODEL_OBJECT_DISPLAY
from captain_america.utils import BaseModel
from spider.models import Site, Channel


@python_2_unicode_compatible
class Task(BaseModel):
    WAIT_GET, BEING_EXECUTE = 1, 2
    LINDA = 1
    VIDEO = 1
    STATUS_LIST = [
        (WAIT_GET, u"待领取"),
        (BEING_EXECUTE, u"执行中")
    ]
    TARGET_LIST = [
        (LINDA, u'Linda')
    ]
    TYPE_LIST = [
        (VIDEO, u'视频')
    ]

    site = models.ForeignKey(Site, verbose_name="站点", related_name='push_task_set')
    channel = models.ForeignKey(Channel, verbose_name="频道", null=True, related_name='push_channel_set', blank=True)
    target = models.PositiveSmallIntegerField(choices=TARGET_LIST, default=1, verbose_name=u"目标")
    type = models.PositiveSmallIntegerField(choices=TYPE_LIST, default=1, verbose_name=u"类型")
    status = models.PositiveSmallIntegerField(choices=STATUS_LIST, default=1, verbose_name=u"状态")
    process_num = models.IntegerField(verbose_name=u'进程数', default=1)

    class Meta:
        verbose_name = verbose_name_plural = u'任务'

    def __str__(self):
        return MODEL_OBJECT_DISPLAY.format('PushTask', self.id)
