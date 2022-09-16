import json
import os
import re
import string
import pandas as pd
from bs4 import BeautifulSoup, ResultSet
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import matplotlib.pyplot as plt


def gettin_news_by_selector(css_selector, response) -> ResultSet:
    """
    Esta función analiza la respuesta del request (response)
    a partir de un css selector y retorna los matchs de la página
    web en relación al css selector.
        :param css_selector: Css Selector para las noticias.
                            Ej.: 'h1 a' o 'h3[itemprop='headline'] a'
        :type css_selector: string
        :param response: Contenido del llamado previo a la url.
        :type response: bytes
        :return: Objeto iterable
        :rtype: <class 'bs4.element.ResultSet'>
    """
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.select(css_selector)


def gettin_news_by_findall(response):
    """
    Esta función busca en el último <script type=application/javascript> y convierte a json la información capturada
    :param response:
    :return: news: list de tuplas: [('noticia1', 'link-de-noticia1'), ('noticia2', 'link-de-noticia2'), ('noticia2', 'link-de-noticia2')]
    """
    soup = BeautifulSoup(response, 'html.parser')
    script = soup.find_all('script', attrs={'type': 'application/javascript'})[-1].string.strip()[133:]
    starts_from, until_to = script.index("{\"type\""), script.index(";Fusion.globalContentConfig=")
    script = json.loads(script[starts_from:until_to])
    news = []
    for x in script['content_elements']:
        new = (x['headlines']['basic'], x['canonical_url'])
        news.append(new)
    if news:
        return news
    else:
        return False


def url_analyse(url: str):
    """
    Receive a url and return only the domain
    :param url: ex: www.bbc.uk
    :return:    bbc
    >>> url_analyse('http://www.elheraldo.co')
    'elheraldo'
    >>> url_analyse('http://www.otrosite.com.co')
    'otrosite'
    >>> url_analyse('www.site.com.co')
    'site'
    """
    # newurl = url[url.index('www') + 4::]
    # newurl = newurl.split('.')
    # return newurl[0]
    return re.findall('[https?:\/\/]?(www\.)?([a-zA-Z0-9]+)+\.[\w+.]+', url)[0][-1]

def clean_text(text: str):
    """
    Elimina algunas palabras de el texto en cada notícia.
    :param text: str:
    :return: text: str
    >>> clean_text('Video En Vivo')
    ''
    >>> clean_text('Video | Video')
    ''
    >>> clean_text('EN VIVO Paro Nacional: siga las marchas')
    'Paro Nacional: siga las marchas'
    """
    removewords = ['[Video]', '  ', '\n', '\t', '(VIDEO)', '(Video)', 'En Vivo |', 'Video |', 'VIDEO |', '[Videos]',
                   'Videos', 'Video', 'Video:', 'En Vivo', 'EN VIVO', '[Fotos]']
    for i in removewords:
        text = text.replace(i, "")
    text = text.lstrip(' ').rstrip(' ')
    return text


def absolute_link(link: str, url: str):
    """
    Recibe el link capturado y si no posee el dominio lo agrega
    :param link: str: '\texto-de-la-noticia\
    :param url: str: 'https://www.site.com.co
    :return: new link :str
    >>> absolute_link('/salud/la-importancia-de-beber-agua', 'https://www.paginaweb.com')
    'https://www.paginaweb.com/salud/la-importancia-de-beber-agua'
    """
    if url_analyse(url) not in link:
        return url + link


def enlace(new, url: str):
    """
    Navega por la noticia hasta encontrar un link
    :param new: (object) con la información de la noticia.
    :param url: (str) con la url del periódico. Ej.: 'https://www.elheraldo.co'
    :return: (str) Link de la noticia, o (False) si no lo encuentra.
    """
    linkTemp = ''
    if new.find_all('a'):
        if url_analyse(url) in new.a['href']:
            linkTemp = new.a['href']
        elif not re.match('^(http|www)', new.a['href']):
            linkTemp = url + new.a['href']
    elif new.name == 'a':
        if url_analyse(url) in new['href']:
            linkTemp = new['href']
        elif not re.match('^(http|www)', new['href']):
            linkTemp = url + new['href']
    elif new.parent.name == 'a':
        if url_analyse(url) in new.parent['href'][:new.parent['href'].index('/', 2)]:
            linkTemp = new.parent['href']
        elif not re.match('^(http|www)', new.parent['href']):
            linkTemp = url + new.parent['href']
    elif new.parent.parent.name == 'a':
        if url_analyse(url) in new.parent.parent['href']:
            linkTemp = new.parent.parent['href']
        elif not re.match('^(http|www)', new.parent.parent['href']):
            linkTemp = url + new.parent.parent['href']
    else:
        return False
    return linkTemp


def create_file(filename, content):
    """
    Crear archivo a partir de un nombre y su contenido
    :param filename: str
    :param content: str
    :return:
    """
    path = os.getcwd()
    with open(f'{path}\\\\{filename}', 'w', encoding="utf-8") as fp:
        fp.write(content.strip())


def to_xml(df):
    """
    Crea xml desde un dataframe
    :param df: dataframe
    :return: str: contenido del xml
    """
    def row_xml(row):
        xml = ['<item>']
        for i, col_name in enumerate(row.index):
            xml.append('  <{0}>{1}</{0}>'.format(col_name, row.iloc[i]))
        xml.append('</item>')
        return '\n'.join(xml)

    res = '\n'.join(df.apply(row_xml, axis=1))
    return (res)


def unifyresults(*tuplas):
    """
    Recibe información del periódico y la unifica.
    :param tuplas:
    :return: Nothing, only generate a dataframe with two columns, column[0]->News and column[1]->Links
    """
    news = []
    links = []
    for tupla in tuplas:
        for new in tupla[0]:
            news.append(new)
        for link in tupla[1]:
            links.append(link)
    df = pd.DataFrame({'Noticias ': news, 'Links': links}, index=range(1, len(news) + 1))
    df.to_csv('all_news.csv', index=range(1, len(news) + 1))
    print(df)
    a = ''
    for str in news:
        a += str.lower() + ' '
    tokenized_word = word_tokenize(a)
    print(tokenized_word)

    fdist = FreqDist(tokenized_word)
    print(fdist)
    stop_words = list(stopwords.words('spanish'))
    stop_words.extend(list(string.punctuation))
    more = list('’’“‘”') + ['el', 'la', 'en', 'Los', 'casos']

    stop_words.extend(more)
    filtered_sent = []
    for w in tokenized_word:
        if w not in stop_words:
            filtered_sent.append(w)
    print("Tokenized Sentence:", tokenized_word)
    print("Filterd Sentence:", filtered_sent)

    fdist = FreqDist(filtered_sent)
    print(fdist.most_common(10))

    fdist.plot(30, cumulative=False)
    plt.show()
