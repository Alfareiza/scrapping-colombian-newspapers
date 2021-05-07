import json

import requests
from bs4 import BeautifulSoup
import os

from scrap.resources.get import url_analyse


def get_site_info(url):
    response = requests.get(url)
    if response.status_code != 400:
        return response.text


def create_file(content, filename='index.html'):
    with open(filename, 'w', encoding="utf-8") as fp:
        fp.write(content)


def get_soup_info(css_selector, filename='index.html'):
    with open(filename, encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    news = soup.select(css_selector)
    return news


def get_json_data(filename):
    with open(filename, encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    script = soup.find_all('script', attrs={'type': 'application/javascript'})[-1].string.strip()[133:]
    starts_from, until_to = script.index("{\"type\""), script.index(";Fusion.globalContentConfig=")
    script = json.loads(script[starts_from:until_to])
    txts, links = [], []
    for new in script['content_elements']:
        txts.append(new['headlines']['basic'])
        links.append(new['headlines']['basic'])
    return txts


def obtain_info(url, css_selector):
    filename = f'{url_analyse(url)}.html'
    if os.path.isfile(filename):
        if 'elespectador' in url:
            news = get_json_data(filename)
        else:
            news = get_soup_info(css_selector, filename)
        return news
    else:
        content = get_site_info(url)
        create_file(content, filename)
        if 'elespectador' in url:
            news = get_json_data(filename)
        else:
            news = get_soup_info(css_selector, filename)
        return news


if __name__ == '__main__':
    css_selector = 'h2'
    news = obtain_info(url='https://www.elespectador.com', css_selector=css_selector)
    # for i, new in enumerate(news, start=1):
    #     print(i, new.get_text(strip=True))
    # Lazo para usarlo con el espectador
    for i, j in enumerate(news):
        print(i, j)
    print(5 * '==', len(news), 'Noticias capturadas', 5 * '==')
