# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DogSpecialPipeline:

    def process_item(self, item, spider):
        item['description'] = item.get('description').strip()
        item['address'] = " ".join(item.get('address'))
        if not item['phone']:
            item['phone'] = 'Phone not found'
        item['town'] = item['town'].decode('utf-8')
        if item.get('town').rfind('?') == -1:
            item['town'] = item['town'][item.get('town').rfind(
                '/') + 1:]
        else:
            item['town'] = item['town'][item.get('town').rfind(
                '/') + 1:item.get('town').rfind('?')]
        item['town'] = (item['town'].replace('-', ' ')).capitalize()
        return item
