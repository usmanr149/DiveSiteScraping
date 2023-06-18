import scrapy
import pandas as pd
import re

from DiveSiteScraping.items import AquanautDiveClubItems

class DiveClubsGermanySpider(scrapy.Spider):
    name = "dive_clubs_germany"
    allowed_domains = ["dive-centers.net"]
    start_urls = ["http://dive-centers.net/dive_clubs-germany-20.html"]

    def parse(self, response):
        
        htmls = response.css('table .a')

        for i in range(19, 30):
            url = 'http://www.dive-centers.net' + htmls[i].css('a').attrib['href']

            yield response.follow(url, self.parse_dive_club_page)

    def parse_dive_club_page(self, response):

        club_items = AquanautDiveClubItems()

        tables = pd.read_html(response.url)

        country = tables[6][tables[6][0] == 'Country:'][1][0]
        city = tables[6][tables[6][0] == 'Region:'][1].iloc[0]
        phone_number_row = [row for row in tables[6][0] if 'phone' in str(row)]
        if len(phone_number_row) > 0:
            phone_number = tables[6][tables[6][0] == phone_number_row[0]][1].iloc[0]
        else:
            phone_number = None

        text = response.xpath('tr//text()').getall()
        text = ' '.join(text)
        email = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
        email = None if len(email) == 0 else email

        club_url = response.css('td .a a::text')[2].get()

        if 'www.' not in club_url:
            try:
                club_url = response.css('td .a a::text')[3].get()
            except:
                pass

        club_items['url'] = response.url
        club_items['tag'] = None
        club_items['date'] = None
        club_items['club_name'] = response.css('h2::text')[0].get()
        club_items['building'] = None
        club_items['city'] = city
        club_items['country'] = country
        club_items['club_url'] = club_url
        club_items['contact'] = None
        club_items['phone'] = phone_number
        club_items['email'] = email

        yield club_items
