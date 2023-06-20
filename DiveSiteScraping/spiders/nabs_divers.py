import re
import scrapy

from DiveSiteScraping.items import AquanautDiveClubItems

class NabsDiversSpider(scrapy.Spider):
    name = "nabs_divers"
    allowed_domains = ["nabsdivers.org"]
    start_urls = ["https://nabsdivers.org/regional-clubs/"]

    def parse(self, response):
        urls = response.css('.sub-menu')[1].css('a::attr(href)').getall()

        # urls = ['https://nabsdivers.org/northeast-region/']

        for url in urls:
            yield response.follow(url, callback = self.parse_region_page)
            
    def parse_region_page(self, response):

        club_items = AquanautDiveClubItems()

        club_details = {
            'https://nabsdivers.org/northeast-region/': [
                {
                    'club_name': 'Underwater Adventure Seekers (UAS)',
                    'city': 'Washington, DC',
                    'contact': 'Kim Walker',
                    'email': 'presidentuas1959@gmail.com',
                    'club_url': 'https://uasdivers.org/',
                    'country': 'USA'
                },
                {
                    'club_name': 'Atlantic Rangers Scuba Club (ATRA)',
                    'city': 'Philadelphia',
                    'contact': 'Claude Knowles',
                    'email': None,
                    'club_url': 'http://atlanticrangerssc.org/',
                    'country': 'USA'
                },
                {
                    'club_name': 'Aquatic Voyagers Scuba Club of New York (AVSC)',
                    'city': 'New York',
                    'contact': 'Norman Berhannan',
                    'email': 'Scubadiving18@optonline.net',
                    'club_url': 'http://www.avscdivers.org/',
                    'country': 'USA'
                },
                {
                    'club_name': 'Charm City Scuba',
                    'city': 'Baltimore, Maryland',
                    'contact': 'Dwayne Johnson',
                    'email': 'president@charmcityscuba.org',
                    'club_url': None,
                    'country': 'USA'
                }
            ],
            'https://nabsdivers.org/midwest-region/': [
                {
                    'club_name': 'Michigan African America Scuba Klub (MASK)',
                    'city': None,
                    'contact': 'Jim Albritton',
                    'email': 'mask@nabsdivers.org',
                    'club_url': None,
                    'country': 'USA'
                },
                {
                    'club_name': 'New Depth Dive Association (NDDA)',
                    'city': None,
                    'contact': 'Allyson Fisher',
                    'email': 'newdepthdiveindy@gmail.com',
                    'club_url': 'https://www.newdepthdiveindy.com/',
                    'country': 'USA'
                },
                {
                    'club_name': 'Windy City Seals Scuba Club',
                    'city': None,
                    'contact': 'Marvin E. Martin, Sr.',
                    'email': None,
                    'club_url': 'https://windycityseals.com/',
                    'country': 'USA'
                }
            ],
            'https://nabsdivers.org/southern-clubs/': [
                {
                    'club_name': 'Atlanta Underwater Explorers (AUE)',
                    'city': 'Atlanta, Georgia',
                    'contact': 'Chris Seales,Voncile Hodges',
                    'email': 'bahamagus1@yahoo.com,diveaueinfo@gmail.com',
                    'club_url': 'http://www.diveaue.org/',
                    'country': 'USA'
                },
                {
                    'club_name': 'Southern SeaQuestrians (SSQ)',
                    'city': 'Atlanta, Georgia',
                    'contact': 'Courtlandt Butts',
                    'email': 'manta@lifeguardian.com',
                    'club_url': 'https://www.ssquest.com/',
                    'country': 'USA'
                },
                {
                    'club_name': 'DIVERSe Orlando',
                    'city': 'Orlando, Florida',
                    'contact': 'Erik Denson',
                    'email': 'edenson@cfl.rr.com',
                    'club_url': 'http://diverseorlando.org/',
                    'country': 'USA'
                },
                {
                    'club_name': 'Nubian Dive Club',
                    'city': 'Houston, Texas',
                    'contact': 'Claude A. Lewis III',
                    'email': 'president@nubiandiveclub.org',
                    'club_url': 'https://www.nubiandiveclub.org/',
                    'country': 'USA'
                },
                {
                    'club_name': 'Black Coral Divers (BCD)',
                    'city': 'Dallas, Texas',
                    'contact': 'Chris Powell',
                    'email': 'Christopherpowell@ymail.com',
                    'club_url': 'http://blackcoraldivers.org/',
                    'country': 'USA'
                },
                {
                    'club_name': 'Unicorns of Diving',
                    'city': 'Tampa, Florida',
                    'contact': 'Justin Lovett',
                    'email': 'unicornsofdiving@gmail.com',
                    'club_url': 'http://unicornsofdiving.com/',
                    'country': 'USA'
                }
            ],
            'https://nabsdivers.org/western-club/': [
                {
                    'club_name': 'Los Angeles Black Underwater Explorers (LABUE)',
                    'city': 'Los Angeles, California',
                    'contact': 'Richard Rice',
                    'email': 'ricere2004@yahoo.com',
                    'club_url': 'http://labue.org/',
                    'country': 'USA'
                }
            ],
            'https://nabsdivers.org/international-club/': [
                {
                    'club_name': 'Bitonga Divers',
                    'city': None,
                    'contact': 'Tim Dykman',
                    'email': 'tdykman@oceanrevolution.org',
                    'club_url': None,
                    'country': 'Mozambique'
                }
            ]
        }

        clubs = club_details[response.url]

        for club in clubs:
            club_items['url'] = response.url
            club_items['tag'] = None
            club_items['date'] = None
            club_items['club_name'] = club.get('club_name')
            club_items['building'] = None
            club_items['city'] = club.get('location')
            club_items['country'] = club.get('country')
            club_items['club_url'] = club.get('club_url')
            club_items['contact'] = club.get('contact')
            club_items['phone'] = None
            club_items['email'] = club.get('email')

            yield club_items

        # for https://nabsdivers.org/northeast-region/
        # response.css('.wpb_wrapper')[1].css('p ::text').get()
        # response.css('.wpb_wrapper')[5].css('p::text').get()

        # response.css('.wpb_wrapper')[9].css('p ::text').get()
        # response.css('.wpb_wrapper')[13].css('p::text').getall()

        # response.css('.wpb_wrapper')[16].css('p ::text').get()
        # response.css('.wpb_wrapper')[18].css('p a::attr(href)').getall()

        # response.css('.wpb_wrapper')[24].css('p ::text').get()
        # response.css('.wpb_wrapper')[26].css('p')


