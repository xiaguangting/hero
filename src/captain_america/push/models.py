# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from six import python_2_unicode_compatible

from captain_america.settings import MODEL_OBJECT_DISPLAY
from captain_america.utils import BaseModel
from spider.models import Site, Channel


@python_2_unicode_compatible
class Task(BaseModel):
    STATUS_LIST = [
        (1, u"待推送"),
        (2, u"推送中"),
        (3, u"已推送")
    ]
    TYPE_LIST = [
        (1, u'Linda')
    ]

    site = models.ForeignKey(Site, verbose_name="站点")
    channel = models.ForeignKey(Channel, verbose_name="频道", null=True)
    name = models.CharField(max_length=128, verbose_name=u'名称', null=True, blank=True)
    priority = models.IntegerField(verbose_name=u'优先级')
    status = models.PositiveSmallIntegerField(choices=STATUS_LIST, default=1, verbose_name=u"状态")
    type = models.PositiveSmallIntegerField(choices=TYPE_LIST, default=1, verbose_name=u"目标")

    class Meta:
        verbose_name = verbose_name_plural = u'任务'

    def __str__(self):
        name = self.name if self.name else ''
        return MODEL_OBJECT_DISPLAY.format(self.id, name)
