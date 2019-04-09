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

            control_id_set = {i.id for i in Control.objects.all()}
            crontab_id_set = {int(i.comment.split(' ')[-1]): i for i in my_user_cron.crons}
            for k, v in crontab_id_set.items():
                if k not in control_id_set:
                    v.delete()

            offset_time = datetime.datetime.now() - datetime.timedelta(seconds=interval)
            control_qs = Control.objects.filter(is_disabled=False, update_time__gt=offset_time)
            for i in control_qs:
                command = '%s %s' % (spider_script_path, i.code)
                comment = COLONIST_CRONTAB_COMMENT.format(i.id)
                is_exist = False
                for j in my_user_cron.find_comment(comment):
                    self.update_crontab_job(j, i.cycle, command, i.is_disabled)
                    is_exist = True
                if not is_exist:
                    self.update_crontab_job(my_user_cron.new(), i.cycle, command, i.is_disabled)
                    
            my_user_cron.write()
            time.sleep(interval)

    def update_crontab_job(self, job, cycle, command, is_disabled):
        job.setall(cycle)
        job.command = command
        job.enable(not is_disabled)
