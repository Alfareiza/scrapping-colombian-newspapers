import requests
from resources import get
from bs4 import BeautifulSoup

DONT_INCLUDE = ['sesión', 'ANUNCIOS', 'registro', 'En video', 'SUSCRÍBETE', '...', '#ENVIDEO',
                'EN VÍDEO', 'Video:']

# Documentation BautifulSoup https://beautiful-soup-4.readthedocs.io/en/latest/

NEWSPAPERS = {'https://www.elheraldo.co': ".titulo", 'https://www.zonacero.com': "div.title",
              'https://www.elpilon.com.co': ".land-see-post-title", 'https://www.eluniversal.com.co': "div.headline",
              'https://www.diariodelcesar.com': "h2.title", 'https://www.hoydiariodelmagdalena.com.co': "h2.title",
              'https://www.diariodelnorte.net': 'h3[itemprop="name"]', 'https://www.laopinion.com.co': "h2.titulo a",
              'https://www.eltiempo.com': "h3[itemprop='headline'] a",
              'https://www.elcolombiano.com': "h3 a .priority-content",
              'https://www.elespectador.com': "h3.Card_CustomLabel", 'https://www.lapatria.com': 'span.field-content',
              'https://www.elpais.com.co': 'h2.title a', 'https://www.elmundo.com': 'a div.col-md-12 h2',
              'http://www.elnuevodia.com.co/nuevodia/': '.field-content', }

PERIODICOS = {}


def touring_newspapers():
    news, links = [], []
    for url, css_selector in NEWSPAPERS.items():
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        set_of_news = soup.select(css_selector)
        for i, new in enumerate(set_of_news, 1):
            if not any((True for x in DONT_INCLUDE if x in new.text)) and (170 > len(new.text) > 33):
                news.append(get.clean_str_new(new.get_text(strip=True)))
                # print(i, get.clean_str_new(new.get_text(strip=True)), '|', new.parent.parent['href'])
                if new.find_all('a'):
                    if get.url_analyse(url) in new.a['href']:
                        links.append(new.a['href'])
                    else:
                        links.append(url + new.a['href'])
                elif new.name == 'a':
                    if get.url_analyse(url) in new['href']:
                        links.append(new['href'])
                    else:
                        links.append(url + new['href'])
                elif new.parent == 'a':
                    if get.url_analyse(url) in new.parent['href']:
                        links.append(new.parent['href'])
                    else:
                        links.append(url + new.parent['href'])
                elif new.parent.parent.name == 'a':
                    if get.url_analyse(url) in new.parent.parent['href']:
                        links.append(new.parent.parent['href'])
                    else:
                        links.append(url + new.parent.parent['href'])
                else:
                    del news[-1]
        # get.generate_csv(news, links, url)
    return news, links


get.unifyresults(touring_newspapers())
# get_new = int(input('=== Este programa retorna las noticias de los siguientes Portales === \n'
#                     '1 - El Heraldo - Barranquilla\n'
#                     '2 - El Pilon - Santa Marta\n'
#                     '3 - El Universal - Cartagena\n'
#                     '4 - Diario Del Cesar - Cesar\n'
#                     'Digite el número del periódico deseado: '))
# if get_new is 1:
#     get_elheraldo_news()
# elif get_new is 2:
#     get_elpilon_news()
# elif get_new is 3:
#     get_eluniversal_news()
# elif get_new is 4:
#     get_diariodelcesar_news()
# else:
#     'Perdiste'
