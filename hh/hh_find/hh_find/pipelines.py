# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String


DATABASE_NAME = 'hh.sqlite'
engine = create_engine(f'sqlite:///{DATABASE_NAME}', future=True)
Session = sessionmaker(bind=engine, future=True)()
Base = declarative_base()


class Post(Base):
    __tablename__ = 'Post'

    id = Column(Integer, primary_key=True)
    href = Column(String())
    title = Column(String())
    author = Column(String())
    salary = Column(String())
    experience = Column(String())
    type_of_work = Column(String())
    content = Column(String())
    status = Column(String())
    note = Column(String())

    def __init__(self, href, title, author, salary, experience, type_of_work, content, status, note):
        self.title = title
        self.salary = salary
        self.experience = experience
        self.author = author
        self.content = content
        self.href = href
        self.type_of_work = type_of_work
        self.status = status
        self.note = note


class HhFindPipeline:
    def open_spider(self, spider):
        Base.metadata.create_all(engine)

    def process_item(self, item, spider):
        if item:
            ind = item['url'].find('?')
            item['url'] = item['url'][:ind]
            if '\xa0' in item['salary']:
                item['salary'] = item['salary'].replace('\xa0', ' ')
            if '   ' in item['salary']:
                item['salary'] = item['salary'].replace('   ', ' ')
            if '  ' in item['salary']:
                item['salary'] = item['salary'].replace('  ', ' ')

            symbol = ['<p>', '</p>', '<li>', '</li>',
                      '<span>', '</span>', '<ul>', '</ul>', '<div>', '</div>', '<br>', '<strong>', '</strong>', '<span class="highlighted">', '<div class="vacancy-branded-user-content" itemprop="description" data-qa="vacancy-description">', '<div class="g-user-content" data-qa="vacancy-description">']
            for i, v in enumerate(symbol):
                if v in item['content']:
                    item['content'] = item['content'].replace(v, '')

            if '    ' in item['content']:
                item['content'] = item['content'].replace('    ', ' ')
            if '   ' in item['content']:
                item['content'] = item['content'].replace('   ', ' ')
            if '  ' in item['content']:
                item['content'] = item['content'].replace('  ', ' ')

            post = Session.query(Post).filter(Post.href == item['url']).first()
            if not post:
                item_for_insert = Post(item['url'], item['title'], item['author'], item['salary'],
                                       item['experience'], item['type_of_work'], item['content'], None, 'NEW')
                Session.add(item_for_insert)
                Session.commit()
                print(f"Новая вакансия: {item['title']} от {item['author']}")

            else:
                print(f"ПОВТОР: {item['title']} от {item['author']}")
            Session.close()
