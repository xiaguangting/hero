# -*- coding:utf-8 -*-
import datetime
import json
import re

import requests
from scrapy.http import Request

from spider_man.items import VideoItem
from spider_man.settings import USER_AGENT_LIST
from spider_man.spiders import Eagle, EagleJson


class Video(EagleJson):
    """
    网易新闻app视频
    """
    site_id = 2

    personal_homepage_url = "https://c.m.163.com/nc/subscribe/list/{0}/video/{1}-{2}.html"
    video_palypage_url = "https://c.m.163.com/nc/video/detail/{0}.html?extraRec=1&skipType=video"
    h5_user_url = "https://c.m.163.com/news/sub/{0}.html?spss=newsapp"
    headers = {
        "User-D": "4hUc8sWTiz+WoudMkYIe/w=="  # 20190403失效解决
    }

    data_list_path = ["tab_list"]
    data_list_fields_map = {
        "third_id": ["videoID"],
        "name": ["title"],
        "cover": ["imgsrc"],
        "duration": ["length"],
        "upload_time": ["mtime"],
    }
    turn_page_fields_map = {

    }

    def get_user_data(self, url):
        result = re.compile("sub/(.*)\.html").findall(url)
        if result:
            third_user_id = result[0]
            headers = self.headers
            headers['User-Agent'] = USER_AGENT_LIST[1]
            resp_data = requests.get(url=self.personal_homepage_url.format(third_user_id, 0, 20), headers=headers).text
            user_data = json.loads(resp_data)['subscribe_info']
            try:
                fans_num = int(user_data['subnum'])
            except:
                fans_num = None
            return {
                'third_id': user_data['ename'],
                'name': user_data['tname'],
                'avatar': user_data['topic_icons'],
                'description': user_data['alias'],
                'fans_num': fans_num
            }

    def gen_crawl_url(self, third_id):
        return self.personal_homepage_url.format(third_id, 0, 20)

    def fields_type_transform(self, name, value):  # 字段类型转换
        if name == "upload_time":  # value ==> timestamp
            return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

    def jumper(self, meta):  # 翻页函数  Request.meta ==> meta  return ==> Request
        last_url = meta['last_url']
        result = re.findall('video/(\d+)-(\d+).html', last_url)
        if result:
            index = int(result[0][0])
            offset = int(result[0][1])
            index += offset
            # https://c.m.163.com/nc/subscribe/list/T1532592501649/video/0-20.html
            return '%s/%s-%s.html' % ('/'.join(last_url.split('/')[:-1]), index, offset)

    def parse(self, response):
        result = super(Video, self).parse(response)
        for i in result:
            if isinstance(i, VideoItem):
                url = self.video_palypage_url.format(i['third_id'])
                req = Request(url=url, callback=self.parse2, headers=self.headers)
                req.meta['item'] = i
                yield req
            else:
                yield i

    def parse2(self, response):
        meta = response.meta
        item = meta.get("item")
        data = json.loads(response.text)
        url = data.get("mp4Hd_url")
        if not url:
            url = data.get("mp4_url")
        item.update({
            'url': url,
            'like_num': data.get("voteCount"),
            'play_num': data.get("playCount")
        })
        yield item
