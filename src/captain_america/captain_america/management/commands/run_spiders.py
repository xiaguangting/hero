# -*- coding: utf-8 -*-
import datetime
import multiprocessing
import os
import sys
import time

from crontab import CronTab
from django.core.management.base import BaseCommand
from django.conf import settings

from captain_america.settings import RUN_SPIDERS_INTERVAL
from spider.models import Control


class Command(BaseCommand):
    help = 'Run spiders by Control'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # 扫描控制表，更新定时任务
        interval = RUN_SPIDERS_INTERVAL
        spider_script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'script')
        while True:
            offset_time = datetime.datetime.now() - datetime.timedelta(seconds=interval)
            print offset_time
            control_qs = Control.objects.filter(is_disabled=False, update_time__gt=offset_time)
            control_list = []
            my_user_cron = CronTab(user=True)
            for i in control_qs:
                job = my_user_cron.new(command='%s %s' % (spider_script_path, i.code))
                job.setall(i.cycle)
                job.set_comment("Captain_america")
            my_user_cron.write()
            time.sleep(interval)
