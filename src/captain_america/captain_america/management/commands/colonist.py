# -*- coding: utf-8 -*-
import datetime
import multiprocessing
import os
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

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # 扫描控制表，更新定时任务
        interval = COLONIST_INTERVAL
        spider_script_path = os.path.join(os.path.dirname(os.getcwd()), SPIDER_PROJECT_NAME, SPIDER_PROJECT_SCRIPT)
        while True:
            my_user_cron = CronTab(user=True)

            control_id_map = {i.id: i for i in Control.objects.all()}
            control_id_set = set(control_id_map)
            crontab_id_map = {int(i.comment.split(' ')[-1]): i for i in my_user_cron.crons}
            crontab_id_set = set(crontab_id_map)
            for i in crontab_id_set - control_id_set:  # 删除Crontab
                crontab_id_map[i].delete()
            for i in control_id_set - crontab_id_set:  # 增加Crontab
                control = control_id_map[i]
                command = '%s %s' % (spider_script_path, i.code)
                comment = COLONIST_CRONTAB_COMMENT.format(i.id)
                self.update_crontab(my_user_cron.new(command), comment, control.cycle, control.is_disabled)

            # 定时更新Crontab
            offset_time = datetime.datetime.now() - datetime.timedelta(seconds=interval)
            control_qs = Control.objects.filter(is_disabled=False, update_time__gt=offset_time)
            for i in control_qs:
                command = '%s %s' % (spider_script_path, i.code)
                comment = COLONIST_CRONTAB_COMMENT.format(i.id)
                is_exist = False
                for j in my_user_cron.find_comment(comment):
                    self.update_crontab(j, comment, i.cycle, i.is_disabled, command)
                    is_exist = True
                if not is_exist:
                    self.update_crontab(my_user_cron.new(command), comment, i.cycle, i.is_disabled)

            my_user_cron.write()  # 写入Crontab操作
            time.sleep(interval)

    def update_crontab(self, job, comment, cycle, is_disabled, command=None):
        job.setcomment(comment)
        job.setall(cycle)
        job.enable(not is_disabled)
        if command is not None:
            job.set_command(command)
