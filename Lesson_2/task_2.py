import sys
import json
import requests
from bs4 import BeautifulSoup

# Функция получает название категорий навигации


def get_navigation_url(url, page=1):
    soup = verify_response(url, page)
    category = soup.find(
        'ul', class_='nav-list').find('li').find('ul').find_all('li')
    category_list = []
    for item in category:
        if item.find('a'):
            category_list.append(item.text.strip())
    print('Сайт содержит следующие категории:', category_list)

# Функция получает картинки, цену, название


def get_image_price_title(url, page=1):
    soup = verify_response(url, page)
    # получаем максимальное количество страниц
    max_count_text = soup.find('ul', class_='pager').find(
        'li', class_='current').text.strip()
    index_space_right = max_count_text.rfind(' ')
    max_count = int(max_count_text[index_space_right+1:])
    res_parsing = []
    # Организовываем цикл в ходе которого делаем запрос к каждой странице, потом все это собираем в массив и записываем в файл
    for i in range(max_count):
        if page != 1:
            soup = verify_response(url, page)
        card = soup.find('ol', class_='row').findAll('li')
        for item in card:
            title = item.find('article', class_='product_pod').find(
                'h3').find('a').text.strip()
            price = item.find('article', class_='product_pod').find(
                'div', class_='product_price').find('p', class_='price_color').text.strip()
            image_url = item.find('article', class_='product_pod').find(
                'div', class_='image_container').find('a').find('img')
            res_parsing.append({'title': title, 'price': price,
                                'image_url': image_url['src']})
        page += 1

    print(res_parsing)
    with open('test.txt', 'w', encoding='utf-8') as file:
        parsing = json.dumps(res_parsing, ensure_ascii=False)
        file.write(parsing)


# Функция проверки доступности сайта, а иначе выход
def verify_response(url, page):
    response = requests.get(url+str(page)+'.html')
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        return soup
    else:
        print(f"Error: {response.status_code}")
        sys.exit(-1)


URL = 'https://books.toscrape.com/catalogue/page-'


# Вызов первой функции
get_navigation_url(URL)

# Вызов второй функции
get_image_price_title(URL)
