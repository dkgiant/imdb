import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=r'//h3[@class="lister-item-header"]/a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield{
            'title': response.xpath(r'//div[@class="title_wrapper"]/h1/text()').get(),
            'year': response.xpath(r'//span[@id="titleYear"]/a/text()').get(),
            'duration': response.xpath(r'normalize-space(//time/text())').get(),
            'genre': response.xpath(r'//div[@class="subtext"]/a/text()').get(),
            'rating': response.xpath(r'//span[@itemprop="ratingValue"]/text()').get(),
            'movie_url': response.url,
        }
