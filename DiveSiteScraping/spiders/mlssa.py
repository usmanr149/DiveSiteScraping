import re
import scrapy


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
                                  errback = self.errorback)
                                #   meta={'location': dive_clubs_table[i].css('td ::text')[1].get()})

    def parse_club_page(self, response):
        
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

        yield{
            'url': response.url,
            'email': email,
            # 'location': response.meta.get('location')
        }

    def errorback(self, response):
        self.logger.error('DNSLookupError on %s', response.url)

