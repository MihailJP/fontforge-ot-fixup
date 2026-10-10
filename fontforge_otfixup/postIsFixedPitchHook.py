import fontforge
from fontTools import ttLib, ufoLib

from . import config, utils
from .utils import isFixedPitch


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
        ttf['post'].isFixedPitch = 1  # type: ignore
        ttf.save(target)


def _fixPostIsFixedPitch_ufo(font: fontforge.font, target: str):
    with ufoLib.UFOReaderWriter(target) as ufo:
        info = _ufoInfo3() if ufo.formatVersionTuple[0] >= 3 else _ufoInfo2()
        ufo.readInfo(info)
        ufo.postscriptIsFixedPitch = True  # type: ignore
        ufo.writeInfo(info)  # type: ignore


def fixPostIsFixedPitch(font: fontforge.font, target: str):
    if isFixedPitch(font):
        if (
            utils.checkExtension(target, ['.ttf', '.otf']) and
            config.config['hooks']['post']['isFixedPitch']['ttf']  # pyright: ignore[reportIndexIssue]
        ):
            _fixPostIsFixedPitch_ttf(font, target)
        elif (
            utils.checkExtension(target, ['.ufo', '.ufo2', '.ufo3']) and
            config.config['hooks']['post']['isFixedPitch']['ufo']  # pyright: ignore[reportIndexIssue]
        ):
            _fixPostIsFixedPitch_ufo(font, target)
