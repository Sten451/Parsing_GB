from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scrapingclub.spiders.second import SecondSpider
from scrapingclub import settings


if __name__ == "__main__":
    crawler_setting = Settings()
    crawler_setting.setmodule(settings)

    process = CrawlerProcess(settings=crawler_setting)
    process.crawl(SecondSpider)
    process.start()
