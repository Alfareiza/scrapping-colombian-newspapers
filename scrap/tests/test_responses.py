import pytest
from scrap.main import NEWSPAPERS, TIMEOUT
import responses
import requests


@pytest.mark.parametrize('urls', NEWSPAPERS)
def test_sites_availables(urls):
    request = requests.get(urls, timeout=TIMEOUT)

    # assert request.status_code == 200
    @responses.activate
    def test_my_api():
        responses.add(responses.GET, NEWSPAPERS, body=request.text)

        resp = requests.get(NEWSPAPERS)
        assert resp.status_code == 200
