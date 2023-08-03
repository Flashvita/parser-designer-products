# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

from mainapp.models import Product, Category
from itemadapter import ItemAdapter
from asgiref.sync import sync_to_async, async_to_sync
"""class ParserPipeline:
    def process_item(self, item, spider):
        return item"""


from django import db
from scrapy.exceptions import DropItem
from django.shortcuts import  get_object_or_404



class CategoryPipeline(object):
   
    @sync_to_async
    def process_item(self, item, spider, *args, **kwargs):
        if item['name'] in ['Fonts','Graphics','Mockups', 'Templates', 'UI Kits', 'Add-Ons']:
            item.save()
            return item
        elif item['name'] in ['Display', 'Sans Serif', 'Serif', 'Script', 'Slab Serif']:
            category = get_object_or_404(Category, name='Fonts')
            item['level'] = 1
            item['parent'] = category
            item.save()
            return item
        
        elif item['name'] in ['Logo Templates', 'Presentation Templates', 'Print Templates', 'PSD Templates', 'Social Media', 'Website Templates']:
            category = get_object_or_404(Category, name='Templates')
            item['level'] = 1
            item['parent'] = category
            item.save()
            return item
        
        elif item['name'] in ['Icons']:
            category = get_object_or_404(Category, name='Graphics')
            item['level'] = 1
            item['parent'] = category
            item.save()
            return item
        else:
            name = item['parse_category'][-1]
            print('cat name= ', name)
            category = get_object_or_404(Category, name=name)
            item['category'] = category
            item.save()
            return item
                

class ProductPipeline(object):
    """
    Save product
    """
    @sync_to_async
    def process_item(self, item, spider):
        print('df_product')
        item.save()
        return item