"""Fontforge plugin to fix issues to generated OT font"""

from .smartDropout import activateSmartDropout, isSmartDropoutActive

__all__ = [
    'activateSmartDropout',
    'isSmartDropoutActive',
]
