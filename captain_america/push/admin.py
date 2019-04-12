# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from push import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'site', 'channel', 'type', 'target', 'status', 'process_num', 'create_time',
                    'update_time', 'is_disabled']
    fields = ['site', 'channel', 'process_num', 'type', 'target', 'status', 'is_disabled']
    list_filter = ['target', 'type', 'status']
    actions = ['disable_multi', 'enable_multi']

    def disable_multi(self, request, queryset):
        queryset.update(is_disabled=True)
    disable_multi.short_description = u"禁用"

    def enable_multi(self, request, queryset):
        queryset.update(is_disabled=False)
    enable_multi.short_description = u"启用"
