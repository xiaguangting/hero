# -*- coding: utf-8 -*-
import datetime
import multiprocessing
import os
import re
import sys
import time

from crontab import CronTab
from django.core.management.base import BaseCommand
from django.conf import settings

from captain_america.settings import COLONIST_INTERVAL, SPIDER_PROJECT_NAME, SPIDER_PROJECT_SCRIPT, \
    COLONIST_CRONTAB_COMMENT
from spider.models import Control


class Command(BaseCommand):
    help = 'Run spiders by Control'
    spider_script_path = os.path.join(os.path.dirname(os.getcwd()), SPIDER_PROJECT_NAME, SPIDER_PROJECT_SCRIPT)
    comment_pattern = re.compile(COLONIST_CRONTAB_COMMENT.format('(\d+)'))

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # 扫描控制表，更新定时任务
        while True:
            my_user_cron = CronTab(user=True)
            self.prepare(my_user_cron)
            self.main(my_user_cron)
            my_user_cron.write()  # 写入Crontab操作
            time.sleep(COLONIST_INTERVAL)

    def prepare(self, crontab):  # 预处理
        control_id_map = {i.id: i for i in Control.objects.all()}
        control_id_set = set(control_id_map)
        crontab_id_map = dict()
        for i in crontab.crons:  # 寻找对应规则的注释
            result = self.comment_pattern.findall(i.comment)
            if result:
                crontab_id_map[int(result[0])] = i
        crontab_id_set = set(crontab_id_map)
        for i in crontab_id_set - control_id_set:  # 删除Crontab
            crontab_id_map[i].delete()
        for i in control_id_set - crontab_id_set:  # 增加Crontab
            self.add_crontab(crontab, control_id_map[i])

    def main(self, crontab):  # 更新Crontab
        offset_time = datetime.datetime.now() - datetime.timedelta(seconds=COLONIST_INTERVAL)
        control_qs = Control.objects.filter(update_time__gt=offset_time)
        for i in control_qs:
            is_exist = False
            for j in crontab.find_comment(COLONIST_CRONTAB_COMMENT.format(i.id)):
                self.alter_crontab(j, i)
                is_exist = True
            if not is_exist:
                self.add_crontab(crontab, i)

    def alter_crontab(self, job, model_object):
        job.set_command('%s %s' % (self.spider_script_path, model_object.code))
        job.setall(model_object.cycle)
        job.enable(not model_object.is_disabled)

    def add_crontab(self, crontab, model_object):
        command = '%s %s' % (self.spider_script_path, model_object.code)
        comment = COLONIST_CRONTAB_COMMENT.format(model_object.id)
        job = crontab.new(command, comment)
        job.setall(model_object.cycle)
        job.enable(not model_object.is_disabled)
