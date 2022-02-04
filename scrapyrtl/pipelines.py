# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.utils.project import get_project_settings
from .items import ArticleItem
from dataclasses import asdict
from datetime import datetime

settings = get_project_settings()
today = datetime.today()

class ArticlesPipeline:
    def __init__(self):
        conn = pymongo.MongoClient(
            settings.get('MONGO_HOST'),
            settings.get('MONGO_PORT')
        )
        db = conn[settings.get('MONGO_DB_NAME')]
        self.collection = db["lu_articles_" + today.strftime("%Y%m%d%H%M")]

    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            self.collection.insert_one(asdict(item))
        return item