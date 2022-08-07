import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashJsonResponse, SplashTextResponse
from scrapy.http import HtmlResponse


class SpecialSpider(CrawlSpider):
    count = 0
    name = 'hh'
    allowed_domains = ['ryazan.hh.ru']
    start_urls = ['https://ryazan.hh.ru/search/vacancy?employment=full&experience=noExperience&schedule=remote&search_field=name&text=python&items_on_page=10',
                  'https://ryazan.hh.ru/search/vacancy?employment=full&experience=between1And3&schedule=remote&search_field=name&text=python&items_on_page=10']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="pager"]/a[@class="bloko-button"]'),
            process_request="use_splash",
            follow=True
        ),
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="vacancy-serp-content"]/div/div/div/div/div/div/h3[@class="bloko-header-section-3"]/span[@class="serp-item__name"]/span[@class="g-user-content"]/a[@class="bloko-link"]'),
            callback='parse_item',
            process_request="use_splash"
        )
    )

    def _requests_to_follow(self, response):
        if not isinstance(
                response,
                (HtmlResponse, SplashJsonResponse, SplashTextResponse)):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)

    def use_splash(self, request):
        request.meta.update(splash={
            'args': {
                'wait': 1,
            },
            'endpoint': 'render.html',
        })
        return request

    def parse_item(self, response):
        item = {}
        item['title'] = response.xpath(
            '//h1[@data-qa="vacancy-title"]/text()').get()
        item['salary'] = ' '.join(response.xpath(
            '//div[@class="vacancy-title"]/div/span/text()').getall())
        item['author'] = ' '.join(response.xpath(
            "//span[@class='vacancy-company-name']/a/span[@class='bloko-header-section-2 bloko-header-section-2_lite']/text()").getall())
        author2 = ' '.join(response.xpath(
            "//span[@class='vacancy-company-name']/a/span[@class='bloko-header-section-2 bloko-header-section-2_lite']/span/text()").getall())
        if author2:
            item['author'] = item['author'] + ' ' + author2
        item['experience'] = (response.xpath(
            "//span[@data-qa='vacancy-experience']/text()").get())
        item['type_of_work'] = 'Вид работы: ' + (response.xpath(
            "//p[@data-qa='vacancy-view-employment-mode']/span/text()").get())
        item['content'] = response.xpath(
            "//div[@data-qa='vacancy-description']").get()
        item['url'] = response.url
        self.count += 1
        print('Всего вакансий: ', self.count)
        return item
