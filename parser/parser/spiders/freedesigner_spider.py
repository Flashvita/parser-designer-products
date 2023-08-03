import datetime


import scrapy
from scrapy import Request

from parser.parser.items import CategoryItem, ProductItem


class FreeDesignerSpider(scrapy.Spider):
    name = 'freedesigner'
 
    allowed_domains = ['freedesignresources.net']
    start_url = 'http://freedesignresources.net/'
    count = 0
    
    def start_requests(self):
        yield Request(url=self.start_url, callback=self.get_categories)

    def get_categories(self, response):
        categories = response.css('ul#menu-main-menu > li')
        for cat in categories:
            cat_link = cat.css('a::attr(href)').extract()[0]
            yield Request(url=cat_link, callback=self.parse_cat)

    def parse_cat(self, response):
        data = response.xpath('//script/text()').extract()[-1]
        pages=data.split('"total_pages":')[1].split('}')[0]
        for page_num in range(1, int(pages) + 1):
            url = response.request.url + f'?_paged={page_num}'
            yield Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        links = response.xpath('//h2/a/@href').extract()
        for detain_link in links:
            yield Request(url=detain_link, callback=self.parse_products)

    def parse(self, response):
        c = response.css('div.container ul.sf-menu a::text').getall()
        cat_len = len(c)
        if self.count < cat_len:
            item=CategoryItem()
            cat = response.css('div.container ul.sf-menu a::text').getall()[int(f'{self.count}')]
            print('category', cat)
            if cat:
                self.count += 1
                item['name']=cat
                yield item
                
    def format_date(self, response):
        input_date = response.css('.meta-date::text').extract()[0]
        if 'th' in input_date.split(' ')[1]:
            date_str = datetime.datetime.strptime(input_date, '%B %dth, %Y')
        elif 'st' in input_date.split(' ')[1]:
            date_str = datetime.datetime.strptime(input_date, '%B %dst, %Y')
        elif 'nd' in input_date.split(' ')[1]:
            date_str = datetime.datetime.strptime(input_date, '%B %dnd, %Y')
        elif 'rd' in input_date.split(' ')[1]:
            date_str = datetime.datetime.strptime(input_date, '%B %drd, %Y')
        date_str = datetime.datetime.strftime(date_str, '%Y-%m-%d')
        return date_str

    def parse_products(self, response):
        item=ProductItem()
        name = response.css('.entry-title::text').extract()
        item['orig_link']=response.url
        item['name'] = name
        item['created'] = self.format_date(response)
        item['parse_desc'] = response.xpath('//div[@class="description"]//*/text()').extract()
        item['parse_category'] = response.xpath('//a[@rel="tag"]/text()').extract()
        yield item   
                  
