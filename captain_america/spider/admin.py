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
    list_display = ['id', 'site', 'code', 'cycle', 'system_info', 'create_time', 'update_time',
                    'is_disabled']


@admin.register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'create_time', 'update_time', 'is_disabled']
