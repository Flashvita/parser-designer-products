from django.core.management.base import BaseCommand

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from parser.parser import settings as my_settings
from parser.parser.spiders.designcuts_spider import DesingCutsSpider


class Command(BaseCommand):
    help = 'Release spider'

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)

        process = CrawlerProcess(settings=crawler_settings)

        process.crawl(DesingCutsSpider)
        process.start()