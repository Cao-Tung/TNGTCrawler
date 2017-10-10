import scrapy
from crawler.items import Item

class ZingSpider(scrapy.Spider):
    name = "zing"
    start_urls = [
        'http://news.zing.vn/tai-nan-giao-thong-tin-tuc.html',
    ]

    def parse(self, response):
        for tn in response.xpath('//p[@class="article-title"]'):
            src = tn.xpath('a/@href').extract_first()
            src = response.urljoin(src)
            yield scrapy.Request(src, callback=self.parse_src)

        next_page = response.xpath('//span[@id="mainContent_ContentList3_pager"]/a[@id="mainContent_ContentList3_pager_nextControl"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_src(self, response):
        self.item = Item()
        self.item["time"] = response.xpath('//li[@class="the-article-publish cms-date"]/text()').extract()
        self.item["title"] = response.xpath('//h1[@class="the-article-title cms-title"]/text()').extract()
        self.item["description"] = response.xpath('//p[@class="the-article-summary cms-desc"]/text()').extract()
        content = ""
        for con in response.xpath('//div[@class="the-article-body cms-body"]/p/text()').extract():
                content += con
        self.item["content"] = content
        if content != "":
            yield self.item