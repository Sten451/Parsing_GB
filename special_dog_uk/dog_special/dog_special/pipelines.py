# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import json
import os.path
from itemadapter import ItemAdapter


class DogSpecialPipeline:
    all_name = []

    def process_item(self, item, spider):
        town = self.get_all_town(item.get('address'))
        if town:
            item['description'] = item.get('description').strip()
            item['address'] = " ".join(item.get('address'))
            item['town'] = town
            if not item['phone']:
                item['phone'] = 'Phone not found'
            self.write_in_csv(item)
        else:
            item['description'] = item.get('description').strip()
            with open("not.json", 'a') as file:
                file.write(json.dumps(item))

        return item

    def get_all_town(self, address):
        with open("Towns_List.csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == 'Town':
                    continue
                if row[0] in address:
                    print("Город найден", row[0])
                    return row[0]
            return None

    def write_in_csv(self, data):
        # если полученное имя компании уже есть в списке выходим из функции
        # и не записываем, иначе помещаем его в список и записываем в файл
        if data.get('name') in self.all_name:
            print("this company is already on the list", data['name'])
            return
        self.all_name.append(data.get('name'))
        print(self.all_name)
        find_file = False
        if os.path.exists('result.csv'):
            find_file = True
            print("find")
        with open("result.csv", 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=list(
                data.keys()), quoting=csv.QUOTE_NONNUMERIC)
            if not find_file:  # т.к. передаем словарь, надо только один раз записать заголовок
                writer.writeheader()
            writer.writerow(data)
            print("Запись в файл осуществлена")
