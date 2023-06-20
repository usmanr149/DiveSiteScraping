import scrapy
import pandas as pd
import time
import re

from DiveSiteScraping.items import AquanautDiveClubItems

from selenium import webdriver
from selenium.webdriver.common.by import By


class BsacSpider(scrapy.Spider):
    name = "bsac"
    allowed_domains = ["bsac.com"]
    start_urls = ["https://www.bsac.com/club-life/find-a-bsac-club/search/?searchType=Branch&postcode=&searchDistance=500"]

    def parse(self, response):

        clubs = response.css('.clubs .club ::attr(href)')

        for club in clubs:
            club_url = 'https://www.bsac.com' + club.get()

            yield response.follow(club_url, callback = self.parse_club_page)

        next_page_url = response.css('a[aria-label=Next] ::attr(href)')

        if len(next_page_url) > 0:
            url = 'https://www.bsac.com/club-life/find-a-bsac-club/search/' + next_page_url[0].get()

            yield response.follow(url, callback = self.parse)

    def parse_club_page(self, response):

        club_items = AquanautDiveClubItems()

        club_name = response.css('h1.page-title::text')[0].get()

        tables = pd.read_html(response.url)
        address = tables[0][tables[0][0] == 'Address'][1].iloc[0].split(',')

        building = ','.join(address[:len(address) - 3])
        city = address[-3]
        country = address[-1]
        if 'Contact' in tables[0][0].tolist():
            contact = tables[0][tables[0][0] == 'Contact'][1].iloc[0]
        else:
            contact = None

        if 'Telephone' in tables[0][0].tolist():
            phone = tables[0][tables[0][0] == 'Telephone'][1].iloc[0]
        else:
            phone = None

        try:
            club_url = response.css('a.button::attr(href)')[2].get()
        except:
            club_url = None

        try:
            fb_url = response.css('.club-socialLink::attr(href)')[0].get()
        except:
            fb_url = None

        email = None
        if fb_url:
            fb_url = fb_url.split("?")[0]
            if fb_url.endswith('/'):
                fb_url = fb_url[:-1]
            driver = webdriver.Chrome()

            driver.get(fb_url + "/about")
            time.sleep(4)

            elementLocator = driver.find_elements(By.CLASS_NAME, "x92rtbv")
            if len(elementLocator) > 0:
                elementLocator[0].click()
            time.sleep(2)
            
            idx = 0
            potential_email = driver.find_elements(By.CLASS_NAME, "x193iq5w.xeuugli.x13faqbe.x1vvkbs")
            while idx < len(potential_email):
                email = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', potential_email[idx].text)
                if len(email) > 0:
                    email = email[0]
                    break
                idx+=1
            
            driver.close()
            if email is not None and len(email) == 0:
                email = None

        club_items['url'] = response.url
        club_items['tag'] = None
        club_items['date'] = None
        club_items['club_name'] = club_name
        club_items['building'] = building
        club_items['city'] = city
        club_items['country'] = country
        club_items['club_url'] = club_url
        club_items['contact'] = contact
        club_items['phone'] = phone
        club_items['email'] = email

        yield club_items