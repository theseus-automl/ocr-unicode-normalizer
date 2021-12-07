from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_nonexistent_endpoint():
    resp = client.get(
        '/abcdef',
        json={},
    )

    assert resp.status_code == 404


def test_text_not_provided():
    resp = client.get(
        '/normalize',
        json={},
    )

    assert resp.status_code == 200
    assert resp.json() == {
        'status': 'error',
        'detail': 'text field is not provided',
    }


def test_nonexistent_language():
    resp = client.get(
        '/normalize',
        json={
            'text': 'hello world',
            'lang': 'abcdef',
        }
    )

    assert resp.status_code == 200
    assert resp.json()['status'] == 'error'


def test_nonexistent_kwargs():
    resp = client.get(
        '/normalize',
        json={
            'text': 'hello world',
            'lang': 'eng',
            'kwarg1': 'a',
        }
    )

    assert resp.status_code == 200
    assert resp.json()['status'] == 'error'


def test_normal_english():
    resp = client.get(
        '/normalize',
        json={
            'text': 'hellо wоrld',  # both "o" come from Cyrillic alphabet
            'lang': 'eng',
        }
    )

    assert resp.status_code == 200
    assert resp.json() == {
        'status': 'ok',
        'text': 'hello world',
    }


def test_normal_russian():
    resp = client.get(
        '/normalize',
        json={
            'text': 'привeт миp',  # "e" and "p" come from English alphabet
            'lang': 'rus',
        }
    )

    assert resp.status_code == 200
    assert resp.json() == {
        'status': 'ok',
        'text': 'привет мир',
    }
