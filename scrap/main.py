import logging.config
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from typing import List

import pandas as pd
from resources import get
import requests

TIMEOUT = 20
DONT_INCLUDE = ['sesión', 'ANUNCIOS', 'registro', 'En video', 'SUSCRÍBETE', '...', '#ENVIDEO',
                'EN VÍDEO', 'Video:', 'Agenda tu cita', 'Buscas casa']


logging.config.fileConfig(Path(__file__).parent / 'setup_log.conf')

# logging.config.fileConfig('setup_log.conf')
# logger = logging.getLogger('root')
logger = logging.getLogger('chardet.charsetprober')
logger.setLevel(logging.INFO)


class Newspaper:
    def __init__(self, nombre, ciudad, url, css_selector, method, ref='', news=[], delta_response=0):
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
        Analiza el metodo de captura del objeto y retorna una lista de tuplas donde [0] es el texto y [1] es la notícia.
        :return: lista of tuplas
        """
        response = self.request_to_newspaper_site()
        if response:
            self.update_deltaresponse(response.elapsed.total_seconds())
            if self.method == 'css_selector':
                news_captured = get.gettin_news_by_selector(self.css_selector, response)
                if news_captured:
                    for i, new_captured in enumerate(news_captured, 1):
                        new = (
                            get.clean_text(new_captured.get_text(strip=True)), get.enlace(new_captured, self.url))
                        if self.validate_new(new):
                            self.news.append(new)
                    logger.info(
                        "{0} - {1}s, {2} noticias.".format(self.nombre, round(self.delta_response, 1),
                                                           self.get_qty_news()))
                    return self.news
            elif self.method == 'own_method':
                news_captured = eval(f"self.{self.ref}_get_news({response.content})")
                if news_captured:
                    for new_captured in news_captured:
                        txt, link = new_captured
                        new = (get.clean_text(txt), get.absolute_link(link, self.url))
                        if self.validate_new(new):
                            self.news.append(new)
                    logger.info(
                        "{0} - {1}s, {2} noticias.".format(self.nombre, self.delta_response, self.get_qty_news()))
                    return self.news
        else:
            pass

    def validate_new(self, new):
        """
        Valida que cada noticia cumpla con ciertos criterios para poder ser almacenada en self.news.
        :param new: tuple: ('texto de la noticia', 'https://site.com/texto-de-la-noticia')
        :return: True o False
        """
        txt, link = new
        ultima_noticia = ''
        if self.get_qty_news() > 0:
            ultima_noticia = self.news[-1]

        if not any((True for x in DONT_INCLUDE if x in txt)) and (
                170 > len(txt) > 30) and link and txt not in ultima_noticia:
            return True
        else:
            return False

    def request_to_newspaper_site(self):
        """
        Principal request para el site del periodico.
        :return: response
        """
        try:
            return requests.get(self.url, timeout=TIMEOUT)
        except requests.exceptions.ConnectionError as e:
            logger.warning(f'Unreacheable info from {self.url} > {e}')
            return False
        except requests.exceptions.ReadTimeout as e:
            logger.warning(f'Unreacheable info from {self.url} (Read timed out)')
            return False

    def get_qty_news(self):
        """
        Calcula a cantidad total de noticias que el periodico posee.
        :return:
        """
        return len(self.news)

    def elespectador_get_news(self, response):
        """
        Método único de "elespectador" para buscar sus noticias en el json que el html posee.
        :param response: content of request
        :return: list of news
        """
        return get.gettin_news_by_findall(response)

    def print_news(self):
        """
        Consulta el atributo self.news : list de tuples, enumera e imprime las noticias en consola.
        :return:
        """
        if self.get_qty_news() > 0:
            for i, new in enumerate(self.news, start=1):
                txt, link = new
                print(i, txt, link)
        else:
            print('No hay noticias capturadas para \"{}\".'.format(self.nombre.capitalize()))

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
        if export == 'csv':
            self.generate_csv(todas_noticias)
        elif export == 'xml':
            self.generate_xml(todas_noticias)
        elif export == 'json':
            self.generate_json(todas_noticias)

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
        if news_of_newspapers:
            self.create_dataframe(news_of_newspapers).to_csv('all_news.csv')
        else:
            print("No hay noticias.")

        if os.path.isfile('all_news.csv'):
            logger.info("{0} Periodicos, Total de Noticias: {1}, Tiempo aproximado {2}s".format(self.cant_periodicos,
                                                                                                self.total_news,
                                                                                                round(
                                                                                                    self.tiempo_total,
                                                                                                    2)))
            print("... Archivo all_news.csv generado con éxito!")

    def generate_xml(self, news_of_newspapers):
        if news_of_newspapers:
            content = get.to_xml(self.create_dataframe(news_of_newspapers))
            get.create_file('all_news.xml', content)
            print("... Archivo all_news.xml generado con éxito!")
        else:
            print("No hay noticias.")

        if os.path.isfile('all_news.xml'):
            logger.info("{0} Periodicos, Total de Noticias: {1}, Tiempo aproximado {2}s".format(self.cant_periodicos,
                                                                                                self.total_news,
                                                                                                round(self.tiempo_total,
                                                                                                      2)))

    def generate_json(self, news_of_newspapers):
        if news_of_newspapers:
            self.create_dataframe(news_of_newspapers).to_json('all_news.json', orient='records')
        else:
            print("No hay noticias.")

        if os.path.isfile('all_news.csv'):
            logger.info("{0} Periodicos, Total de Noticias: {1}, Tiempo aproximado {2}s".format(self.cant_periodicos,
                                                                                                self.total_news,
                                                                                                round(self.tiempo_total,
                                                                                                      2)))
        print("... Archivo all_news.json generado con éxito!")

    def update_cant_periodicos(self, cant):
        """
        Actualiza el atributo de cantidad de periodicos que se procesan.
        :return:
        """
        self.cant_periodicos = cant

    def update_total_news(self, cant):
        self.total_news = cant


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
    elheraldo = Newspaper(nombre='El Heraldo', ciudad='Barranquilla', url='https://www.elheraldo.co',
                          css_selector='h1 a',
                          method='css_selector')
    zonacero = Newspaper(nombre='Zonacero', ciudad='Barranquilla', url='https://www.zonacero.com',
                         css_selector='div.title',
                         method='css_selector')
    elpilon = Newspaper(nombre='El Pilon', ciudad='', url='https://elpilon.com.co',
                        css_selector='.land-see-post-title', method='css_selector')
    eluniversal = Newspaper(nombre='El Universal', ciudad='', url='https://www.eluniversal.com.co',
                            css_selector='div.headline', method='css_selector')
    diariodelcesar = Newspaper(nombre='Diario Del Cesar', ciudad='', url='https://www.diariodelcesar.com',
                               css_selector='h2.title', method='css_selector')
    hoydiariodelmagdalena = Newspaper(nombre='Hoy Diario Del Magdalena', ciudad='',
                                      url='https://www.hoydiariodelmagdalena.com.co', css_selector='h2.title',
                                      method='css_selector')
    diariodelnorte = Newspaper(nombre='Diario Del Norte', ciudad='', url='https://www.diariodelnorte.net',
                               css_selector='.entry-title', method='css_selector')
    laopinion = Newspaper(nombre='La Opinión', ciudad='', url='https://www.laopinion.com.co', css_selector='h2 a',
                          method='css_selector')
    eltiempo = Newspaper(nombre='El Tiempo', ciudad='', url='https://www.eltiempo.com',
                         css_selector="h3[itemprop='headline'] a", method='css_selector')
    elcolombiano = Newspaper(nombre='El Colombiano', ciudad='', url='https://www.elcolombiano.com',
                             css_selector='h3 a .priority-content', method='css_selector')
    elespectador = Newspaper(nombre='El Espectador', ciudad='', url='https://www.elespectador.com', css_selector='',
                             method='own_method')
    lapatria = Newspaper(nombre='La Patria', ciudad='', url='https://www.lapatria.com',
                         css_selector='span.field-content', method='css_selector')
    elpais = Newspaper(nombre='El Pais', ciudad='', url='https://www.elpais.com.co', css_selector='h2.title a',
                       method='css_selector')
    elmundo = Newspaper(nombre='El Mundo', ciudad='', url='https://www.elmundo.com', css_selector='a div.col-md-12 h2',
                        method='css_selector')
    elnuevodia = Newspaper(nombre='El Nuevo Dia', ciudad='', url='http://www.elnuevodia.com.co/nuevodia/',
                           css_selector='.field-content', method='css_selector')
    elmanduco = Newspaper(nombre='El Manduco', ciudad='', url='https://www.elmanduco.com.co',
                          css_selector='.article-title a', method='css_selector')
    semana = Newspaper(nombre='Semana', ciudad='', url='https://www.semana.com', css_selector='h2.card-title',
                       method='css_selector')
    publimetro = Newspaper(nombre='Publimetro', ciudad='', url='https://www.publimetro.co/', css_selector='h2',
                           method='css_selector')
    pulzo = Newspaper(nombre='Pulzo', ciudad='', url='https://www.pulzo.com', css_selector='a.event-warmmap',
                      method='css_selector')
    larepublica = Newspaper(nombre='La Republica', ciudad='', url='https://www.larepublica.co',
                            css_selector='.agriculturaSect, .economiaSect, .globoeconomiaSect, .empresasSect, '
                                         '.ocioSect, .actualidadSect, .consumidorSect, .finanzasSect, .internet-economySect, '
                                         '.ganaderiaSect, .climaSect, .caja-fuerteSect',
                            method='css_selector')
    newspapers_list = [elheraldo, zonacero, elpilon, eluniversal, diariodelcesar, hoydiariodelmagdalena, diariodelnorte,
                       laopinion, eltiempo, elcolombiano, lapatria, elpais, elmundo, elnuevodia,
                       elmanduco, semana, publimetro, pulzo, larepublica, elespectador]

    # publimetro.get_news()
    # publimetro.print_news()
    scrap = Scrapping_newspapers()
    scrap.get_all_news(newspapers_list, export='csv')
    # analisis = Explore()
    # analisis.tk()
