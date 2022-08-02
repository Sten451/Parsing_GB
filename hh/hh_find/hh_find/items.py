# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HhFindItem(scrapy.Item):
    title = scrapy.Field()
    salary = scrapy.Field()
    author = scrapy.Field()
    experience = scrapy.Field()
    href = scrapy.Field()
    type_of_work = scrapy.Field()
    content = scrapy.Field()
    data = scrapy.Field()
