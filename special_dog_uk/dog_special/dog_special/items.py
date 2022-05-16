# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DogSpecialItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    description = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()
    town = scrapy.Field()
