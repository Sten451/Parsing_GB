import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import HtmlResponse


class SecondSpider(CrawlSpider):
    name = 'second'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/list_basic/']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//nav/ul/li[last()]/a'), follow=True),
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="card"]/div[@class="card-body"]/h4/a'), follow=True, callback='parse_item')
    )

    def parse_item(self, response: HtmlResponse):
        item = {}
        item['title'] = response.xpath(
            '//h3[@class="card-title"]/text()').get()
        item['price'] = response.xpath(
            '//div[@class="card-body"]/h4/text()').get()
        item['description'] = response.xpath(
            '//p[@class="card-text"]/text()').get()
        item['image'] = response.urljoin(response.xpath(
            '//img[@class="card-img-top img-fluid"]/@src').get())
        return item
