import fontforge
from . import postIsFixedPitchHook, smartDropout
from typing import Literal, Callable


def _addGlobalHook(
    name: Literal['newFontHook', 'loadFontHook'],
    hook: Callable[[fontforge.font], None]
):
    assert isinstance(fontforge.hooks, dict)
    if name in fontforge.hooks:
        currentHook = fontforge.hooks[name]

        def chainHook(font: fontforge.font):
            currentHook(font)
            hook(font)

        fontforge.hooks[name] = chainHook
    else:
        fontforge.hooks[name] = hook


def _addFontHook(
    font: fontforge.font,
    name: Literal['generateFontPreHook', 'generateFontPostHook'],
    hook: Callable[[fontforge.font, str], None]
):
    if not isinstance(font.temporary, dict):
        font.temporary = {}
    if name in font.temporary:
        currentHook = font.temporary[name]

        def chainHook(font: fontforge.font, target: str):
            currentHook(font, target)
            hook(font, target)

        font.temporary[name] = chainHook
    else:
        font.temporary[name] = hook


def fontforge_plugin_init(**kw):
    fontforge.registerMenuItem(
        callback=lambda _, font: smartDropout.activateSmartDropout(font),
        enable=lambda _, font: not smartDropout.isSmartDropoutActive(font),
        context="Font",
        name="Activate smart dropout"
    )

    def generateHook(font: fontforge.font, target: str):
        postIsFixedPitchHook.fixPostIsFixedPitch(font, target)

    def openHook(font: fontforge.font):
        _addFontHook(font, 'generateFontPostHook', generateHook)

    _addGlobalHook('newFontHook', openHook)
    _addGlobalHook('loadFontHook', openHook)
