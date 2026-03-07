import fontforge
import re


SCANCTRL_511 = b'\xb8\x01\xff\x85'
SCANTYPE_4 = b'\xb0\x04\x8d'
SMART_DROPOUT_SNIPPET = SCANCTRL_511 + SCANTYPE_4


__all__ = [
    'activateSmartDropout',
    'isSmartDropoutActive',
]


def isSmartDropoutActive(font: fontforge.font) -> bool:
    """Check if smart dropout is already activated for the font

    :param font: Fontforge font object
    :type font: fontforge.font
    :return: ``True`` if already active, ``False`` otherwise
    :rtype: bool
    """
    currentPrep = font.getTableData('prep') or b''
    if SMART_DROPOUT_SNIPPET not in currentPrep:
        return False
    else:
        revPrep = currentPrep[::-1]
        afterSnippet = (revPrep[:revPrep.find(SMART_DROPOUT_SNIPPET[::-1])])[::-1]
        if re.search(b'\xb0[^\x04]\x8d', afterSnippet):
            return False
        elif re.search(b'\xb8([^\x01].|.[^\xff])\x85', afterSnippet):
            return False
        else:
            return True


def activateSmartDropout(font: fontforge.font):
    """Activates smart dropout for the font

    This function appends the following snippet into ``prep`` table:
    ``0xb8 0x01 0xff 0x85 0xb0 0x04 0x8d`` in bytecode, or
    ``PUSHW 511 SCANCTRL PUSHB 4 SCANTYPE`` in mnemonics.
    If that is already in, does nothing.

    :param font: Fontforge font object
    :type font: fontforge.font
    """
    if not isSmartDropoutActive(font):
        currentPrep = font.getTableData('prep') or b''
        font.setTableData('prep', currentPrep + SMART_DROPOUT_SNIPPET)
