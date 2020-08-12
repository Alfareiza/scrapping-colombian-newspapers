import pytest
import requests
from scrap.main import NEWSPAPERS, TIMEOUT
from scrap.resources import get


@pytest.mark.parametrize('urls', NEWSPAPERS)
def test_sites_availables(urls):
    request = requests.get(urls, timeout=TIMEOUT)
    assert request.status_code == 200


@pytest.mark.parametrize('urls_and_css_selectors', NEWSPAPERS)
def test_set_of_news_with_css_selector(urls_and_css_selectors):
    request = requests.get(urls_and_css_selectors, timeout=TIMEOUT)
    css_selector = NEWSPAPERS.get(urls_and_css_selectors)
    set_of_news = get.gettin_news(css_selector, request)
    assert len(set_of_news) > 0


@pytest.mark.parametrize('urls', NEWSPAPERS)
def test_domain_in_link_valid(urls):
    request = requests.get(urls, timeout=TIMEOUT)
    css_selector = NEWSPAPERS.get(urls)
    set_of_news = get.gettin_news(css_selector, request)
    link = get.link_valid(set_of_news[0], urls)
    assert get.url_analyse(urls) in link
