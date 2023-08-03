import scrapy

from scrapy.loader.processors import TakeFirst

from asgiref.sync import sync_to_async, async_to_sync

class CreativeSpider(scrapy.Spider):
    name = "creative"
    allowed_domains = ['creativemarket.com']
    start_url = 'https://creativemarket.com/'
    
    def start_requests(self):
        urls = ['https://creativemarket.com/free-goods',]
        for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def response_is_ban(self, request, response):
        print('your banned creative market!!!!!!!!!!!!!!!!!!!!!!')
        return b'banned' in response.body

    def exception_is_ban(self, request, exception):
        return None

    def parse(self, response):
        filename = f'creativemarket.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')