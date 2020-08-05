import string
import pandas as pd
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


def clean_text(text):
    """
    Exclude some words of the text in every new
    :param text:
    :return: text
    """
    removewords = ['[Video]', '  ', '\n', '\t', '(VIDEO)', 'En Vivo |', 'Video |', '[Videos]']
    text = text.lstrip(' ')
    for i in removewords:
        text = text.replace(i, "")
    return text


def link_valid(new, url):
    linkTemp = []
    if new.find_all('a'):
        if url_analyse(url) in new.a['href']:
            linkTemp.append(new.a['href'])
        else:
            linkTemp.append(url + new.a['href'])
    elif new.name == 'a':
        if url_analyse(url) in new['href']:
            linkTemp.append(new['href'])
        else:
            linkTemp.append(url + new['href'])
    elif new.parent == 'a':
        if url_analyse(url) in new.parent['href']:
            linkTemp.append(new.parent['href'])
        else:
            linkTemp.append(url + new.parent['href'])
    elif new.parent.parent.name == 'a':
        if url_analyse(url) in new.parent.parent['href']:
            linkTemp.append(new.parent.parent['href'])
        else:
            linkTemp.append(url + new.parent.parent['href'])
    else:
        return False
    return linkTemp


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


def unifyresults(*tuplas):
    """
    Receive info from newsletter and unify them
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
