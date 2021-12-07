from pathlib import Path

from ocr_unicode_normalizer.normalizer import Normalizer

_CWD = Path(__file__).parents[1]
_DUMMY_PATH = _CWD / 'abcdef'


def test_nonexistent_tessdata():
    try:
        Normalizer(tessdata_path=_DUMMY_PATH)
    except Exception as err:
        assert type(err) == ValueError


def test_nonexistent_font():
    try:
        Normalizer(font_path=_DUMMY_PATH)
    except Exception as err:
        assert type(err) == OSError


def test_bad_font():
    norm = Normalizer(tessdata_path=_CWD / 'tessdata')

    try:
        norm.normalize(
            'привет мир',
            lang='eng',
        )
    except Exception as err:
        assert type(err) == RuntimeError


def test_normal_english():
    norm = Normalizer(
        tessdata_path=_CWD / 'tessdata',
        font_path=_CWD / 'font.ttf',
    )
    res = norm.normalize(
        'hellо wоrld',
        lang='eng',
    )

    assert res == 'hello world'


def test_normal_russian():
    norm = Normalizer(
        tessdata_path=_CWD / 'tessdata',
        font_path=_CWD / 'font.ttf',
    )
    res = norm.normalize(
        'привeт миp',
        lang='rus',
    )

    assert res == 'привет мир'
