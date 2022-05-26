import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PetrolCountSpider(CrawlSpider):
    name = 'petrol_count'
    allowed_domains = ['www.petrolprices.com']
    start_urls = ['https://www.petrolprices.com/brands/']
    all = 0

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="et_pb_main_blurb_image"]/a'), follow=True, callback='parse_item'),
    )

    def parse_item(self, response):
        item = {}
        item['count'] = response.xpath(
            '//div[contains(@class, "et_pb_module")]/@data-number-value').get()
        item['url'] = response.url
        self.all = self.all + int(item['count'])
        item['all'] = self.all
        return item
