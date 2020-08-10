import pytest
import requests
from scrap.main import NEWSPAPERS, TIMEOUT
from scrap.resources import get


@pytest.mark.parametrize('urls', NEWSPAPERS)
def test_response_200(urls):
    response = requests.get(urls, timeout=TIMEOUT)
    assert response.status_code == 200


@pytest.mark.parametrize('urls_and_css_selectors', NEWSPAPERS)
def test_set_of_news_with_css_selector(urls_and_css_selectors):
    response = requests.get(urls_and_css_selectors, timeout=TIMEOUT)
    css_selector = NEWSPAPERS.get(urls_and_css_selectors)
    set_of_news = get.gettin_news(css_selector, response)
    assert len(set_of_news) > 0


@pytest.mark.parametrize('urls', NEWSPAPERS)
def test_domain_in_link_valid(urls):
    response = requests.get(urls, timeout=TIMEOUT)
    css_selector = NEWSPAPERS.get(urls)
    set_of_news = get.gettin_news(css_selector, response)
    link = get.link_valid(set_of_news[0], urls)
    assert get.url_analyse(urls) in link


if __name__ == '__main__':
    print(NEWSPAPERS)
