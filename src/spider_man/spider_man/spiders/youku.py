# -*- coding:utf-8 -*-
import datetime
import json
import re
import time

import requests
from lxml import etree
from scrapy.http import Request

from spider_man.items import VideoItem
from spider_man.settings import USER_AGENT_LIST
from spider_man.spiders import Eagle, EagleHtml


class Video(EagleHtml):
    """优酷网页用户主页视频
    """
    site_id = 1
    parse_type = 'html'

    personal_homepage_url = "http://i.youku.com/i/{0}/videos"
    video_palypage_url = "https://c.m.163.com/nc/video/detail/{0}.html?extraRec=1&skipType=video"
    h5_user_url = "https://c.m.163.com/news/sub/{0}.html?spss=newsapp"
    headers = {
        "User-D": "4hUc8sWTiz+WoudMkYIe/w=="  # 20190403失效解决
    }

    data_list_path = ['//div[@class="v va"]']
    data_list_fields_map = {
        "third_id": ['div[@class="v-link"]/a/@href'],
        "name": ['div[@class="v-thumb"]/img/@alt'],
        "cover": ['div[@class="v-thumb"]/img/@src'],
        "duration": ['div[@class="v-link"]/div[@class="v-link-tagrb"]/span[@class="v-time"]/text()'],
        "upload_time": ['div[@class="v-meta"]/div[@class="v-meta-entry"]/span[@class="v-publishtime"]/text()'],
        'url': ['div[@class="v-link"]/a/@href']
    }
    turn_page_fields_map = {

    }

    def get_user_data(self, url):
        result = re.compile("(U.*?)[/?&]").findall(url)
        if result:
            third_user_id = result[0]
            headers = self.headers
            headers['User-Agent'] = USER_AGENT_LIST[1]
            html = etree.HTML(requests.get(url=url, headers=headers).text)
            img_info = html.xpath('//div[@class="head-avatar"]/a/img')[0]
            name = unicode(img_info.xpath('@alt')[0])
            avatar = img_info.xpath('@src')[0]
            description = unicode(html.xpath('//span[@class="desc"]/text()')[0])
            return {
                'third_id': third_user_id,
                'name': name,
                'avatar': avatar,
                'description': description,
            }

    def gen_crawl_url(self, third_id):
        # 通过用户唯一标识符获取其视频列表页url
        # http: // i.youku.com / i / UNTEwMTgyMzY0 / videos / videos, 1
        return self.personal_homepage_url.format(third_id)

    def fields_type_transform(self, name, value):  # 字段类型转换
        if name == 'duration':
            return self.transform_duration(value)
        elif name == 'url':
            if value.startswith('//'):
                return 'https:' + value
        elif name == 'third_id':
            result = re.findall('/id_(.*?)\.h', value)
            if result:
                return result[0]
        elif name == 'upload_time':
            return self.transform_publishtime(value)

    def item_check(self, item, meta):
        super_return = super(Video, self).item_check(item, meta)
        if super_return:
            return super_return
        item['is_parse'] = True  # 优酷视频Url需要进行解析

    def transform_duration(self, duration):
        # 解析播放时长
        result = duration.split(":")
        if len(result) == 2:
            return int(result[0]) * 60 + int(result[1])
        elif len(result) == 3:
            return int(result[0]) * 3600 + int(result[1]) * 60 + int(result[2])

    def transform_publishtime(self, publishtime):
        # 将优酷视频发布时间转换DateTime对象
        year, month, day, hours, minute = [int(i) for i in time.strftime("%Y,%m,%d,%H,%M").split(",")]
        pattern = re.compile("(\d{2})-(\d{2}) (\d{2}):(\d{2})")
        pattern2 = re.compile("(\d{4})-(\d{2})-(\d{2})")
        try:
            if u"分钟前" in publishtime:
                new_minute = int(re.findall("(\d).*", publishtime)[0])
                new_hours = hours
                if new_minute > minute:
                    new_minute = 60 - new_minute - minute
                    new_hours = hours - 1
                else:
                    new_minute = minute - new_minute
                return datetime.datetime(year, month, day, new_hours, new_minute)
            elif u"小时前" in publishtime:
                new_hours = int(re.findall("(\d).*", publishtime)[0])
                new_day = day
                if new_hours > hours:
                    new_hours = 24 - new_hours - hours
                    new_day = day - 1
                else:
                    new_hours = hours - new_hours
                return datetime.datetime(year, month, new_day, new_hours)
            elif u"昨天" in publishtime:
                new_hours, new_minute = publishtime.split(u"昨天")[1].split(":")
                new_day = day - 1
                new_month = month
                if new_day < 1:
                    new_month -= 1
                    if new_month == 2:
                        new_day = 28
                    else:
                        new_day = 30
                return datetime.datetime(year, new_month, new_day, int(new_hours), int(new_minute))
            elif u"前天" in publishtime:
                new_hours, new_minute = publishtime.split(u"前天")[1].split(":")
                new_day = day - 2
                new_month = month
                if new_day < 1:
                    new_month -= 1
                    if new_month == 2:
                        new_day = 27
                    else:
                        new_day = 29
                return datetime.datetime(year, new_month, new_day, int(new_hours), int(new_minute))
            elif u"天前" in publishtime:
                new_day = int(re.findall("(\d).*", publishtime)[0])
                new_month = month
                if new_day > day:
                    new_day = 31 - new_day - day
                    new_month = month - 1
                else:
                    new_day = day - new_day
                return datetime.datetime(year, new_month, new_day)
            else:
                length = len(publishtime)
                if length == 11:  # 11-08 18:00
                    new_month, new_day, new_hours, new_minute = pattern.findall(publishtime)[0]
                    return datetime.datetime(year, int(new_month), int(new_day), int(new_hours), int(new_minute))
                elif length == 10:  # 往年的视频
                    new_year, new_month, new_day = pattern2.findall(publishtime)[0]
                    return datetime.datetime(int(new_year), int(new_month), int(new_day))
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())
            logging.log(logging.INFO, 'Extract error: utime %s' % publishtime)
            return None
