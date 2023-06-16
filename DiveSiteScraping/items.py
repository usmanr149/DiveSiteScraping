# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DivesitescrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AquanautDiveClubItems(scrapy.Item):
    url = scrapy.Field()
    tag = scrapy.Field()
    date = scrapy.Field()
    club_name = scrapy.Field()
    building = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    club_url = scrapy.Field()
    contact = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
