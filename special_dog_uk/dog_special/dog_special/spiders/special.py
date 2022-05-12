import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SpecialSpider(CrawlSpider):
    name = 'special'
    allowed_domains = ['directory.independent.co.uk']
    start_urls = ['https://directory.independent.co.uk/dog-grooming/in/uk']

    rules = (
        Rule(LinkExtractor(
             restrict_xpaths='//ul[@class="em-pagination pagination"]/li[last()]/a'), follow=True),
        Rule(LinkExtractor(
            restrict_xpaths='//h2[@class="result-title"]/a'), follow=True, callback='parse_item')
    )

    def parse_item(self, response):
        item = {}
        item['name'] = response.xpath(
            '//h2[@class="profile-heading"]/text()').get()
        item['description'] = response.xpath(
            '//p[@class="profile-category"]/text()').get()
        item['address'] = response.xpath(
            '//p[@class="profile-address"]/text()').getall()
        item['phone'] = response.xpath(
            '//div[@class="profile-numbers"]/p[contains(@class, "profile-number")]/a[last()]/@link_number').get()
        item['url'] = response.url
        return item
