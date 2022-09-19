import logging.config
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from typing import List

import pandas as pd
from resources import get
import requests

DONT_INCLUDE = ['sesión', 'ANUNCIOS', 'registro', 'En video', 'SUSCRÍBETE', '...', '#ENVIDEO',
                'EN VÍDEO', 'Video:', 'Agenda tu cita', 'Buscas casa']

logging.config.fileConfig(Path(__file__).parent / 'setup_log.conf')

# logging.config.fileConfig('setup_log.conf')
# logger = logging.getLogger('root')
logger = logging.getLogger('chardet.charsetprober')
logger.setLevel(logging.INFO)


class Newspaper:
    def __init__(self, nombre, ciudad, url, css_selector='',
                 method='css_selector', ref='', news=[], delta_response=0):
        self.nombre = nombre
        self.ciudad = ciudad
        self.url = url
        self.css_selector = css_selector
        self.method = method
        self.ref = self.nombre.lower().replace(' ', '')
        self.news = news
        self.delta_response = delta_response

    def update_deltaresponse(self, seconds):
        self.delta_response = seconds

    def get_news(self):
        """
        Analiza el metodo de captura del objeto y retorna una lista de
        tuplas donde [0] es el texto y [1] es la notícia.
        :return: lista de tuplas
        """
        if not (response := self.request_to_newspaper_site()):
            return
        self.update_deltaresponse(response.elapsed.total_seconds())
        if self.method == 'css_selector':
            if news_captured := get.gettin_news_by_selector(self.css_selector, response):
                for i, new_captured in enumerate(news_captured, 1):
                    new = get.clean_text(new_captured.get_text(strip=True)), \
                          get.enlace(new_captured, self.url)

                    if self.validate_new(new): self.news.append(new)

                logger.info("{} - {:.1f}s, {} noticias.".
                            format(self.nombre,
                                   self.delta_response,
                                   self.get_qty_news()))

                return self.news
        elif self.method == 'own_method':
            if news_captured := eval(f"self.get_news_{self.ref}({response.content})"):
                for new_captured in news_captured:
                    txt, link = new_captured
                    new = get.clean_text(txt), get.absolute_link(link, self.url)

                    if self.validate_new(new): self.news.append(new)

                logger.info("{0} - {1}s, {2} noticias.".
                            format(self.nombre,
                                   self.delta_response,
                                   self.get_qty_news()))

                return self.news

        if not self.news:
            logger.warning("{} - {:.1f}s, {} noticias.".
                           format(self.nombre,
                                  self.delta_response,
                                  'sin'))
            return

    def validate_new(self, new) -> bool:
        """
        Valida que cada noticia cumpla con ciertos criterios para poder ser
        almacenada en self.news.
        :param new: tuple: ('texto de la noticia', 'https://site.com/texto-de-la-noticia')
        :return: True o False
        """
        txt, link = new
        ultima_noticia = self.news[-1] if self.get_qty_news() > 0 else ''
        return bool(not any(True for x in DONT_INCLUDE if x in txt) and
                    170 > len(txt) > 30 and link and txt not in ultima_noticia)

    def request_to_newspaper_site(self, attempts=2, timeout=20, error=None):
        """
        Principal request para el site del periodico.
        :return: response
        """
        try:
            if not attempts:
                return
            attempts -= 1
            return requests.get(self.url,
                                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
                                                       'Win64; x64) AppleWebKit/537.36 '
                                                       '(KHTML, like Gecko) Chrome/102.0.0.0'
                                                       ' Safari/537.36'},
                                verify=False, timeout=timeout)

        except requests.exceptions.ConnectionError as error:
            logger.warning(f'Unreacheable info from {self.url} > {error}')
            return
        except requests.exceptions.ReadTimeout as error:
            logger.warning(f'Unreacheable info from {self.url} (Read timed out)')
            timeout += 20
            return self.request_to_newspaper_site(timeout=timeout, attempts=attempts)

    def get_qty_news(self):
        """
        Calcula a cantidad total de noticias que el periodico posee.
        :return:
        """
        return len(self.news)

    def get_news_elespectador(self, response):
        """
        Método único de "elespectador" para buscar sus noticias en el
        json que el html posee.
        :param response: content of request
        :return: list of news
        """
        return get.gettin_news_by_findall(response)

    def print_news(self):
        """
        Consulta el atributo self.news : list de tuples, enumera e
        imprime las noticias en consola.
        :return:
        """
        if self.get_qty_news() > 0:
            for i, new in enumerate(self.news, start=1):
                txt, link = new
                print(i, txt, link)
        else:
            print(f'No hay noticias capturadas para \"{self.nombre.capitalize()}\".')

    def limpiar_noticias(self):
        self.news.clear()


