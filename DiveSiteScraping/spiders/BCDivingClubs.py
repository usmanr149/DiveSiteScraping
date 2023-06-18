import scrapy
from DiveSiteScraping.items import AquanautDiveClubItems

class BcdivingclubsSpider(scrapy.Spider):
    name = "BCDivingClubs"
    allowed_domains = ["bcdiving.ca"]
    start_urls = ["https://bcdiving.ca/club-resources/provincial-clubs/"]

    def parse(self, response):

        club_items = AquanautDiveClubItems()
        
        for i in range(1, 7):
            table_line = response.css('tr')[i]
            club_items['url'] = response.url
            club_items['tag'] = None
            club_items['date'] = None
            club_items['club_name'] = table_line.xpath('td[1]//text()').extract_first()
            club_items['building'] = None
            club_items['city'] = table_line.xpath('td[2]//text()').extract_first()
            club_items['country'] = 'Canada'
            club_items['club_url'] = table_line.xpath('td[4]//@href').extract_first()
            club_items['contact'] = None
            club_items['phone'] = None
            club_items['email'] = table_line.xpath('td[3]//@href').extract_first()
            
            yield club_items
