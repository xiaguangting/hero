# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from spider import models


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'create_time', 'update_time', 'is_disabled']


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'site', 'name', 'url', 'priority', 'type', 'status', 'create_time', 'update_time', 'is_disabled']
    fields = ['site', 'name', 'url', 'priority', 'type', 'is_disabled']
    list_filter = ['status']
    actions = ['disable_multi', 'enable_multi', 'full_multi', 'increment_multi']

    def disable_multi(self, request, queryset):
        queryset.update(is_disabled=True)
    disable_multi.short_description = u"禁用"

    def enable_multi(self, request, queryset):
        queryset.update(is_disabled=False)
    enable_multi.short_description = u"启用"

    def full_multi(self, request, queryset):
        queryset.update(type=1)
    full_multi.short_description = u"全量"

    def increment_multi(self, request, queryset):
        queryset.update(type=2)
    increment_multi.short_description = u"增量"


@admin.register(models.Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = ['id', 'site', 'code', 'cycle', 'create_time', 'update_time',
                    'is_disabled']


@admin.register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'create_time', 'update_time', 'is_disabled']


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'site', 'cover_show', 'name', 'play', 'channel', 'duration', 'play_num', 'like_num',
                    'comment_num', 'user', 'upload_time', 'third_id', 'oid', 'push_status', 'create_time', 'update_time',
                    'is_disabled']
    list_filter = ['push_status']
    search_fields = ['name']

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
