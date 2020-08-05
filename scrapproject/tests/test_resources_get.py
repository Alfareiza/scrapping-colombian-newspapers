import pytest
from scrapproject.resources import get

title = '[Videos] [Video] ¿Quién En Vivo | Video |  hizo   más ruido?\n Noche de (VIDEO) cacerolazos\t(VIDEO) '

def test_text_without_remove_words():
    text_cleaned = get.clean_text(title)
    assert not '[Videos]' in text_cleaned