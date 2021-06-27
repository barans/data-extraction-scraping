# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import locale


class HepsiburadaPipeline:

    def __init__(self):
        self.ids = set()
        locale.setlocale(locale.LC_NUMERIC, "tr")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['id'] in self.ids:
            raise DropItem(f"Duplicate: {item}")
        else:
            if adapter.get('price'):
                self.ids.add(adapter['id'])
                item['price'] = locale.atof(item['price'])
                return item
            else:
                raise DropItem(f"No Price {item}")
