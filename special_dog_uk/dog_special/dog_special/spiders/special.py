import csv
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SpecialSpider(CrawlSpider):
    name = 'special'
    allowed_domains = ['directory.independent.co.uk']
    start_urls = []

    with open("Towns_List.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'Town':
                continue
            temp_url = row[0].replace(' ', '-')
            start_urls.append(
                'https://directory.independent.co.uk/dog-grooming/in/' + temp_url.lower())
        print(start_urls)

    #start_urls = ['https://directory.independent.co.uk/dog-grooming/in/uk']

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
        item['phone'] = (response.xpath(
            "//p[@class='profile-number ']/a/@link_number").get())
        item['url'] = response.url
        item['town'] = response.request.headers.get('Referer')
        return item
