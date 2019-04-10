#!/bin/bash

nohup scrapy crawl $* >/var/log/hero/spider-man/tmp.log
