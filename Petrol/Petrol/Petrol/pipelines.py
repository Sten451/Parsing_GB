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

DATABASE_NAME = 'dz7.sqlite'
engine = create_engine(f'sqlite:///{DATABASE_NAME}', future=True)
Session = sessionmaker(bind=engine, future=True)()
Base = declarative_base()


class Team(Base):
    __tablename__ = 'Team'

    id = Column(Integer, primary_key=True)
    rank = Column(String())
    name = Column(String())
    division = Column(String())
    wins = Column(String())
    loses = Column(String())
    ol = Column(String())
    pts = Column(String())

    def __init__(self, rank, name, division, wins, loses, ol, pts):
        self.rank = rank
        self.name = name
        self.division = division
        self.wins = wins
        self.loses = loses
        self.ol = ol
        self.pts = pts


class PetrolPipeline:
    def open_spider(self, spider):
        Base.metadata.create_all(engine)

    def process_item(self, item, spider):
        if item['name']:
            item_for_insert = Team(
                item['rank'], item['name'], item['division'], item['wins'], item['loses'], item['losses_ot_avg'], item['points_avg'])
            Session.add(item_for_insert)
            Session.commit()
            Session.close()


class Petrol_countPipeline:
    def process_item(self, item, spider):
        return item
