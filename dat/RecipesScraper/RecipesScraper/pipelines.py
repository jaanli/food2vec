# -*- coding: utf-8 -*-
from scrapy.exporters import JsonLinesItemExporter


class JsonPipeline(object):
    """Save Pipeline output to JSON."""
    def __init__(self, spider_name):
        self.file = open("output/{}_recipes.json".format(spider_name), 'wb')
        self.exporter = JsonLinesItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            spider_name=crawler.spider.name
        )

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
