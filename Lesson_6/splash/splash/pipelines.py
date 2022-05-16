# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

DATABASE_NAME = 'dz6.sqlite'
engine = create_engine(f'sqlite:///{DATABASE_NAME}', future=True)
Session = sessionmaker(bind=engine, future=True)()
Base = declarative_base()


class Product(Base):
    __tablename__ = 'Product'

    id = Column(Integer, primary_key=True)
    title = Column(String())
    price = Column(String())
    description = Column(String())
    image = Column(String())
    url = Column(String())

    def __init__(self, title, price, description, image, url):
        self.title = title
        self.price = price
        self.description = description
        self.image = image
        self.url = url


class SplashPipeline:
    def open_spider(self, spider):
        Base.metadata.create_all(engine)

    def process_item(self, item, spider):
        item_for_insert = Product(
            item['title'], item['price'], item['description'], item['image'], item['url'])
        Session.add(item_for_insert)
        Session.commit()
        Session.close()
