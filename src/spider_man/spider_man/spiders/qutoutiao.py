# -*- coding:utf-8 -*-
import datetime
import json
import logging
import re
import sys
import time

import requests

from spider_man import get_tag, get_user
from spider_man.settings import USER_AGENT_LIST
from spider_man.spiders import Eagle, EagleJson


class Video(EagleJson):
    site_id = 1

    # h5页面所访问接口，DATE: 20190320
    # {0} ==> 用户ID  {1} ==> 页码  {2} ==> 时间戳（毫秒）
    user_video_list_url = "http://api.1sapp.com/wemedia/content/videoList?token=&dtu=200&version=0&os=android&id={0}&page={1}&_={2}"
    # https://mpapi.qutoutiao.net/video/getAddressByFileId?file_id=205ecaa6ae9568d94c92a336e91cbc88&token=&dtu=200&r=3861774036496166&o=4&s=124302064&_=1553136160521
    get_address_by_file_id_url = "https://mpapi.qutoutiao.net/video/getAddressByFileId?file_id={0}"
    user_info_url = 'http://api.1sapp.com/wemedia/author/memberInfo?token=&dtu=200&version=0&os=android&id={0}&_={1}'
    headers = {
        "Host": "api.1sapp.com",
        "Connection": "keep-alive",
        "Accept": "application/json",
        "Origin": "http://h5ssl3.1sapp.com",
        "User-Agent": USER_AGENT_LIST[1],
        "Referer": "http://h5ssl3.1sapp.com/qukan_new2/dest/zmt_home/read/zmt_home/index.html?id={0}",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    data_list_path = ["data", "list"]
    data_list_fields_map = {
        "third_id": ["id"],
        "name": ["title"],
        "cover": ["cover"],
        "url": ["video_info", "hd", "url"],
        "duration": ["video_info", "duration"],
        "tag": ["tag"],
        "upload_time": ["show_time"],
    }
    turn_page_fields_map = {
        "total_page": ["data", "total_page"],
        "page": ["data", "page"]
    }

    def get_user_data(self, url):
        pattern = re.compile(".*\?id=(\d*)")
        result = pattern.findall(url)
        if result:
            self.third_id_user_id = result[0]
            user_info_url = self.user_info_url.format(result[0], int(time.time() * 1000))
            resp_data = json.loads(requests.get(url=user_info_url).text)
            data = resp_data['data']
            return {
                'third_id': data['author_id'],
                'name': data['nickname'],
                'avatar': data['avatar'],
                'description': data['description'],
                'fans_num': data['follow_num']
            }

    def gen_crawl_url(self, third_id):
        # url ==> http://h5ssl3.1sapp.com/qukan_new2/dest/zmt_home/read/zmt_home/index.html?id=1445683
        return self.user_video_list_url.format(third_id, 1, int(time.time() * 1000))

    def jumper(self, meta):
        # last_page = int(re.findall("&page=(\d*)&", last_url)[0])
        last_url = meta.get("last_url")
        last_page = meta.get("page")
        if last_page < meta.get("total_page"):
            page = last_page + 1
            return re.sub("&_=\d*", "&_=%s" % int(time.time() * 1000), re.sub("&page=\d*", "&page=%s" % page, last_url))

    def scavenger(self, fail_key_list, data):  # data_list_fields_map提取失败，统一进入这个方法
        ret_data = {}
        if "duration" in fail_key_list or "url" in fail_key_list:
            video_value = data.get("video_value")
            resp_data = json.loads(requests.get(url=self.get_address_by_file_id_url.format(video_value)).text)
            duration = resp_data["data"]["duration"]
            url = resp_data["data"]["hd"]["url"]
            ret_data["url"] = url
            ret_data["duration"] = duration
        return ret_data

    def update_headers(self, step):
        if step == 1:
            self.headers["Referer"] = self.headers["Referer"].format(self.third_id_user_id)

    def fields_type_transform(self, name, value):  # 字段类型转换
        if name == "cover":  # value ==> list
            return value[0]
        elif name == "tag":  # value ==> list
            return value
        elif name == "upload_time":  # value ==> timestamp
            return datetime.datetime.fromtimestamp(value)
