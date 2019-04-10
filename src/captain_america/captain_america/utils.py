# -*- coding: utf-8 -*-
from django.db import models


class BaseModel(models.Model):  # 模型基类
    is_disabled = models.BooleanField(u"是否禁用", default=False)
    update_time = models.DateTimeField(u"更新时间", auto_now=True)
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-create_time"]


def get_model_field_name(model):
    """
    获取model的verbose_name和name的字段
    """
    return {i.name: i.verbose_name for i in model._meta.fields}
