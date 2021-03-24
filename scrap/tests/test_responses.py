# import pytest
import requests
# from scrap.resources import get
from vcr import VCR

vcr = VCR(
    cassette_library_dir="resources/cassettes",
    path_transformer=VCR.ensure_suffix(".yaml"),
    record_mode="once"
)

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

URLS_AND_SELECTORS = [i for i in NEWSPAPERS.items()]

url = 'http://www.elheraldo.co'


# @pytest.mark.parametrize


@vcr.use_cassette
def mocked_site(url):
    response = requests.get(url, timeout=20)
    print(response)


def test_status_code(resp):
    assert resp.status_code == 200

# @pytest.mark.parametrize('url, css_selector', [('http://www.elheraldo.co', '.titulo')])

# 1. le envío al fixture los datos para que mocke la jugada
# 2. el fixture me retorna un response
# 3. vccasete, recibe el objeto mockado y hace los asserts
