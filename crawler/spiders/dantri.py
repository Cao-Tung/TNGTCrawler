import scrapy
from crawler.items import Item

class DantriSpider(scrapy.Spider):
    name = "dantri"
    start_urls = [
        'http://dantri.com.vn/tai-nan-giao-thong.tag',
    ]

    def parse(self, response):
        for tn in response.xpath('//div[@class="mr1"]'):
            src = tn.xpath('h2/a/@href').extract_first()
            src = response.urljoin(src)
            yield scrapy.Request(src, callback=self.parse_src)

        if len(response.xpath('//div[@class="fl"]/a[@class="fon27 mt1 mr2"]').extract()) == 1:
            next_page = response.xpath('//div[@class="fl"]/a[@class="fon27 mt1 mr2"]/@href').extract_first()
            print(next_page)
            if next_page is not None:
                next_page = response.urljoin(next_page)
                print(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
        elif len(response.xpath('//div[@class="fl"]/a[@class="fon27 mt1 mr2"]').extract()) == 2:
            next_page = response.xpath('//div[@class="fl"]/a/@href').extract()
            next = next_page[1]
            print(next)
            if next is not None:
                next = response.urljoin(next)
                print(next)
                yield scrapy.Request(next, callback=self.parse)

    def parse_src(self, response):
        self.item = Item()
        self.item["time"] = response.xpath('//span[@class="fr fon7 mr2 tt-capitalize"]/text()').extract()
        self.item["title"] = response.xpath('//h1[@class="fon31 mgb15"]/text()').extract()
        self.item["description"] = response.xpath('//h2[@class="fon33 mt1 sapo"]/text()').extract()
        content = ""
        for con in response.xpath('//div[@id="divNewsContent"]/p/text()').extract():
                content += con
        self.item["content"] = content
        if content != "":
            yield self.item