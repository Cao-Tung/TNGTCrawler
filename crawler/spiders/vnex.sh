#!/bin/sh
cd /home/caotung/PycharmProjects/Crawler/Crawler/spiders/
PATH=$PATH:/usr/local/bin
export PATH
echo `scrapy crawl vnex -o data.csv -t csv`
