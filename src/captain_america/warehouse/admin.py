# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from warehouse import models


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'site', 'cover_show', 'name', 'play', 'channel', 'duration', 'play_num', 'like_num',
                    'comment_num', 'user', 'upload_time', 'third_id', 'oid', 'push_status_linda', 'create_time', 'update_time',
                    'is_disabled']
    list_filter = ['push_status_linda']
    search_fields = ['name']
    list_per_page = 10

    def cover_show(self, obj):
        if obj.cover:
            return u'<img src="%s" width="100">' % obj.cover
        else:
            return u"无封面"
    cover_show.allow_tags = True
    cover_show.short_description = u'封面'

    def play(self, obj):
        if obj.url:
            return u'<a href="%s" target="_blank" rel="noreferrer">播放</a>' % obj.url
        else:
            return u"无播放地址"
    play.allow_tags = True
    play.short_description = u'播放地址'


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'site', 'avatar_show', 'name', 'description', 'fans_num', 'contact', 'address', 'third_id', 'create_time', 'update_time', 'is_disabled']

    def avatar_show(self, obj):
        if obj.avatar:
            return u'<img src="%s" width="30">' % obj.avatar
        else:
            return u"无头像"
    avatar_show.allow_tags = True
    avatar_show.short_description = u'头像'


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'create_time', 'update_time', 'is_disabled']


@admin.register(models.VideoTag)
class VideoTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'video', 'tag', 'create_time', 'update_time', 'is_disabled']
