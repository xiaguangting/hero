#!/bin/bash

nohup scrapy crawl $* >/dev/null 2>&1 &