class Scrapping_newspapers():
    def __init__(self, cant_periodicos=0, total_news=0, tiempo_total=0):
        self.cant_periodicos = cant_periodicos
        self.total_news = total_news
        self.tiempo_total = tiempo_total

    def get_all_news(self, newspapers_list: List[Newspaper], export='csv'):
        """
        Recibe lista de objetos de periodicos.
        todas_noticias es UNA lista de tuplas con todas las
        noticias de los objetos de la lista newspapers_list.
        """
        todas_noticias = []
        self.update_cant_periodicos(len(newspapers_list))
        for newspaper in newspapers_list:
            newspaper.get_news()
            todas_noticias += newspaper.news
            newspaper.limpiar_noticias()
            self.tiempo_total += newspaper.delta_response
        self.update_total_news(len(todas_noticias))
        if todas_noticias:
            if export == 'csv':
                self.generate_csv(todas_noticias)
            elif export == 'xml':
                self.generate_xml(todas_noticias)
            elif export == 'json':
                self.generate_json(todas_noticias)
        else:
            print("No hay noticias.")

    def create_dataframe(self, data):
        """
        Crea dataframe basándose en una lista de tuplas.
        :param data:
        :return: df:
        """
        df = pd.DataFrame(data, columns=['title', 'link'])
        df.index += 1
        return df

    def generate_csv(self, news_of_newspapers):
        """
        Recibe lista de tuplas (news_of_newspapers) lo convierte a dataframe y genera un csv.
        :param news_of_newspapers:
        :return:
        """
        self.create_dataframe(news_of_newspapers).to_csv('all_news.csv')

        if os.path.isfile('all_news.csv'):
            logger.info("{} Periodicos analizados, Total de Noticias: {}, Tiempo aproximado {:.2f}s".
                        format(self.cant_periodicos,
                               self.total_news,
                               self.tiempo_total))
            print("... Archivo all_news.csv generado con éxito!")

    def generate_xml(self, news_of_newspapers):
        content = get.to_xml(self.create_dataframe(news_of_newspapers))
        get.create_file('all_news.xml', content)

        if os.path.isfile('all_news.xml'):
            logger.info("{} Periodicos analizados, Total de Noticias: {}, Tiempo aproximado {:.2f}s".
                        format(self.cant_periodicos,
                               self.total_news,
                               self.tiempo_total))
            print("... Archivo all_news.xml generado con éxito!")

    def generate_json(self, news_of_newspapers):
        self.create_dataframe(news_of_newspapers).to_json('all_news.json', orient='records')

        if os.path.isfile('all_news.json'):
            logger.info("{} Periodicos analizados, Total de Noticias: {}, Tiempo aproximado {:.2f}s".
                        format(self.cant_periodicos,
                               self.total_news,
                               self.tiempo_total))

            print("... Archivo all_news.json generado con éxito!")

    def update_cant_periodicos(self, cant):
        """
        Actualiza el atributo de cantidad de periodicos que se procesan.
        :return:
        """
        self.cant_periodicos = cant

    def update_total_news(self, cant):
        self.total_news += cant


class Explore():
    def __init__(self, archivos=[]):
        self.current_path = os.getcwd()
        self.archivos = archivos

    def algun_nombre(self):
        """
        Función que lee el arhivo .csv o .xml o .json y analiza la información.
        :return:
        """
        self.detecta_archivos()
        if 'all_news.csv' in self.archivos:
            pass

    def detecta_archivos(self):
        """
        Detecta todos los archivos de la carpeta.
        :return: list: Lista con nombre de los archivos en esta carpeta.
        """
        onlyfiles = [f for f in listdir(self.current_path) if isfile(join(self.current_path, f))]
        self.archivos = onlyfiles

    def identifica_extension(self, file):
        """
        Detecta la extensión de un archivo.
        :param file: all_news.csv
        :return: str: csv
        """
        extension = file.split('.')[1]
        return extension


