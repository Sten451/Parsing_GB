import scrapy


class FirstSpider(scrapy.Spider):
    name = 'first'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/list_basic/']

    def parse(self, response):
        cards = response.xpath(
            '//div[@class="col-lg-4 col-md-6 mb-4"]')
        for card in cards:
            yield{
                'title': card.xpath('.//div[@class="card"]/div[@class="card-body"]/h4/a/text()').get(),
                'price': card.xpath('.//div[@class="card"]/div[@class="card-body"]/h5/text()').get(),
                'description': 'card',
                'image': 'card'
            }
            print(card)
