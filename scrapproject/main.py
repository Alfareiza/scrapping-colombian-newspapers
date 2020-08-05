import requests
import pandas as pd
from scrapproject.resources import get
from bs4 import BeautifulSoup
import logging

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
              'http://www.elnuevodia.com.co/nuevodia/': '.field-content',
              'https://www.elmanduco.com.co': '.article-title a', 'https://www.semana.com': 'h2.article-h a',
              'https://www.publimetro.co/co/': '.tit', 'https://www.pulzo.com': 'a.event-warmmap',
              'https://www.larepublica.co': '.agriculturaSect, .economiaSect, .globoeconomiaSect, '
                                            '.empresasSect, .ocioSect, .actualidadSect, .consumidorSect, '
                                            '.finanzasSect, .internet-economySect, .ganaderiaSect, .climaSect, '
                                            '.caja-fuerteSect'}

PERIODICOS = {'https://www.diariodelnorte.net': 'h3[itemprop="name"]'}

PERIODICOS2 = {'https://www.publimetro.co/co/': '.tit'}


def touring_newspapers():
    news, links = [], []
    for url, css_selector in NEWSPAPERS.items():
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            set_of_news = soup.select(css_selector)
            for i, new in enumerate(set_of_news, 1):
                txt = get.clean_text(new.get_text(strip=True))
                link = get.link_valid(new, url)
                if not any((True for x in DONT_INCLUDE if x in txt)) and (170 > len(txt) > 30) and link:
                    news.append(txt)
                    links.append(link[0])
            # print(f'{get.url_analyse(url)} [{len(news)}]')
            # get.generate_csv(news, links, url)
            # deltaResponse = response.elapsed.total_seconds()
        except requests.RequestException as e:
            print(f'No fue posible capturar info de {url} : ERROR > {e}')
    if not len(news) == 0:
        df = pd.DataFrame({'Noticias ': news, 'Links': links}, index=range(1, len(news) + 1))
        df.to_csv('all_news.csv', index=range(1, len(news) + 1))
        return df
    else:
        return f'No Information'


print(touring_newspapers())
