import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.avito.ru/lipetsk/kvartiry'
domen = 'https://www.avito.ru/'


def get_html(url, params=None):
    return requests.get(url, params=params)


def get_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('div', class_='snippet-horizontal')
    data_items = []
    for i in products:
        data_items.append({
            'name': i.find('a', class_='snippet-link').get_text(strip=True),
            'url': domen + i.find('a', class_='snippet-link').get('href'),
            'price': i.find('span', class_='snippet-price').get_text(strip=True).replace(' ', '').split('₽')[0],
            'place': i.find('span', class_='item-address__string').get_text(strip=True),
            'time': i.find('div', class_='snippet-date-info').get_text(strip=True)
        })
    return data_items


def get_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    return int(soup.find('div', class_='pagination-root-2oCjZ').find_all('span')[-2].get_text())


def save_file(data_items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=':')
        writer.writerow(['Название', 'URL', 'Цена', 'Место', 'Время'])
        for i in data_items:
            writer.writerow([i['name'], i['url'], i['price'], i['place'], i['time']])


def parse():
    html = get_html(url)
    if html.status_code == 200:
        pages = get_page(html.text)
        data_set = []
        for number in range(1, pages + 1):
            print(f'Парсинг {number} страницы из {pages}...')
            data_set.extend(get_info(get_html(url, params={'0': number}).text))
        save_file(data_set, 'file.csv')
    else:
        print('ERROR. YOU ARE STUPID, SORRY!')


if __name__ == "__main__":
    parse()
