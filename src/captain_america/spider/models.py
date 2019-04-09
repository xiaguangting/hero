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


class CrawlData(BaseModel):
    task = models.ForeignKey(Task, null=True, verbose_name="任务")
    site = models.ForeignKey(Site, verbose_name="站点")
    third_id = models.CharField(max_length=64, null=True, verbose_name=u"第三方ID")

    class Meta:
        abstract = True


@python_2_unicode_compatible
class User(CrawlData):
    name = models.CharField(max_length=64, verbose_name=u'名称')
    avatar = models.CharField(max_length=256, null=True, verbose_name=u'头像')
    description = models.CharField(max_length=256, null=True, verbose_name=u'描述')
    fans_num = models.IntegerField(null=True, verbose_name=u'粉丝数')
    contact = models.CharField(max_length=256, null=True, verbose_name=u'联系方式')
    address = models.CharField(max_length=256, null=True, verbose_name=u'地址')

    class Meta:
        verbose_name = verbose_name_plural = u'用户'

    def __str__(self):
        return MODEL_OBJECT_DISPLAY.format(self.id, self.name)


@python_2_unicode_compatible
class Video(CrawlData):
    PUSH_STATUS_LIST = [
        (1, u"待推送"),
        (2, u"推送中"),
        (3, u"已推送")
    ]

    name = models.CharField(max_length=256, verbose_name=u'名称')
    cover = models.CharField(max_length=512, verbose_name=u'封面')
    url = models.CharField(max_length=512, verbose_name=u'播放地址')

    channel = models.ForeignKey(Channel, verbose_name="频道", null=True)
    duration = models.IntegerField(verbose_name=u"时长", null=True)
    play_num = models.IntegerField(verbose_name=u'播放数', null=True)
    like_num = models.IntegerField(verbose_name=u'喜欢数', null=True)
    comment_num = models.IntegerField(verbose_name=u'评论数', null=True)
    user = models.ForeignKey(User, verbose_name=u"用户", null=True)
    upload_time = models.DateTimeField(verbose_name=u"用户上传时间", null=True)

    oid = models.CharField(max_length=64, verbose_name=u'风行图片ID', null=True)
    push_status = models.PositiveSmallIntegerField(choices=PUSH_STATUS_LIST, default=1, verbose_name=u"推送状态")
    is_parse = models.BooleanField(u"是否解析Url", default=False)

    class Meta:
        verbose_name = verbose_name_plural = u'视频'

    def __str__(self):
        return MODEL_OBJECT_DISPLAY.format(self.id, self.name)


@python_2_unicode_compatible
class Tag(BaseModel):
    name = models.CharField(u"名称", max_length=128)

    class Meta:
        verbose_name = verbose_name_plural = u'标签'

    def __str__(self):
        return MODEL_OBJECT_DISPLAY.format(self.id, self.name)


class VideoTag(BaseModel):
    video = models.ForeignKey(Video, verbose_name=u"视频")
    tag = models.ForeignKey(Tag, verbose_name=u"标签")

    class Meta:
        verbose_name = verbose_name_plural = u'视频与标签'
