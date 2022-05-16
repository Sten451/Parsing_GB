import scrapy
from scrapy_splash import SplashRequest


class SportSpider(scrapy.Spider):
    name = 'sport'
    allowed_domains = ['scrapingclub.com']
    
    script = '''
        function main(splash, args)
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url='https://scrapingclub.com/exercise/detail_sign/',
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.script
            }
        )

    def parse(self, response):
        item = {}
        item['title'] = response.xpath(
            '//h4[@class="card-title"]/text()').get()
        item['price'] = response.xpath(
            '//h4[@class="card-price"]/text()').get()
        item['description'] = response.xpath(
            '//p[@class="card-description"]/text()').get()
        item['image'] = response.urljoin(response.xpath(
            '//img[@class="card-img-top img-fluid"]/@src').get())
        item['url'] = response.url
        return item
