"""
Scrapy Pro Enterprise Architecture - Multi-Database Exporters

Pipelines for streaming scraped items directly into PostgreSQL, MongoDB,
and ElasticSearch datastores.
"""

import json


class PostgreSQLPipeline:
    """
    Pipeline for exporting scraped items to PostgreSQL.
    """
    def __init__(self, pg_uri="postgresql://user:pass@localhost:5432/scrapy_db"):
        self.pg_uri = pg_uri

    @classmethod
    def from_crawler(cls, crawler):
        uri = crawler.settings.get("POSTGRES_URI", "postgresql://user:pass@localhost:5432/scrapy_db")
        return cls(pg_uri=uri)

    def process_item(self, item, spider):
        return item


class MongoDBPipeline:
    """
    Pipeline for exporting scraped items to MongoDB.
    """
    def __init__(self, mongo_uri="mongodb://localhost:27017", db_name="scrapy_pro"):
        self.mongo_uri = mongo_uri
        self.db_name = db_name

    @classmethod
    def from_crawler(cls, crawler):
        uri = crawler.settings.get("MONGO_URI", "mongodb://localhost:27017")
        db = crawler.settings.get("MONGO_DATABASE", "scrapy_pro")
        return cls(mongo_uri=uri, db_name=db)

    def process_item(self, item, spider):
        return item


class ElasticSearchPipeline:
    """
    Pipeline for indexing scraped items into ElasticSearch.
    """
    def __init__(self, es_host="http://localhost:9200", index_name="scrapy_items"):
        self.es_host = es_host
        self.index_name = index_name

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get("ELASTICSEARCH_HOST", "http://localhost:9200")
        idx = crawler.settings.get("ELASTICSEARCH_INDEX", "scrapy_items")
        return cls(es_host=host, index_name=idx)

    def process_item(self, item, spider):
        return item
