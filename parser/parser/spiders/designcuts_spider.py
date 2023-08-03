import scrapy
from scrapy import Request

from asgiref.sync import sync_to_async

from parser.parser.items import ProductCutsItem

from mainapp.models import Product


class DesingCutsSpider(scrapy.Spider):
    name = "designcuts"
    allowed_domains = ['designcuts.com']
    
    @sync_to_async
    
    def pipeline(self, item_data):
        """Load data to db"""
        product=Product.objects.create(name=item_data['name'])
        product.save()
        print('item/data',product )


    start_url = 'https://www.designcuts.com'
    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse)
    
    """def get_categories(self, response):
        categories = response.css('div.collapse').getall()
        for cat in categories:
            cat_link = cat.css('a::attr(href)').extract()[5]
            yield Request(url=cat_link, callback=self.parse_products)

    def parse_cat(self, response):
        data = response.xpath('//script/text()').extract()[-1]
        pages=data.split('"total_pages":')[1].split('}')[0]
        for page_num in range(1, int(pages) + 1):
            url = response.request.url + f'?_paged={page_num}'
            yield Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        links = response.xpath('//h2/a/@href').extract()
        for detain_link in links:
            yield Request(url=detain_link, callback=self.parse_products)"""

    def parse(self, response):
        item = ProductCutsItem()
        item['name']= 'SuperTest2'
        return self.pipeline(item)
        
                

    def parse_products(self, response):
        item=ProductCutsItem()
        categories = response.css('div.collapse').getall()
        items=[]
        for cat in categories:
            item['name'] = cat
            items.append(item)
        return item
    


  