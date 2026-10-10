"""Fontforge plugin to fix issues to generated OT font"""

from .smartDropout import activateSmartDropout, isSmartDropoutActive
from .utils import isFixedPitch, fixedPitchWidth

__all__ = [
    # smartDropout.py
    'activateSmartDropout',
    'isSmartDropoutActive',

    # utils.py
    'isFixedPitch',
    'fixedPitchWidth',
]
