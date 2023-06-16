# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DivesitescrapingPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        cols = ['tag', 'date', 'club_name', 'building', 
                'city', 'country', 'contact', 'phone',
                'email']

        for col in cols:
            value = adapter.get(col)
            if ':' in value:
                adapter[col] = value.split(':')[1].strip()

        return item
