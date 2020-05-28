# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import pymysql
import pymongo
from arcgis_tiles.items import *


class ArcgisTilesPipeline:
    def process_item(self, item, spider):
        return item


class PostgresJsonPipeline():
    # 如果主键，有存在的会报错
    def __init__(self, host, port, database, username, password):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('POSTGRES_HOST'),
            port=crawler.settings.get('POSTGRES_PORT'),
            database=crawler.settings.get('POSTGRES_DATABASE'),
            username=crawler.settings.get('POSTGRES_USERNAME'),
            password=crawler.settings.get('POSTGRES_PASSWORD'),
        )

    def open_spider(self, spider):
        self.db = psycopg2.connect(database=self.database, user=self.username,
                                     password=self.password, host=self.host, port=self.port, )
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        # self.cur.close()
        self.db.close()

    def process_item(self, item, spider):
        if isinstance(item, ArcgisTilesJson):
            data = dict(item)
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            # sql = 'insert into service(service_name, service_config) values("%s")' % (values)
            # sql = "insert into service(service_name, service_config) values ('1', '1')"
            sql = 'insert into service (service_name, service_config) values (%s)' % (values)
            try:
                self.cursor.execute(sql, tuple(data.values()))
                self.db.commit()
            except Exception as e:
                self.db.rollback()
        return item


class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password,
                                  self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        # keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into service (name, config) values (%s)' % (values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item


class SqlitePipeline():
    pass


class MongoPipeline():
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db1 = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # 瓦片进入后类型应该是ArcgisTilesItem，但是不知道为什么变成了None
        if isinstance(item, ArcgisTilesItem):
            data = dict(item)
            name = data.get('tile_collection')
            # name = item.collection
            del data['tile_collection']
            self.db1[name].insert(data)
        return item

    def close_spider(self, spider):
        self.client.close()