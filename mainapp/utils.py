import re

def generate_url_alias(cls_name, name, author_id=None):
    alias = name.strip().lower()
    if ('http' or 'www') in name:
        alias = re.sub(r'(^https?)|(:\/{1,2})|(w){3}(.)', '', alias)
        alias = re.sub('/', '-', alias)
    if '+' in name:
        alias = alias.replace('+', ' plus ')
    if '&' in name:
        alias = alias.replace('&', ' and ')
    alias = re.sub('^\.|[®\'\"″’\/\\:;]|\.$', '', alias)
    alias = alias.replace('.', '_')
    
    if cls_name in ('Product', 'Category'):
        alias = re.sub(r'-*\s*[–*;:,\s*-]\s*-*', '-', alias)
    return alias

def product_file_path(instance, filename):
    return f'products/{instance.id}/{filename}'