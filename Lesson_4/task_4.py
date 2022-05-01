import os
import sys
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import join
from sqlalchemy import select

DATABASE_NAME = 'dz4.sqlite'
engine = create_engine(f'sqlite:///{DATABASE_NAME}', future=True)
Session = sessionmaker(bind=engine, future=True)()
Base = declarative_base()


# класс Юзер
class Author(Base):
    __tablename__ = 'Author'

    id = Column(Integer, primary_key=True)
    name = Column(String())

    def __init__(self, name):
        self.name = name


# класс цитаты
class Quotes(Base):
    __tablename__ = 'Quotes'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    author_id = Column(Integer, ForeignKey('Author.id'))

    def __init__(self, name, author_id):
        self.name = name
        self.author_id = author_id


# класс цитаты
class Tags(Base):
    __tablename__ = 'Tags'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    quote = Column(Integer, ForeignKey('Quotes.id'))

    def __init__(self, name, quote):
        self.name = name
        self.quote = quote


def create_db():
    Base.metadata.create_all(engine)


# Функция получает название категорий навигации
def get_quotes(url, page=1):
    soup = verify_response(url, page)
    # замечание учтено про строку ниже)))
    if soup:
        while True:  # мы же не знаем сколько там страниц поэтому бесконечный цикл
            if page != 1:
                soup = verify_response(url, page)
            all_quotes = soup.select('.quote')
            for item in all_quotes:
                quote = item.select_one('span[class=text]').text.strip()
                author = item.select_one('small[class=author]').text.strip()
                tags = item.find_all('a', class_='tag')
                tag_list = []
                for tag in tags:
                    tag_list.append(tag.text.strip())

                # Создаем экземпляры объектов и вызываем функции записи в бд, два раза потому что
                # нельзя изначально получить id экземпляра, если только имя писать
                author = Author(author)
                save_in_db(author, Author)

                quote = Quotes(quote, author.name)
                save_in_db(quote, Quotes)

                # Вызываем функцию записи в БД конечно не самая лучшая реализация передавать
                # экземпляры и сами классы функций
                # Теги придется писать отдельно
                for tag in tag_list:
                    tag = Tags(tag, quote.id)
                    print('Записываем в базу данных', '********', tag.name)
                    Session.add(tag)
                    Session.commit()

            # проверяем наличие кнопки next, если ее нет то break
            button_next = soup.find('nav').find('li', class_='next')
            if button_next is None:  # если кнопки next нет значит выходим из бесконечного цикла
                print("Больше страниц для парсинга нет. Парсинг закончен.")
                break
            page += 1
    else:
        print('Фреймворк не получил данные для разбора...')


def save_in_db(examples, ClassName):
    if Session.query(ClassName).filter(
            ClassName.name == examples.name).count():
        print("найден повтор. Пропускаем запись.")
    else:
        print('Записываем в базу данных', examples.name)
        Session.add(examples)
        Session.commit()


# Функция проверки доступности сайта, а иначе выход
def verify_response(url, page):
    response = requests.get(url+str(page))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        return soup
    else:
        print(f"Error: {response.status_code}")
        sys.exit(-1)


URL = 'https://quotes.toscrape.com/page/'


def first_create():
    # Проверяем при запуске на наличие базы данных, если нет то создаём
    root = os.getcwd()
    path = os.path.join(root, 'dz4.sqlite')

    if os.path.exists(path):
        print("Найдена база данных. Удалите базу данных.")
        sys.exit(-1)
    else:
        print("База данных не найдена. Создаём.")
        create_db()  # Создаём базу данных


first_create()
get_quotes(URL)

# Получаем список авторов
print('Количество авторов', Session.query(Author).count())
# Получаем количество цитат
print('Количество цитат', Session.query(Quotes).count())
# Получаем количество тегов
print('Количество тегов', Session.query(Tags).count())
