import requests
import pandas as pd
import logging.config
from scrap.resources import get

TIMEOUT = 20

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

logging.config.fileConfig(fname='logs/logging.ini')
logger = logging.getLogger('root')


def touring_newspapers():
    global_news, global_links = [], []
    j, totaltimeResponse = 0, 0
    for url, css_selector in NEWSPAPERS.items():
        news, links = [], []
        try:
            response = requests.get(url, timeout=TIMEOUT)
            deltaResponse = response.elapsed.total_seconds()
            set_of_news = get.gettin_news(css_selector, response)
            for i, new in enumerate(set_of_news, 1):
                txt = get.clean_text(new.get_text(strip=True))
                link = get.link_valid(new, url)
                if not any((True for x in DONT_INCLUDE if x in txt)) and (170 > len(txt) > 30) and link:
                    global_news.append(txt)
                    global_links.append(link[0])
                    news.append(txt)
                    links.append(link[0])
        except requests.RequestException as e:
            logger.warning(f'Unreacheable info from {url} > {e}')
        j += 1
        logger.info(
            f'{j} de {len(NEWSPAPERS)}, {get.url_analyse(url)}, '
            f'timeResponse= {round(deltaResponse, 2)}s, qtyNews= {len(news)}')
        # get.export_by_newspaper(news, links, url)
        # if not len(news) == 0:
        # get.generate_csv(news, links, url)
        # get.generate_xml(news, links, url)
        # get.generate_json(news, links, url)
        totaltimeResponse += deltaResponse

    # get.export_global_news(global_news, global_links)
    if not len(global_news) == 0:
        df = pd.DataFrame({'Noticias ': global_news, 'Links': global_links}, index=range(1, len(global_news) + 1))
        df.to_csv('all_news.csv', index=range(1, len(global_news) + 1))
        logger.info(
            f'{len(NEWSPAPERS)} NewsPapers Scrapped, Total of News={len(global_news)}, total timeResponse={round(totaltimeResponse, 1)}s')
        return df
    else:
        pass


touring_newspapers()

if __name__ == '__main__':
    print('olá')