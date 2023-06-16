import scrapy
from DiveSiteScraping.items import AquanautDiveClubItems

class AquanautSpider(scrapy.Spider):
    name = "aquanaut"
    allowed_domains = ["aquanaut.com"]
    start_urls = ["https://aquanaut.com/clubs/"]

    def parse(self, response):
        refs = response.css('dd a ::attr(href)')

        for ref in refs:
            relative_url = 'https://aquanaut.com/' + ref.get() 
            yield response.follow(relative_url, callback = self.parse_club_page)

    def parse_club_page(self, response):
        table_lines = response.css('dd ::text')

        club_items = AquanautDiveClubItems()

        url = None
        tag = None
        date = None
        club_name = None
        building = None
        city = None
        country = None
        club_url = None
        contact = None
        phone = None
        email = None

        for line in table_lines:
            row = line.get()
            if row.split(':')[0] == 'Tag':
                tag = row
            elif row.split(':')[0] == 'Date':
                date = row
            elif row.split(':')[0] == 'Club Name':
                club_name = row
            elif row.split(':')[0] == 'Building':
                building = row
            elif row.split(':')[0] == 'City':
                city = row
            elif row.split(':')[0] == 'Country':
                country = row
            elif row.split(':')[0] == 'URL':
                club_url = response.css('a[href^=http]').attrib['href']
            elif row.split(':')[0] == 'Contact':
                contact = row
            elif row.split(':')[0] == 'Phone':
                phone = row
            elif row.split(':')[0] == 'Email':
                email = response.css('a[href^=mailto]').attrib['href']

        club_items['url'] = response.url
        club_items['tag'] = tag
        club_items['date'] = date
        club_items['club_name'] = club_name
        club_items['building'] = building
        club_items['city'] = city
        club_items['country'] = country
        club_items['club_url'] = club_url
        club_items['contact'] = contact
        club_items['phone'] = phone
        club_items['email'] = email

        yield club_items