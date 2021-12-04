from pathlib import Path
from typing import (
    List,
    Optional,
)

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)

_REPLACEMENT_CHARACTER = '\uFFFD'
_NEWLINE_REPLACEMENT_STRING = f' {_REPLACEMENT_CHARACTER} '

_WHITE = '#FFF'
_BLACK = '#000'


class ImageFactory:
    def __init__(
        self,
        font_path: Optional[Path] = None,
    ) -> None:
        self._font = ImageFont.load_default() if font_path is None else ImageFont.truetype(str(font_path), 15)
        self._left_padding = 3
        self._right_padding = 3
        self._width = 200
        self._line_start = self._width - self._right_padding - self._left_padding

    def from_text(
        self,
        text: str,
    ) -> Image.Image:
        lines = self._prepare_text(text)

        line_height = self._font.getsize(text)[1]
        img_height = line_height * (len(lines) + 1)

        img = Image.new(
            'RGB',
            (
                self._width,
                img_height,
            ),
            _WHITE,
        )
        draw = ImageDraw.Draw(img)

        for i, line in enumerate(lines):
            draw.text(
                (
                    self._left_padding,
                    i * line_height,
                ),
                line,
                _BLACK,
                font=self._font,
            )

        return img

    def _prepare_text(
        self,
        text: str,
    ) -> List[str]:
        text = text.replace(
            '\n',
            _NEWLINE_REPLACEMENT_STRING,
        )

        lines = []
        line = ''

        for word in text.split():
            if word == _REPLACEMENT_CHARACTER:  # Blank line
                lines.append(line[1:])  # Slice the white space in the beginning of the line
                line = ''
                lines.append('')  # Blank line
            else:
                try:
                    is_fit = self._font.getsize(line + ' ' + word)[0] <= self._line_start
                except UnicodeEncodeError:
                    raise RuntimeError('your font does not support Unicode. Consider choosing another one')

                if is_fit:
                    line += f' {word}'
                else:
                    lines.append(line[1:])  # Slice the white space in the beginning of the line
                    line = ''

                    # TODO: handle too long words at this point
                    line += f' {word}'  # For now, assume no word alone can exceed the line width

        if len(line):
            lines.append(line[1:])  # Add the last line

        return lines
