from pathlib import Path
from typing import Optional

from pytesseract import get_languages

from src._exceptions import UnsupportedLanguageError
from src._image_factory import ImageFactory
from src._ocr import OCR


class Normalizer:
    def __init__(
        self,
        tesseract_path: Optional[Path] = None,
        tessdata_path: Optional[Path] = None,
        font_path: Optional[Path] = None,
    ) -> None:
        self._ocr = OCR(
            tesseract_path,
            tessdata_path,
        )
        self._image_factory = ImageFactory(font_path)
        self._supported_langs = set(get_languages())

    def normalize(
        self,
        text: str,
        **kwargs,
    ) -> str:
        lang = kwargs.get(
            'lang',
            None,
        )

        if lang is None:
            raise ValueError('target language is not provided')

        if lang not in self._supported_langs:
            raise UnsupportedLanguageError(
                f'language "{lang}" is not supported by Tesseract. '
                f'Possible languages are: {", ".join(self._supported_langs)}'
            )

        image = self._image_factory.from_text(text)
        normalized = self._ocr.recognize(
            image,
            **kwargs,
        ).strip()

        return normalized
