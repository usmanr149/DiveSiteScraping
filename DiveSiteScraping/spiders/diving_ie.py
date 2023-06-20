import scrapy
import time
import re

from DiveSiteScraping.items import AquanautDiveClubItems

from selenium import webdriver
from selenium.webdriver.common.by import By

class DivingIeSpider(scrapy.Spider):
    name = "diving_ie"
    allowed_domains = ["diving.ie"]
    start_urls = ["https://diving.ie/clubs-overview/"]

    def parse(self, response):
        
        drop_downs = response.css('.drop__content.js-drop-content')
        locations = response.css('.drop__title h5::text')

        for location, drop_down in zip(locations, drop_downs):

            clubs = drop_down.css('.single-club')

            for club in clubs:
                
                club_items = AquanautDiveClubItems()

                club_name = club.css('h3::text').get()
                urls = club.css('a ::attr(href)').getall()

                club_email = None
                fb_url = None
                phone = None
                club_url = None

                for url in urls:
                    if 'mailto:' in url:
                        club_email = url
                    elif 'www.facebook.com' in url:
                        fb_url = url

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
                    potentials = driver.find_elements(By.CLASS_NAME, "x193iq5w.xeuugli.x13faqbe.x1vvkbs")
                    for idx in range(len(potentials)):
                        if club_email is None:
                            email = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', potentials[idx].text)
                            if len(email) > 0:
                                club_email = email
                        if phone is None and potentials[idx].text == 'Mobile':
                            if idx - 1 > 0:
                                phone = potentials[idx - 1].text
                        if club_url is None and potentials[idx].text == 'Website':
                            if idx - 1 > 0:
                                club_url = potentials[idx - 1].text

                    driver.close()
                    if type(club_email) == list and len(club_email) > 0:
                        club_email = club_email[0]

                club_items['url'] = response.url
                club_items['tag'] = None
                club_items['date'] = None
                club_items['club_name'] = club_name
                club_items['building'] = None
                club_items['city'] = location.get()
                club_items['country'] = 'Ireland'
                club_items['club_url'] = club_url
                club_items['contact'] = None
                club_items['phone'] = phone
                club_items['email'] = club_email

                yield club_items   
