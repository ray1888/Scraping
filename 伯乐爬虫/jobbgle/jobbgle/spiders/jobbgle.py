import scrapy
from scrapy import selector
from scrapy.http import Request
from jobbgle.items import JobbgleItem

class Jobb(scrapy.Spider):
    name = "Jobb"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        page = selector.Selector(response)
        lists = page.xpath('//div[@class="grid-8"]/div[@class="post floated-thumb"]')
        urls = lists.xpath('//div[@class="post-meta"]//a[@class="archive-title"]/@href').extract()
        for url in urls:
            yield Request(url=url, headers=self.headers, callback=self.detail)

        next_url = page.xpath('//a[@class="next page-numbers"]/@href').extract()
        for url in next_url:
            if url:
                yield Request(url=url, headers=self.headers)

    def detail(self, response):
        detail_page = selector.Selector(response)
        JBItem = JobbgleItem()
        title = detail_page.xpath('//div[@class="entry-header"]/h1').extract()
        field = detail_page.xpath('//div[@class="entry-meta"]/p/a[1]/text()').extract()
        comment = detail_page.xpath('//div[@class="entry-meta"]/p/a[2]/text()').extract()
        JBItem['title'] = title
        JBItem['field'] = field
        JBItem['comment'] = comment
        yield JBItem