import multiprocessing
import os
import time
from multiprocessing import Process

from django.core.management.base import BaseCommand
from django.conf import settings

from spider.models import Control


class Command(BaseCommand):
    help = 'Run spiders by Control'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        unique_set, process_list = set(), []
        while True:
            unique_set_new = set()
            for i in Control.objects.filter(is_disabled=False):
                unique_set_new.add(
                    ':'.join([str(i.site_id), i.code, str(i.num), i.minute, i.hour, i.day, i.month, i.week]))
            for i in unique_set_new - unique_set & unique_set_new:
                print 'test'
                process_list.append(Process(target=RunSpider, kwargs={'unique_id': i}))
            unique_set = unique_set_new

            for i in process_list:
                i.start()
            for i in process_list:
                i.join()
            print 'end'
            time.sleep(60)


class RunSpider(object):
    def __init__(self, unique_id):
        print unique_id

    def __call__(self):
        self.run()

    def run(self):
        pass
