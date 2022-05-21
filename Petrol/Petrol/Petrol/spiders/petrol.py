import scrapy
from scrapy_splash import SplashRequest


class PetrolSpider(scrapy.Spider):
    name = 'petrol'
    allowed_domains = ['scrape.world']
    start_urls = ['https://scrape.world/login']

    def parse(self, response):
        token = response.xpath("//input[@name='csrf_token']/@value").get()
        yield scrapy.FormRequest(
            'https://scrape.world/login',
            formdata={
                'csrf_token': token,
                'username': 'admin',
                'password': 'admin'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        yield scrapy.Request('https://scrape.world/season', callback=self.parse2)

    def parse2(self, response):
        trs = response.xpath("//tbody/tr")
        for tr in trs:
            division = tr.xpath(
                ".//td[@colspan='18']/strong/text()").get()
            if division:
                division2 = division
            yield {
                'division': division2,
                'rank': tr.xpath(".//th[@class='right ']/text()").get(),
                'name': tr.xpath(".//td[@data-stat='team_name']/text()").get(),
                'wins': tr.xpath(".//td[@data-stat='wins_avg']/text()").get(),
                'loses': tr.xpath(".//td[@data-stat='losses_avg']/text()").get(),
                'losses_ot_avg': tr.xpath(".//td[@data-stat='losses_ot_avg']/text()").get(),
                'points_avg': tr.xpath(".//td[@data-stat='points_avg']/text()").get(),
            }
