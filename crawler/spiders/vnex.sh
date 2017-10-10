#!/bin/sh
cd /home/caotung/PycharmProjects/TNGTCrawler/crawlerspiders/
PATH=$PATH:/usr/local/bin
export PATH
echo `scrapy crawl vnex -o data.csv -t csv`
