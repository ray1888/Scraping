# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class JobbglePipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(host = "localhost", port = 27017)
        db = client['Jobb']
        self.job = db['job']


    def process_item(self, item, spider):
        try:
            self.job.insert(dict(item))
        except Exception:
            pass

        return item
