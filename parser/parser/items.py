# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from mainapp.models import Product, Category

class CategoryItem(DjangoItem):
    django_model = Category

class ProductItem(DjangoItem):
    django_model = Product
    parse_category = scrapy.Field()
    images = scrapy.Field()

class ProductCutsItem(DjangoItem):
    django_model = Product
    