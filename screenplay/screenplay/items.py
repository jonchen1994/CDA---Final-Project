# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScreenplayItem(scrapy.Item):
    # define the fields for your item here like:
    Genre = scrapy.Field()
    Film = scrapy.Field()
    F = scrapy.Field()
    D = scrapy.Field()
    S = scrapy.Field()
    B = scrapy.Field()
    A = scrapy.Field()
    
