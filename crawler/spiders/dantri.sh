#!/bin/sh
cd /home/caotung/PycharmProjects/Crawler/Crawler/spiders/
PATH=$PATH:/usr/local/bin
export PATH
echo `scrapy crawl dantri -o data.csv -t csv`
