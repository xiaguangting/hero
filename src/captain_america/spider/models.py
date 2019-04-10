# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from six import python_2_unicode_compatible

from captain_america.settings import MODEL_OBJECT_DISPLAY
from captain_america.utils import BaseModel


@python_2_unicode_compatible
class Site(BaseModel):
    name = models.CharField(max_length=32, verbose_name=u'名称')

    class Meta:
        verbose_name = verbose_name_plural = u'站点'

    def __str__(self):
        return MODEL_OBJECT_DISPLAY.format(self.id, self.name)


@python_2_unicode_compatible
class Control(BaseModel):
    site = models.ForeignKey(Site, verbose_name="站点")
    code = models.CharField(max_length=32, verbose_name=u'爬虫CODE')
    cycle = models.CharField(max_length=64, verbose_name=u'执行周期', null=True)
    system_info = models.CharField(max_length=64, verbose_name=u'系统信息', null=True)
    # num = models.IntegerField(verbose_name=u'数量', default=1)
    # minute = models.CharField(verbose_name=u'分钟', max_length=16, default='*')
    # hour = models.CharField(verbose_name=u'小时', max_length=16, default='*')
    # day = models.CharField(verbose_name=u'天', max_length=16, default='*')
    # month = models.CharField(verbose_name=u'月', max_length=16, default='*')
    # week = models.CharField(verbose_name=u'周', max_length=16, default='*')

    class Meta:
        verbose_name = verbose_name_plural = u'控制'

    def __str__(self):
        return MODEL_OBJECT_DISPLAY.format(u'Control', self.id)


class Channel(BaseModel):
    name = models.CharField(max_length=32, verbose_name=u'名称')

    class Meta:
        verbose_name = verbose_name_plural = u'频道'


@python_2_unicode_compatible
class Task(BaseModel):
    STATUS_LIST = [
        (1, u"待领取"),
        (2, u"执行中"),
    ]
    TYPE_LIST = [
        (1, u'全量'),
        (2, u'增量')
    ]

    site = models.ForeignKey(Site, verbose_name="站点")
    name = models.CharField(max_length=128, verbose_name=u'名称', null=True, blank=True)
    url = models.CharField(max_length=256, verbose_name="地址")
    priority = models.IntegerField(verbose_name=u'优先级')
    status = models.PositiveSmallIntegerField(choices=STATUS_LIST, default=1, verbose_name=u"状态")
    type = models.PositiveSmallIntegerField(choices=TYPE_LIST, default=1, verbose_name=u"类型")

    class Meta:
        verbose_name = verbose_name_plural = u'任务'

    def __str__(self):
        name = self.name if self.name else ''
        return MODEL_OBJECT_DISPLAY.format(self.id, name)
