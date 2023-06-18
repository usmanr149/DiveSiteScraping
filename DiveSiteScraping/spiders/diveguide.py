import re

import scrapy
from DiveSiteScraping.items import AquanautDiveClubItems

class DiveguideSpider(scrapy.Spider):
    name = "diveguide"
    allowed_domains = ["diveguide.com"]
    start_urls = ["https://diveguide.com/clubs.htm"]

    def parse(self, response):

        club_items = AquanautDiveClubItems()

        p_tags = response.xpath("//p")

        phone_regex_1 = re.compile(r'Phone:\s*(?<!\d)\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', re.IGNORECASE)
        phone_regex_2 = re.compile(r'(?<!\d)\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', re.IGNORECASE)
        postal_code_regex = re.compile(r'[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d')
        city_regex = re.compile(r'([A-Z][a-z]+\s?)+,\s[A-Z]{2}')
        city_regex = re.compile(r'\b[a-zA-Z\s]+(?=,|\n)')

        for p in p_tags:
            if len(p.css('a[href^=mailto]')) > 0:

                if re.search(postal_code_regex, p.get()):
                    country = 'Canada'
                elif 'Indonesia' in  p.get():
                    country = 'Indonesia'
                elif 'Nicaragua' in p.get():
                    country = 'Nicaragua'
                elif 'Venezuela' in p.get():
                    country = 'Venezuela'
                else:
                    country = 'USA'

                phone_number = re.findall(phone_regex_1, p.get())

                if len(phone_number) == 0:
                    phone_number = re.findall(phone_regex_2, p.get())
                
                if len(phone_number) > 0:
                    phone_number = phone_number[0]

                city = p.css('p b::text').get()
                city = city if city is not None else re.search(city_regex, p.get()).group()

                club_name = p.css('p::text')[1].get()
                if club_name:
                    club_name = club_name.strip()

                club_items['url'] = response.url
                club_items['tag'] = None
                club_items['date'] = None
                club_items['club_name'] = club_name
                club_items['building'] = None
                club_items['city'] = city
                club_items['country'] = country
                club_items['club_url'] = None
                club_items['contact'] = None
                club_items['phone'] = phone_number
                club_items['email'] = p.css('a[href^=mailto]').attrib['href']
            
                yield club_items

        club_items['url'] = response.url
        club_items['tag'] = None
        club_items['date'] = None
        club_items['club_name'] = 'Scuba Guengo'
        club_items['building'] = None
        club_items['city'] = 'Cabo San Lucas'
        club_items['country'] = 'Mexico'
        club_items['club_url'] = None
        club_items['contact'] = None
        club_items['phone'] = None
        club_items['email'] = 'scubaguengo@scubadiving.com'
    
        yield club_items

        yield response.follow(response.url, callback = self.parse_left_overs)

    def parse_left_overs(self, response):

        club_items = AquanautDiveClubItems()

        h3s = response.xpath('//h3/text()').getall()

        text = response.xpath('//text()').getall()
        cleaned_text = [t.strip() for t in text if t.strip()]

        phone_regex_1 = re.compile(r'Phone:\s*(?<!\d)\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', re.IGNORECASE)
        phone_regex_2 = re.compile(r'(?<!\d)\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', re.IGNORECASE)
        postal_code_regex = re.compile(r'[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d')
        city_regex = re.compile(r'([A-Z][a-z]+\s?)+,\s[A-Z]{2}')

        for h3 in h3s:
            for i in range(len(cleaned_text)):
                if cleaned_text[i] == h3:

                    text = '\n'.join(cleaned_text[i:i+10])

                    if re.search(postal_code_regex, text):
                        country = 'Canada'
                    elif 'Indonesia' in  text:
                        country = 'Indonesia'
                    elif 'Nicaragua' in text:
                        country = 'Nicaragua'
                    elif 'Venezuela' in text:
                        country = 'Venezuela'
                    else:
                        country = 'USA'

                    phone_number = re.findall(phone_regex_1, text)

                    if len(phone_number) == 0:
                        phone_number = re.findall(phone_regex_2, text)
                    
                    if len(phone_number) > 0:
                        phone_number = phone_number[0]

                    city = re.search(city_regex, text).group()

                    club_name = cleaned_text[i + 1]

                    email = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
                    email = None if len(email) == 0 else ','.join(email)

                    club_items['url'] = response.url
                    club_items['tag'] = None
                    club_items['date'] = None
                    club_items['club_name'] = club_name
                    club_items['building'] = None
                    club_items['city'] = city
                    club_items['country'] = country
                    club_items['club_url'] = None
                    club_items['contact'] = None
                    club_items['phone'] = phone_number
                    club_items['email'] = email
                
                    yield club_items
