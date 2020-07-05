from resources.get import *

DONT_INCLUDE = ['sesión', 'ANUNCIOS', 'registro', 'En video', 'SUSCRÍBETE']


def get_news(new, url):
    news, links = list(), list()
    for i, j in enumerate(new):
        if not any((True for x in DONT_INCLUDE if x in j.text)):
            news.append(clean_str_new(j.text))
            if j.find_all('a'):
                if url_analyse(url) in j.a['href']:
                    links.append(j.a['href'])
                else:
                    links.append(url + j.a['href'])
            elif j.name == 'a':
                if url_analyse(url) in j['href']:
                    links.append(j['href'])
                else:
                    links.append(url + j['href'])
            else:
                if j.parent['href']:
                    if url_analyse(url) in j.parent['href']:
                        links.append(j.parent['href'])
                    else:
                        links.append(url + j.parent['href'])
    return news, links


def elheraldo():
    url = 'https://www.elheraldo.co'
    soup = get_html_site(url)
    # Get news from site according class 'titulo' in any tag
    new = soup.find_all(class_=['titulo'])
    result = get_news(new, url)
    # generate_csv(news, links, url)
    return result


def zonacero():
    url = 'https://www.zonacero.com/'
    soup = get_html_site(url)
    new = soup.find_all("div", class_=['title'])
    result = get_news(new, url)
    # generate_csv(news, links, url)
    return result


def elpilon():
    url = 'https://www.elpilon.com.co'
    soup = get_html_site(url)
    new = soup.find_all(class_=['land-see-post-title'])
    result = get_news(new, url)
    # generate_csv(news, links, url)
    return result


def eluniversal():
    url = 'https://www.eluniversal.com.co'
    soup = get_html_site(url)
    new = soup.find_all("div", class_=['headline'])
    result = get_news(new, url)
    # generate_csv(news, links, url)
    return result


def diariodelcesar():
    url = 'https://www.diariodelcesar.com/'
    soup = get_html_site(url)
    new = soup.find_all("h2", class_=['title'])
    result = get_news(new, url)
    # generate_csv(news, links, url)
    return result


def diariodelmagdalena():
    url = 'https://www.hoydiariodelmagdalena.com.co/'
    soup = get_html_site(url)
    new = soup.find_all("h2", class_=['title'])
    result = get_news(new, url)
    # generate_csv(news, links, url)
    return result


def diariodelnorte():
    url = 'https://www.diariodelnorte.net/'
    soup = get_html_site(url)
    new = soup.find_all("h3", itemprop=['name'])
    result = get_news(new, url)
    # generate_csv(result[0], result[1], url)
    return result


unifyresults(elheraldo(), zonacero(), elpilon(), eluniversal(), diariodelcesar(), diariodelmagdalena(), diariodelnorte())
# print(soup.find_all.'title'.text)
# print(soup.title.get_text())
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
