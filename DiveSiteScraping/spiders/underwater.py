# this website only has 4 diveclubs
import scrapy

from DiveSiteScraping.items import AquanautDiveClubItems

class UnderweaterSpider(scrapy.Spider):
    name = "underwater"
    # allowed_domains = ["underwater.com.au"]
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"] 
    # "https://underwater.com.au/dive_clubs/"]

    def parse(self, response):
        
        club_items = AquanautDiveClubItems()

        club_names = ['Black Rock Underwater Diving Group',
                      'Underwater Explorers Club of W.A.',
                      'Mildura Desert Divers Club Inc.',
                      'Murdoch University Divers Club']
        emails = ['president@brudg.org.au',
                  'membership@uecwa.com.au',
                  'milduradesertdivers@gmail.com',
                  None]
        cities = ['Victoria', 'City of Cockburn', 'Victoria', 'Perth']
        countries = ['Australia', 'Australia', 'Australia', 'Australia']
        contacts = [None, 
                    'Mike Buchanan',
                    'Grant Brown',
                    'The Secretary']
        buildings = ['The Swan Hotel, 425 Church st', 
                     'Underwater Explorers Club of W.A. (Inc.) Port Coogee Marina',
                     'Mildura Airport',
                     'Murdoch University School of Veterinary and Life Sciences 90 South Street Murdoch'
                     ]
        club_urls = ['http://www.brudg.org.au/',
                     'https://www.uecwa.com.au/',
                     None,
                     'https://www.mud.org.au/']
        phones = [None, '+61457825074', '0408034964', '08 9360 6387']



        for i in range(4):
            club_items['url'] = "https://underwater.com.au/dive_clubs/"
            club_items['tag'] = None
            club_items['date'] = None
            club_items['club_name'] = club_names[i]
            club_items['building'] = buildings[i]
            club_items['city'] = cities[i]
            club_items['country'] = countries[i]
            club_items['club_url'] = club_urls[i]
            club_items['contact'] = contacts[i]
            club_items['phone'] = phones[i]
            club_items['email'] = emails[i]

            yield club_items
