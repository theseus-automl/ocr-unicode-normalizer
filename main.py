from pathlib import Path

from fastapi import (
    FastAPI,
    Request,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from yaml import safe_load

from ocr_unicode_normalizer.normalizer import Normalizer


def load_config() -> dict:
    with open(Path(__file__).parent / 'config.yaml', 'r', encoding='utf-8') as f:
        cfg = safe_load(f)

    for k, v in cfg['data'].items():
        if v is not None:
            cfg['data'][k] = Path(v)

    return cfg


app = FastAPI()
norm = Normalizer(**load_config()['data'])


@app.get('/normalize')
async def normalize(
    request: Request,
) -> JSONResponse:
    request = await request.json()

    if 'text' not in request:
        return JSONResponse(
            content=jsonable_encoder(
                {
                    'status': 'error',
                    'detail': 'text field is not provided',
                },
            ),
        )

    text = request.pop('text')

    try:
        result = norm.normalize(
            text,
            **request,
        )
    except Exception as err:
        resp = {
            'status': 'error',
            'detail': str(err),
        }
    else:
        resp = {
            'status': 'ok',
            'text': result,
        }

    return JSONResponse(content=jsonable_encoder(resp))