if __name__ == '__main__':
    elheraldo = Newspaper(nombre='El Heraldo', ciudad='Barranquilla',
                          url='https://www.elheraldo.co',
                          css_selector='h1 a')
    zonacero = Newspaper(nombre='Zonacero', ciudad='Barranquilla',
                         url='https://www.zonacero.com',
                         css_selector='div.title')
    elpilon = Newspaper(nombre='El Pilon', ciudad='',
                        url='https://elpilon.com.co',
                        css_selector='.title_note')
    eluniversal = Newspaper(nombre='El Universal', ciudad='',
                            url='https://www.eluniversal.com.co',
                            css_selector='div.headline')
    diariodelcesar = Newspaper(nombre='Diario Del Cesar', ciudad='',
                               url='https://www.diariodelcesar.com',
                               css_selector='h2.title')
    diariodelmag = Newspaper(nombre='Hoy Diario Del Magdalena', ciudad='',
                             url='https://www.hoydiariodelmagdalena.com.co',
                             css_selector='h2.title')
    elinformador = Newspaper(nombre='El Informador', ciudad='Santa Marta',
                             url='https://www.elinformador.com.co',
                             css_selector="h3[itemprop='name'] a")
    diariodelnorte = Newspaper(nombre='Diario Del Norte', ciudad='',
                               url='https://www.diariodelnorte.net',
                               css_selector='.entry-title')
    laopinion = Newspaper(nombre='La Opinión', ciudad='',
                          url='https://www.laopinion.com.co',
                          css_selector='h2 a')
    eltiempo = Newspaper(nombre='El Tiempo', ciudad='',
                         url='https://www.eltiempo.com',
                         css_selector="h2[itemprop='headline'] a")
    elcolombiano = Newspaper(nombre='El Colombiano', ciudad='',
                             url='https://www.elcolombiano.com',
                             css_selector='h3 a .priority-content')
    elespectador = Newspaper(nombre='El Espectador', ciudad='',
                             url='https://www.elespectador.com',
                             method='own_method')
    lapatria = Newspaper(nombre='La Patria', ciudad='',
                         url='https://www.lapatria.com',
                         css_selector='span.field-content')
    elpais = Newspaper(nombre='El Pais', ciudad='',
                       url='https://www.elpais.com.co',
                       css_selector='h2.title a')
    elmundo = Newspaper(nombre='El Mundo', ciudad='',
                        url='https://www.elmundo.com',
                        css_selector='a div.col-md-12 h2')
    elnuevodia = Newspaper(nombre='El Nuevo Dia', ciudad='',
                           url='http://www.elnuevodia.com.co',
                           css_selector='.field-content')
    elmanduco = Newspaper(nombre='El Manduco', ciudad='',
                          url='https://www.elmanduco.com.co',
                          css_selector='.article-title a')
    semana = Newspaper(nombre='Semana', ciudad='',
                       url='https://www.semana.com',
                       css_selector='h2.card-title')
    publimetro = Newspaper(nombre='Publimetro', ciudad='',
                           url='https://www.publimetro.co/',
                           css_selector='h2')
    pulzo = Newspaper(nombre='Pulzo', ciudad='',
                      url='https://www.pulzo.com',
                      css_selector="h2[itemprop='headline']")
    larepublica = Newspaper(nombre='La Republica', ciudad='',
                            url='https://www.larepublica.co',
                            css_selector='.agriculturaSect, .economiaSect, .globoeconomiaSect, .empresasSect, '
                                         '.ocioSect, .actualidadSect, .consumidorSect, .finanzasSect, '
                                         '.internet-economySect, .ganaderiaSect, .climaSect, .caja-fuerteSect')

    newspapers_list = [elheraldo, zonacero, elpilon, eluniversal,
                       diariodelcesar, elinformador, diariodelmag, diariodelnorte,
                       laopinion, eltiempo, elcolombiano, lapatria,
                       elpais, elmundo, elnuevodia, elmanduco, semana,
                       publimetro, pulzo, larepublica, elespectador]

    # publimetro.get_news()
    # publimetro.print_news()
    scrap = Scrapping_newspapers()
    scrap.get_all_news(newspapers_list, export='csv')
    # analisis = Explore()
    # analisis.tk()
