# -*- coding:utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import datetime
import json
import os
import sys
import traceback
import logging
import urlparse
from importlib import import_module

from scrapy.spiders import Spider
from scrapy.http import Request

from spider_man import get_site, get_task, is_exist, TABLE_MAP, batch_video_tag_relation, alter_task_status, \
    alter_attribute, models, get_tag, get_user
from spider_man.items import VideoItem


class Eagle(Spider):
    """User home page spider
    """
    site_id = None  # 站点ID
    parse_type = 'json'  # 解析类型，json or html
    data_list_path = []  # 数据列表路径，["data", "list"]
    data_list_fields_map = {}  # 数据列表字段映射，{"title": ["video_info", "name"]}

    name = ""  # 爬虫名称，默认是模块名与类名组合。eg: spiders_eagle
    headers = {}  # 请求头
    cookies = {}  # 请求COOKIES
    turn_page_fields_map = {}  # 翻页字段映射，{"pages": ["data", "total_page"]}
    full_increment = True  # 全量过后是否变为增量

    def __init__(self, *args, **kwargs):
        super(Eagle, self).__init__(*args, **kwargs)
        self.end_date = datetime.datetime.now()
        self.begin_date = self.end_date - datetime.timedelta(hours=int(kwargs.get('limit', 1)))
        self.restore = int(kwargs.get('restore', 0))
        site = get_site(self.site_id)
        if site:
            self.site = site
        else:
            assert False, ('No site with id %s was found' % self.site_id)

    def get_user_data(self, url):
        # 返回用户数据字典
        # 键为Captain_america的User模型字段
        # third_id字段为强制性
        logging.log(logging.INFO, 'Warning! This "get_user_data" not rewritten')
        return {}

    def gen_crawl_url(self, third_id):
        logging.log(logging.INFO, 'Warning! This "gen_crawl_url" not rewritten')

    def fields_type_transform(self, name, value):  # 字段类型转换
        logging.log(logging.INFO, 'Warning! This "scavenger" not rewritten')

    def scavenger(self, fail_key_list, data):  # 提取失败，回调此方法
        logging.log(logging.INFO, 'Warning! This "scavenger" not rewritten')
        ret_data = {}
        return ret_data

    def jumper(self, meta):  # 翻页函数  Request.meta ==> meta  return ==> Request
        logging.log(logging.INFO, 'Warning! This "jumper" not rewritten')

    def start_requests(self):
        try:
            tasks = get_task(self.site_id)
            logging.log(logging.INFO, 'Found %s task' % len(tasks))
            for task in tasks:
                data = self.get_user_data(task.url)
                url = self.gen_crawl_url(data['third_id'])
                if not url:
                    continue
                req = self.build_request(url, step=1)

                # 将必要数据留存meta
                url_query = urlparse.parse_qs(task.url.split('?')[-1], True)
                channel_name = url_query['cat_name'][0] if url_query.get("cat_name") else ""
                req.meta.update({
                    "task": task,
                    'channel_name': channel_name,
                    "last_url": url,
                    'user': get_user(task, **data)
                })
                yield req
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())



    def handle_extract_fail_key(self, fail_key_list, key):
        logging.log(logging.INFO, 'This key %s extraction failed' % key.capitalize())
        fail_key_list.append(key)

    def parse_html(self, response):  # 响应为html的解析
        item = VideoItem()
        for i in self.data_list_path:
            for j in response.xpath(i):
                # 每条数据处理
                fail_key_list, tag_list = [], []
                for k, v in self.data_list_fields_map.items():
                    is_succeed = False  # 字段提取是否成功
                    for p in v:
                        try:
                            value = unicode(j.xpath(p)[0].extract())
                            result = self.fields_type_transform(k, value)
                            if result:
                                value = result
                            print k, value
                            item[k] = value
                            if value:
                                is_succeed = True
                                break
                        except:
                            continue
                    if not is_succeed:
                        self.handle_extract_fail_key(fail_key_list, k)
                yield item, fail_key_list, tag_list

    def parse_bk(self, response):
        meta = response.meta
        task = meta['task']
        result = None
        if self.parse_type == 'json':
            result = self.parse_json(response)
        elif self.parse_type == 'html':
            result = self.parse_html(response)
        if result:
            for i in result:
                item, fail_key_list, tag_list = i
                if fail_key_list:  # 提取失败的Key交由清道夫
                    logging.log(logging.INFO, "The scavenger has been handed over")
                    scavenger_result = self.scavenger(fail_key_list, i)
                    if scavenger_result:
                        self.scavenger_checks(scavenger_result)
                        item.update(scavenger_result)
                if task.type == 2 and item.get("upload_time"):  # 增全量验证
                    if item.get("upload_time") < self.begin_date:
                        logging.log(logging.INFO, "The incremental crawl with task id %s takes effect" % task.id)
                        self.task_finshed(task)
                        return
                if is_exist(TABLE_MAP.get(u"视频"), self.site, item['third_id']):  # distinct
                    # Finally, verify whether it is repeated
                    continue
                item.update({  # 更新共通
                    "task": meta.get("task"),
                    "site": self.site,
                    'user': meta.get('user')
                })
                yield item  # 交由Pipelines

                if tag_list:  # 批量处理视频标签关联
                    models.VideoTag.objects.bulk_create(
                        [models.VideoTag(video=item.instance, tag=tag) for tag in tag_list])

    def scavenger_checks(self, result):  # 清道夫返回结果检查
        for k, v in result.items():
            if v:
                logging.log(logging.INFO, 'The %s key retries successfully' % k.title())

    def task_finshed(self, task):
        logging.log(logging.INFO, "The crawl with task id %s is complete" % task.id)
        update_fields = {
            'status': 1
        }
        if task.type == 1 and self.full_increment:
            update_fields['type'] = 2
        alter_attribute("Task", [task.id], update_fields)

    def update_headers(self, step):  # 更新请求头  step ==> 步骤
        pass

    def build_request(self, url, step=None):  # 建立请求
        self.update_headers(step)
        req = Request(url=url, headers=self.headers, cookies=self.cookies)
        return req

    def get_member_via_path(self, data, path):  # 嵌套字典查找
        tmp, is_first = None, True
        for i in path:
            if isinstance(i, list):
                try:
                    tmp = self.get_member_via_path(data, i)
                    if tmp:
                        break
                except:
                    continue
            else:
                if is_first:
                    tmp = data.get(i)
                    is_first = False
                else:
                    tmp = tmp.get(i)
        return tmp

    def incremental_check(self, task, item):
        if task.type == 2 and item.get("upload_time"):  # 增量检查
            if item.get("upload_time") < self.begin_date:
                logging.log(logging.INFO, "The incremental crawl with task id %s takes effect" % task.id)
                self.task_finshed(task)
                return True

    def item_check(self, item, meta):
        if not item.get('third_id'):
            return 'continue'
        task = meta.get("task")
        if self.incremental_check(task, item):  # 增量检查
            return 'return'
        if is_exist(TABLE_MAP.get(u"视频"), self.site, item['third_id']):  # distinct
            # Finally, verify whether it is repeated
            return 'continue'
        item.update({  # 更新共通
            "task": task,
            "site": self.site,
            'user': meta.get('user')
        })

    def scavenger_proxy(self, item, data, fail_key_list):
        if not fail_key_list:
            return
        logging.log(logging.INFO, "The scavenger has been handed over")
        scavenger_result = self.scavenger(fail_key_list, data)
        if scavenger_result:
            self.scavenger_checks(scavenger_result)
            item.update(scavenger_result)


