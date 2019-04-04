# -*- coding: utf-8 -*-
import json
import sys
import time
import urllib

from scrapy.cmdline import execute

# from appcrawler.utils import call_js_method

if __name__ == "__main__":
    execute("scrapy crawl youku_video".split(" "))
