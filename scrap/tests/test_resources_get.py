from scrap.resources import get

TITLE = '[Videos] [Video] ¿Quién En Vivo | Video |  hizo   más ruido?\n Noche de (VIDEO) cacerolazos\t(VIDEO) '
NEW = {}
URL = ''


def test_text_without_removewords():
    text_cleaned = get.clean_text(TITLE)
    assert '[Videos]' not in text_cleaned
