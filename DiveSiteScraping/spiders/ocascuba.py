import scrapy
from DiveSiteScraping.items import AquanautDiveClubItems

class OcascubaSpider(scrapy.Spider):
    name = "ocascuba"
    allowed_domains = ["www.ocascuba.org"]
    start_urls = ["http://www.ocascuba.org/links_dive_other.php"]

    def parse(self, response):

        club_items = AquanautDiveClubItems()

        clubs = {
            'MetroWest Dive Club': {
                'club_name': 'MetroWest Dive Club',
                'city': 'Framingham',
                'contact': 'Jack Sargentn,Frances Antonelli,Bill Borek',
                'email': 'president@mwdc.org,vicepresident@mwdc.org,treasurer@mwdc.org',
                'club_url': 'http://www.mwdc.org/index.html',
                'country': 'USA'
            },
            'New England Aquarium Dive Club': {
                'club_name': 'New England Aquarium Dive Club',
                'city': 'Boston, MA',
                'contact': 'Uma Mirani,Greg Hunter',
                'email': 'president@neadc.org,vicepresident@neadc.org',
                'club_url': 'http://www.neadc.org/',
                'country': 'USA'
            },
            'North Shore Divers Club': {
                'club_name': 'North Shore Divers Club',
                'city': 'Revere, MA',
                'contact': None,
                'email': None,
                'club_url': 'https://www.northshorediversclub.com/cgi-sys/suspendedpage.cgi',
                'country': 'USA'
            },
            'North Shore Frogmen': {
                'club_name': 'North Shore Frogmen',
                'city': 'Beverly, MA',
                'contact': 'Dylan Langelier',
                'email': 'officers@northshorefrogmen.com',
                'club_url': 'http://www.northshorefrogmen.com/',
                'country': 'USA'
            },
            'Old Colony Amphibians Club': {
                'club_name': 'Old Colony Amphibians Club',
                'city': 'South Attleboro, MA',
                'contact': None,
                'email': None,
                'club_url': 'http://www.ocascuba.org/index.php',
                'country': 'USA'
            },
            'South Shore Neptunes': {
                'club_name': 'South Shore Neptunes',
                'city': 'Quincy, MA',
                'contact': None,
                'email': 'info@southshoreneptunes.org',
                'club_url': 'http://www.southshoreneptunes.org/index.html',
                'country': 'USA'
            }
        }

        for key in clubs.keys():
            club = clubs[key]

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
