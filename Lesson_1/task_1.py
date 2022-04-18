import requests
"""Парсер погоды"""
url = 'http://api.weatherapi.com/v1/current.json'

params = {
    'key': 'cec1f0aed2714d46817181112221804',
    'q': 'Ryazan'
}
req = requests.get(url, params=params)
if req.status_code == 200:
    response = req.json()
    print(
        f"Температура в городе {response['location']['name']} в {response['current']['last_updated']} равняется {response['current']['temp_c']} градусов по цельсию.")
else:
    print('Ошибка доступа к сайту')
