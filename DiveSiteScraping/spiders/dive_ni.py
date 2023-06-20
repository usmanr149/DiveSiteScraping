import scrapy
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

class DiveNiSpider(scrapy.Spider):
    name = "dive_ni"
    allowed_domains = ["www.dive-ni.com"]
    start_urls = ["https://www.dive-ni.com/dive-clubs/"]

    def parse(self, response):
        driver = webdriver.Chrome()

        driver.get(response.url)

        time.sleep(4)

        club_boxes = driver.find_elements(By.CLASS_NAME, "fc-item-box")

        club_name = None
        city = None
        country = 'Northern Ireland'
        phone = None
        email = None
        club_url = None

        for box in club_boxes:
            club_name = box.find_elements(By.CSS_SELECTOR, ".wpomp_location_title a")[0].text
            city = box.find_elements(By.CLASS_NAME, "marker_address")[0].text
            phone = box.find_elements(By.CLASS_NAME, "clubs_phone")[0].text
            email = box.find_elements(By.CLASS_NAME, "clubs_email")[0].text
            club_url = box.find_elements(By.CSS_SELECTOR, ".clubs_link a")[0].get_attribute('href')

            yield{
                'club_name': club_name,
                'country': country,
                'city': city,
                'phone': phone,
                'email': email,
                'club_url': club_url
            }