class EagleJson(Eagle):
    def parse(self, response):
        meta = response.meta
        task = meta['task']
        resp_data = json.loads(response.text)
        list_data = self.get_member_via_path(resp_data, self.data_list_path)
        if not list_data:  # 无数据，提前退出
            self.task_finshed(task)
            return
        for i in list_data:
            item = VideoItem()
            fail_key_list, tag_list = [], []
            third_id = self.get_member_via_path(i, self.data_list_fields_map['third_id'])
            for k, v in self.data_list_fields_map.items():
                try:
                    value = self.get_member_via_path(i, v)
                    value_transform = self.fields_type_transform(k, value)
                    if value_transform:
                        value = value_transform
                    if k == "tag":  # 标签逻辑，需要在字段类型转换中，将标签值转为列表
                        for tag_name in value:
                            tag_list.append(get_tag(tag_name))
                        continue
                    assert value
                    item[k] = value
                except AssertionError:
                    logging.log(logging.INFO, 'This key %s has a null value' % k.capitalize())
                except Exception, e:
                    self.handle_extract_fail_key(fail_key_list, k)
            self.scavenger_proxy(item, i, fail_key_list)  # 提取失败的Key交由清道夫代理
            result = self.item_check(item, meta)  # Item交由Pipelines之前再处理
            if result == 'return':
                return
            elif result == 'continue':
                continue
            yield item
            # 批量处理视频标签关联
            models.VideoTag.objects.bulk_create([models.VideoTag(video=item.instance, tag=tag) for tag in tag_list])

        for k, v in self.turn_page_fields_map.items():
            meta[k] = self.get_member_via_path(resp_data, v)

        url = self.jumper(meta)  # 翻页函数  Request.meta = meta  return ==> new url
        if url:
            req = self.build_request(url)
            req.meta.update(meta)
            req.meta["last_url"] = url
            yield req
        else:
            self.task_finshed(task)


class EagleHtml(Eagle):
    def parse(self, response):  # 响应为html的解析
        meta = response.meta
        task = meta['task']
        for i in self.data_list_path:
            for j in response.xpath(i):
                # 每条数据处理
                item = VideoItem()
                fail_key_list, tag_list = [], []
                for k, v in self.data_list_fields_map.items():
                    is_succeed = False  # 字段提取是否成功
                    for p in v:
                        try:
                            value = unicode(j.xpath(p)[0].extract())
                            result = self.fields_type_transform(k, value)
                            if result:
                                value = result
                            item[k] = value
                            if value:
                                is_succeed = True
                                break
                        except:
                            continue
                    if not is_succeed:
                        self.handle_extract_fail_key(fail_key_list, k)
                result = self.item_check(item, meta)
                if result == 'return':
                    return
                elif result == 'continue':
                    continue
                yield item


# The end
def handle_spider_name():
    for i in os.listdir(__path__[0]):
        if i.endswith('.py') and i != '__init__.py':
            module_name = i.replace('.py', '')
            module_path = '.'.join([__package__, module_name])
            for k, v in import_module(module_path).__dict__.items():
                if isinstance(v, type):
                    if v.__module__ == module_path:
                        if not v.name:
                            name = '%s_%s' % (module_name, k)
                            v.name = name.lower()


handle_spider_name()
