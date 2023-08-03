import scrapy
from scrapy import Request

from parser.parser.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'df_product'
 
    allowed_domains = ['freedesignresources.net']
    start_url = 'http://freedesignresources.net/'
    local_id = 0

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.get_categories)

    def get_categories(self, response):
        categories = response.css('ul#menu-main-menu > li')
        for cat in categories:
            cat_link = cat.css('a::attr(href)').extract()[0]
            yield Request(url=cat_link, callback=self.parse_category)

    def parse_category(self, response):
        script_text = response.xpath('//script/text()').extract()[-1]
        total_pages = script_text.split('"total_pages":')[1].split('}')[0]
        print(response.url.split('/')[-2])
        print(f'Total pages: {total_pages}')
        for page_num in range(1, int(total_pages) + 1):
            url = response.request.url + f'?_paged={page_num}'
            yield Request(url=url, callback=self.parse_category_page)

    def parse_category_page(self, response):
        link_list = response.xpath('//h2/a/@href').extract()
        for detain_link in link_list:
            yield Request(url=detain_link, callback=self.parse)

    
    def parse(self, response):
        item=ProductItem()
        item['name']="test"
        item['file_type']='s'
        yield item 
                




            
            

    

    