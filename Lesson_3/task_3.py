import sys
import json
import requests
from bs4 import BeautifulSoup


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
                author = item.select_one(
                    'span small[class=author]').text.strip()
                tags = item.find_all('a', class_='tag')
                tag_list = []
                for tag in tags:
                    tag_list.append(tag.text.strip())
                quotes_dict = {
                    'quotes': quote,
                    'author': author,
                    'tags': tag_list,  # Вы сказали хороший тон источник)))
                    'source': 'https://quotes.toscrape.com'
                }
                with open('test2.json', 'a', encoding='utf-8') as file:
                    parsing = json.dumps(quotes_dict, ensure_ascii=False)
                    file.write(parsing + '\n')
            # проверяем наличие кнопки next, если ее нет то break
            button_next = soup.find('nav').find('li', class_='next')
            if button_next is None:  # если кнопки next нет значит выходим из бесконечного цикла
                print("Больше страниц для парсинга нет. Парсинг закончен.")
                break
            page += 1
    else:
        print('Фреймворк не получил данные для разбора...')


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


# Вызов функции
get_quotes(URL)
