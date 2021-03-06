import scrapy
from crawler.items import Item

class VNexSpider(scrapy.Spider):
    name = "vnex"
    start_urls = [
        'https://vnexpress.net/tai-nan-giao-thong/tag-20607-1.html',
    ]

    def parse(self, response):
        for tn in response.xpath('//h3[@class="title_news"]'):
            src = tn.xpath('a/@href').extract_first()
            src = response.urljoin(src)
            yield scrapy.Request(src, callback=self.parse_src)

        next_page = response.xpath('//div[@id="pagination"]/a[@class="next"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_src(self, response):
        self.item = Item()
        content = ""
        for con in response.xpath('//p[@class="Normal"]/text()').extract():
            if "video" in con or "Video" in con or con == "\n":
                content = content
            else:
                content += con
        self.item["content"] = content
        self.item["description"] = response.xpath('//h2[@class="description"]/text()').extract()
        self.item["title"] = response.xpath('//h1[@class="title_news_detail mb10"]/text()').extract()
        if content != "":
            yield self.item