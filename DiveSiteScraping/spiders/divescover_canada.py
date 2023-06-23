import scrapy
import time
import re

import urllib.parse

from selenium import webdriver
from selenium.webdriver.common.by import By

from DiveSiteScraping.items import AquanautDiveClubItems
from DiveSiteScraping.helpers import scrape_facebook_about_page

class DivescoverCanadaSpider(scrapy.Spider):
    name = "divescover_canada"
    allowed_domains = ["divescover.com"]
    start_urls = ["https://divescover.com/dive-centers/canada"]

    def parse(self, response):

        # scrape current page
        club_titles = response.css('.item-title')

        for title in club_titles:
            club_items = AquanautDiveClubItems()
            text = title.css('h2 ::text').getall()

            club_title = text[0]

            fb_url = None

            text = [t.strip() for t in text]
            text = ' '.join(text).strip()

            driver = webdriver.Chrome()

            query = 'https://www.google.com/search?q=' + urllib.parse.quote(text + ' Facebook')

            driver.get(query)

            time.sleep(2)

            first_hit = driver.find_elements(By.CSS_SELECTOR, '.yuRUbf a')[0].get_attribute('href')
            club_email, phone, club_url = None, None, None
            if 'www.facebook.com' in first_hit:
                fb_url = first_hit + 'about'
                driver.get( fb_url )

                time.sleep(2)

                club_email, phone, club_url = scrape_facebook_about_page(driver)

            driver.close()
            if type(club_email) == list and len(club_email) > 0:
                club_email = club_email[0]

            club_items['url'] = response.url
            club_items['tag'] = None
            club_items['date'] = None
            club_items['club_name'] = club_title
            club_items['building'] = None
            club_items['city'] = None
            club_items['country'] = 'Canada'
            club_items['club_url'] = club_url
            club_items['contact'] = None
            club_items['phone'] = phone
            club_items['email'] = club_email

            yield club_items
        
        # go to next page if it exists
        if response.css('.pagination a')[-1].css('a ::text').get() == 'Next':
            next_page = response.css('.pagination a')[-1].css('a ::attr(href)').get()

            url = 'https://divescover.com/dive-centers/canada' + next_page

            yield response.follow(url, self.parse)

