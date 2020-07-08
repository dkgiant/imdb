import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookScrapeSpider(CrawlSpider):
    name = 'book_scrape'
    allowed_domains = ['books.toscrape.com']

    user_agent = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='http://books.toscrape.com/', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths=r'//article[@class="product_pod"]/div/a'), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths=r'//li[@class="next"]/a'), process_request='set_user_agent'),
    )
    def set_user_agent(self, request):
        request.headers['User-Agent']=self.user_agent
        return request
    def parse_item(self, response):
        yield{
            'book_name': response.xpath(r'//h1/text()').get(),
            'price': response.xpath(r'//p[@class="price_color"]/text()').get(),
            # 'user-agent': response.request.headers['User-Agent']
        }
