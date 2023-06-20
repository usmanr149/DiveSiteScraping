import scrapy


class DiveNiSpider(scrapy.Spider):
    name = "dive_ni"
    allowed_domains = ["www.dive-ni.com"]
    start_urls = ["https://www.dive-ni.com/dive-clubs/"]

    def parse(self, response):
        pass
