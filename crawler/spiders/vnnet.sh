#!/bin/sh
cd /home/caotung/PycharmProjects/TNGTCrawler/crawlerspiders/
PATH=$PATH:/usr/local/bin
export PATH
echo `scrapy crawl vnnet -o data.csv -t csv`
