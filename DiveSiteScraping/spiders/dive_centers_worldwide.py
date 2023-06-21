import re
import scrapy

import pandas as pd
from DiveSiteScraping.items import AquanautDiveClubItems

class DiveCentersWorldwideSpider(scrapy.Spider):
    name = "dive_centers_worldwide"
    allowed_domains = ["www.dive-centers.net"]
    start_urls = ["http://www.dive-centers.net/dive_clubs_worldwide.html"]

    def parse(self, response):
        
        table_of_interest = response.css('table')[6].css('tr')

        for i in range(len(table_of_interest) - 1):
            url = table_of_interest[i].css('td')[0].css('td ::attr(href)').get()

            if url is not None:
                country = table_of_interest[2].css('td')[0].css('td ::text').get()

                country_url = 'http://www.dive-centers.net' + url

                yield response.follow(country_url, self.parse_country_page)

    def parse_country_page(self, response):

        htmls = response.css('table')[10].css('tr ::attr(href)').getall()

        for i in range(len(htmls)):
            url = 'http://www.dive-centers.net' + htmls[i]

            yield response.follow(url, self.parse_dive_club_page)

    def parse_dive_club_page(self, response):

        club_items = AquanautDiveClubItems()

        tables = pd.read_html(response.url)

        for idx in range(3, len(tables)):
            if len(tables[idx]) > 5:
                break

        if idx == len(tables) - 1:
            yield club_items

        else:
            country_row = [row for row in tables[idx][0] if 'Country' in str(row)]
            if len(country_row) > 0:
                country = tables[idx][tables[idx][0] == country_row[0]][1].iloc[0]
            else:
                country = None

            city_row = [row for row in tables[idx][0] if 'Region' in str(row)]
            if len(city_row) > 0:
                city = tables[idx][tables[idx][0] == city_row[0]][1].iloc[0]
            else:
                city = None
            
            phone_number_row = [row for row in tables[idx][0] if 'phone' in str(row)]
            if len(phone_number_row) > 0:
                phone_number = tables[idx][tables[idx][0] == phone_number_row[0]][1].iloc[0]
            else:
                phone_number = None

            text = response.xpath('//text()').getall()
            text = ' '.join(text)
            email = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
            email = None if len(email) == 0 else ','.join(email)

            club_url = None
            club_urls = response.css('td .a a::text').getall()

            for club_url in club_urls:
                if 'www.' in club_url:
                    break

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

        # response.css('table')[6].css('tr')[40].get()


    # response.css('table')[6].css('tr')[2].get()

    # response.css('table')[10].css('tr').getall()
