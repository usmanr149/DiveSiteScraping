import re
import scrapy

from DiveSiteScraping.items import AquanautDiveClubItems

class MlssaSpider(scrapy.Spider):
    name = "mlssa"
    # allowed_domains = ["mlssa.org.au"]
    start_urls = ["http://mlssa.org.au/resources/list-of-dive-shops-and-dive-clubs-in-south-australia/"]

    def parse(self, response):
        dive_clubs_table = response.css('table')[2].css('tr')

        for i in range(1, len(dive_clubs_table)):
            url = dive_clubs_table[i].css('td a::attr(href)')[0].get()

            yield response.follow(url = url, 
                                  callback = self.parse_club_page,
                                  errback = self.errorback,
                                  meta={
                                      'club_name': dive_clubs_table[i].css('td ::text')[0].get(),
                                      'location': dive_clubs_table[i].css('td ::text')[1].get()
                                      })

    def parse_club_page(self, response):

        club_items = AquanautDiveClubItems()
        
        email = None

        text = response.xpath('//text()').getall()
        for t in text:
            email = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', t)
            if len(email) > 0:
                break
        
        if email is None or len(email) == 0:
            for link in response.css('a::attr(href)'):
                email = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', link.get())
                if len(email) > 0:
                    break

        if email is not None:
            if len(email) > 0:
                email = email[0]
            if len(email) == 0:
                email = None

        club_items['url'] = response.url
        club_items['tag'] = None
        club_items['date'] = None
        club_items['club_name'] = response.meta.get('club_name')
        club_items['building'] = None
        club_items['city'] = response.meta.get('location')
        club_items['country'] = 'Australia'
        club_items['club_url'] = response.url
        club_items['contact'] = None
        club_items['phone'] = None
        club_items['email'] = email

        yield club_items

    def errorback(self, failure):
        self.logger.error('DNSLookupError on %s', failure.url)

