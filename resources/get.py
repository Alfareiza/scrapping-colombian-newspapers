import string
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import matplotlib.pyplot as plt


def url_analyse(url):
    """
    Receive a url and return only the domain
    :param url: ex: www.bbc.uk
    :return:    bbc
    """
    newurl = url[url.index('www') + 4::]
    newurl = newurl.split('.')
    return newurl[0]


def get_html_site(url):
    """
    Receive an url and return a contend parsed according BeautifulSoup
    :param url: ex: https://www.colombiannews.com.co:
    :return:        <!DOCTYPE html><body>....
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def clean_str_new(str):
    """
    Make some treatments on every string news
    :param str:
    :return:
    """
    str = str.lstrip(' ')
    str = str.replace('  ', '')
    str = str.replace('\n', '')
    str = str.replace('\t', '')
    return str


def generate_csv(news, links, url):
    """
    This program receive two lists: news and links, also a str with url and then generate a csv
    :param  news:['text of first new', 'text of second new', 'text of third new']
            links: ['http://wwww.colombiannew.com/text-of-first-new','http://wwww.colombiannew.com/text-of-second-new,
                    'http://wwww.colombiannew.com/text-of-third-new']
            url: 'http://wwww.colombiannew.com'
    :return: csv organized into dataframe with two columns (1-text of new, 2-link of new)
    """
    df = pd.DataFrame({'Noticias ': news, 'Links': links}, index=range(1, len(news) + 1))
    df.to_csv(f'{url_analyse(url)}.csv', index=range(1, len(news) + 1))
    print(df)


DATA = ''


def unifyresults(*tuplas):
    """
    Receive info from newsletter and unify them
    :param tuplas:
    :return: Nothing, only generate a dataframe with two columns, column[0]->News and column[1]->Links
    """
    news = []
    links = []
    for tupla in tuplas:
        for n in tupla[0]:
            news.append(n)
        for l in tupla[1]:
            links.append(l)
    df = pd.DataFrame({'Noticias ': news, 'Links': links}, index=range(1, len(news) + 1))
    df.to_csv('all_news.csv', index=range(1, len(news) + 1))
    print(df)
    a = ''
    for str in news:
        a += str.lower() + ' '
    DATA = a
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
