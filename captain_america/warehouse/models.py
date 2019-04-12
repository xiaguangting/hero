# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from six import python_2_unicode_compatible

from captain_america.settings import MODEL_OBJECT_DISPLAY
from captain_america.utils import BaseModel
from spider.models import Task, Site, Channel


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
    WAIT_PUSH, BEING_PUSH, FINISH_PUSH = 1, 2, 3
    PUSH_STATUS_LINDA_LIST = [
        (WAIT_PUSH, u"待推送"),
        (BEING_PUSH, u"推送中"),
        (FINISH_PUSH, u"已推送")
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
    push_status_linda = models.PositiveSmallIntegerField(choices=PUSH_STATUS_LINDA_LIST, default=1,
                                                         verbose_name=u"推送状态(Linda)")
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

