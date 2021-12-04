from pathlib import Path
from typing import Optional

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

    def normalize(
        self,
        text: str,
        **kwargs,
    ) -> str:
        image = self._image_factory.from_text(text)
        normalized = self._ocr.recognize(
            image,
            **kwargs,
        )

        return normalized
