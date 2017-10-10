import scrapy
from crawler.items import Item


class VNnetSpider(scrapy.Spider):
    name = "vnnet"
    start_urls = [
        'http://vietnamnet.vn/tai-nan-giao-thong-tag52274.html',
    ]

    def parse(self, response):
        for tn in response.xpath('//li[@class="ArticleCateItem item clearfix dotter"]/h3'):
            src = tn.xpath('a[@class="title f-16 articletype_5"]/@href').extract_first()
            src = response.urljoin(src)
            yield scrapy.Request(src, callback=self.parse_src)

        if len(response.xpath('//a[@id="hBack"]').extract()) == 1:
            next_page = response.xpath('//a[@id="hBack"]/@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                print(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
        elif len(response.xpath('//a[@id="hBack"]').extract()) == 2:
            next_page = response.xpath('//a[@id="hBack"]/@href').extract()
            next = next_page[1]
            print(next)
            if next is not None:
                next = response.urljoin(next)
                print(next)
                yield scrapy.Request(next, callback=self.parse)

    def parse_src(self, response):
        self.item = Item()
        self.item["time"] = response.xpath('//div[@class="ArticleDateTime"]/span[@class="ArticleDate"]/text()').extract()
        self.item["title"] = response.xpath('//div[@class="ArticleDetail"]/h1[@class="title"]/text()').extract()
        self.item["description"] = response.xpath('//div[@id="ArticleContent"]/p/strong/text()').extract()
        content = ""
        for con in response.xpath('//div[@id="ArticleContent"]/p/text()').extract():
                content += con
        self.item["content"] = content
        if content != "":
            yield self.item