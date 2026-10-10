import fontforge
from fontTools import ttLib

from . import config, utils
from .utils import isFixedPitch, fixedPitchWidth


def _fixOs2XAvgCharWidth_ttf(font: fontforge.font, target: str):
    with ttLib.TTFont(target) as ttf:
        assert (pitch := fixedPitchWidth(font)) is not None
        ttf['OS/2'].xAvgCharWidth = pitch
        ttf.save(target)


def fixOs2XAvgCharWidth(font: fontforge.font, target: str):
    if isFixedPitch(font):
        if (
            utils.checkExtension(target, ['.ttf', '.otf']) and
            config.config['hooks']['OS/2']['xAvgCharWidth']['ttf']  # pyright: ignore[reportIndexIssue]
        ):
            _fixOs2XAvgCharWidth_ttf(font, target)
