# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import logging
import pymongo


class MongodbPipeline:
    collection_name = "best_movies"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            "mongodb+srv://dhgiang:Df7604129@cluster0.v2jiv.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.client["IMDB"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
