import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['www.imdb.com']
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc',headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths=r'//h3[@class="lister-item-header"]/a'), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths=r'(//a[@class="lister-page-next next-page"])[2]'), process_request='set_user_agent'),
        
    )
    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent

        return request

    def parse_item(self, response):
        yield{
            'title': response.xpath(r'//div[@class="title_wrapper"]/h1/text()').get(),
            'year': response.xpath(r'//span[@id="titleYear"]/a/text()').get(),
            'duration': response.xpath(r'normalize-space(//time/text())').get(),
            'genre': response.xpath(r'//div[@class="subtext"]/a/text()').get(),
            'rating': response.xpath(r'//span[@itemprop="ratingValue"]/text()').get(),
            'movie_url': response.url,
            # 'user-agent':response.request.headers['User-Agent']
        }
