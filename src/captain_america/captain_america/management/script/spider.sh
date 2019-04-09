#!/bin/bash

SPIDER_DIR="src/spider_man"

cd ${SPIDER_DIR};scrapy crawl $*
