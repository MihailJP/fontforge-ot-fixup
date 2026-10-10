from typing import Iterable, Optional

import fontforge


def checkExtension(filename: str, extensions: Iterable[str]) -> bool:
    return any((filename.endswith(ex) for ex in extensions))


def _fixedPitchWidths(font: fontforge.font):
    return (glyph.width for glyph in font.glyphs() if 0x20 <= glyph.unicode <= 0x7e)


def isFixedPitch(font: fontforge.font) -> bool:
    """Checks if the font is intended to be fixed pitch

    This checks if U+0020 to U+007E have the same advance width.

    :param font: Fontforge font object
    :type font: fontforge.font
    :returns: ``True`` if U+0020 to U+007E have the same advance width,
        ``False`` otherwise
    :rtype: bool"""
    return len(set(_fixedPitchWidths(font))) == 1


def fixedPitchWidth(font: fontforge.font) -> Optional[int]:
    """Returns advance width of fixed pitch font

    :param font: Fontforge font object
    :type font: fontforge.font
    :returns: Advance width if ``isFixedPitch(font)`` is ``True``,
        ``None`` otherwise
    :rtype: int or None"""
    if isFixedPitch(font):
        return int(list(_fixedPitchWidths(font))[0])
    else:
        return None
