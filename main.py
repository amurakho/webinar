import csv

import requests
from bs4 import BeautifulSoup

import settings


def parse_content(content):
    soup = BeautifulSoup(content, 'html.parser')

    boxes = soup.find_all('article', class_='box')

    page = []

    for box in boxes:
        if box.find('p', class_='lead'):
            return page

        data = {
            'link': box.find('a', class_='article-link').attrs['href'],
            'title': box.find('h2', class_='entry-title').get_text(),
            'text': box.find('div', class_='entry-content').get_text(),
        }
        page.append(data)

    return page


def save_to_csv(file_path, data):
    with open(file_path, 'w') as file:
        writer = csv.DictWriter(
            file,
            fieldnames=['link', 'title', 'text'],
            quoting=csv.QUOTE_MINIMAL,
        )

        writer.writeheader()
        for elem in data:
            writer.writerow(elem)


def pass_request(tag_name, page_num, data=None):

    url = settings.BASE_URL.format(tag=tag_name, page_num=page_num)

    response = requests.get(url)

    page = parse_content(response.content)

    if page:
        data.extend(page)
        pass_request(tag_name, page_num+1, data)
    else:
       save_to_csv(tag_name + '.csv', data)


if __name__ == '__main__':

    for name in settings.PAGES_NAMES:
        pass_request(name, 1, [])



