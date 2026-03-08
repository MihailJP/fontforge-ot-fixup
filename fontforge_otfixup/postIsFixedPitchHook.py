import fontforge
from fontTools import ttLib, ufoLib
from typing import Iterable
from . import config


def _isFixedPitch(font: fontforge.font) -> bool:
    return len(
        set(
            (glyph.width for glyph in font.glyphs() if 0x20 <= glyph.unicode <= 0x7e)
        )
    ) == 1


class _ufoInfo2:
    from fontTools.ufoLib import fontInfoAttributesVersion2
    from itertools import repeat
    _data = dict(zip(list(fontInfoAttributesVersion2), repeat(None)))

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        else:
            raise AttributeError("attribute '{0}' not found".format(name))

    def __setattr__(self, name, value):
        if name in self._data:
            self._data[name] = value
        else:
            raise AttributeError("attribute '{0}' not found".format(name))


class _ufoInfo3(_ufoInfo2):
    from fontTools.ufoLib import fontInfoAttributesVersion3
    from itertools import repeat
    _data = dict(zip(list(fontInfoAttributesVersion3), repeat(None)))


def _fixPostIsFixedPitch_ttf(font: fontforge.font, target: str):
    with ttLib.TTFont(target) as ttf:
        ttf['post'].isFixedPitch = 1
        ttf.save(target)


def _fixPostIsFixedPitch_ufo(font: fontforge.font, target: str):
    with ufoLib.UFOReaderWriter(target) as ufo:
        info = _ufoInfo3() if ufo.formatVersionTuple[0] >= 3 else _ufoInfo2()
        ufo.readInfo(info)
        ufo.postscriptIsFixedPitch = True
        ufo.writeInfo(info)


def _checkExtension(filename: str, extensions: Iterable[str]) -> bool:
    return any((filename.endswith(ex) for ex in extensions))


def fixPostIsFixedPitch(font: fontforge.font, target: str):
    if _isFixedPitch(font):
        if (
            _checkExtension(target, ['.ttf', '.otf']) and
            config.config['hooks']['post']['isFixedPitch']['ttf']
        ):
            _fixPostIsFixedPitch_ttf(font, target)
        elif (
            _checkExtension(target, ['.ufo', '.ufo2', '.ufo3']) and
            config.config['hooks']['post']['isFixedPitch']['ufo']
        ):
            _fixPostIsFixedPitch_ufo(font, target)
