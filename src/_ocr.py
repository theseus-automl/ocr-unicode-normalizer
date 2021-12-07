import shutil
from os import (
    environ,
    getenv,
)
from pathlib import Path
from typing import (
    Optional,
    Union,
)

import pytesseract
from PIL import Image


class OCR:
    def __init__(
        self,
        tesseract_path: Optional[Path] = None,
        tessdata_path: Optional[Path] = None,
    ) -> None:
        if not self._tessdata_exists():
            if tessdata_path is None:
                raise ValueError(
                    'unable to load tesseract data. '
                    'Make sure the TESSDATA_PREFIX environment variable is set to your "tessdata" directory '
                    'or provide tessdata_path argument'
                )

            if not tessdata_path.exists():
                raise ValueError('tesseract data directory does not exist')

            environ['TESSDATA_PREFIX'] = str(tessdata_path.resolve())

        if not self._tesseract_exists():
            if tesseract_path is None:
                raise ValueError('unable to find tesseract in PATH. Provide tesseract_path argument')

            if not tesseract_path.exists():
                raise ValueError('tesseract path does not exist')

            if not tesseract_path.is_file():
                raise ValueError('tesseract path is not a file')

            pytesseract.pytesseract.tesseract_cmd = tesseract_path.resolve()

    @staticmethod
    def recognize(
        image: Union[Image.Image, Path],
        lang: str,
        **kwargs,
    ) -> str:
        if isinstance(image, Path):
            image = Image.open(str(image))

        text = pytesseract.image_to_string(
            image,
            lang=lang,
            **kwargs,
        )

        return text

    @staticmethod
    def _tesseract_exists() -> bool:
        return shutil.which('tesseract') is not None

    @staticmethod
    def _tessdata_exists() -> bool:
        return getenv('TESSDATA_PREFIX') is not None
