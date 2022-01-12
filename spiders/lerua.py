import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem



class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']
    #start_urls = ['http://leroymerlin.ru/']

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        #next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        #if next_page:
        #    yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        print()
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_xpath('name', '//h1//text()')
        loader.add_xpath('_id', '//span[@itemprop="sku"]/@content')
        loader.add_xpath('price', '//uc-pdp-price-view[@class="primary-price"]/meta[@itemprop="price"]/@content')
        loader.add_xpath('photos', "///picture[@slot='pictures']/source[1]/@srcset")
        loader.add_value('url', response.url)
        print()
        yield loader.load_item()
