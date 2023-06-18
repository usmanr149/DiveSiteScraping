import re

import scrapy
from DiveSiteScraping.items import AquanautDiveClubItems

class DiventuresSpider(scrapy.Spider):
    name = "diventures"
    allowed_domains = ["diventures.com"]
    start_urls = ["https://www.diventures.com/locations/"]

    def parse(self, response):

        club_items = AquanautDiveClubItems()

        numbers = [i for i in range(3, 38, 2)]

        for number in numbers:
            title = ''.join(response.css('.et_pb_section .et_pb_section_{} .et_pb_text_inner h2::text'.format(number)).getall())

            title = title.split('–')

            encodedEmailString = response.css('.et_pb_section .et_pb_section_{} .et_pb_text_inner a'.format(number))[2].attrib['href']

            encodedString = encodedEmailString.split('#')[1]

            r = int(encodedString[:2],16)
            email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])

            phone_number = response.css('.et_pb_section .et_pb_section_3 .et_pb_text_inner a')[1].attrib['href']

            club_items['url'] = response.url
            club_items['tag'] = None
            club_items['date'] = None
            club_items['club_name'] = title[0]
            club_items['building'] = None
            club_items['city'] = title[1]
            club_items['country'] = 'USA'
            club_items['club_url'] = None
            club_items['contact'] = None
            club_items['phone'] = phone_number
            club_items['email'] = email
        
            yield club_items
