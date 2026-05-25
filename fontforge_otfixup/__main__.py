import fontforge

from . import aaltFeatureHook, config, postIsFixedPitchHook, smartDropout
from fontforge_plugin_helper import addSystemHook, generationHookSetter


def fontforge_plugin_config(**kw):
    try:
        config.configInterface()
    except Exception as e:
        fontforge.postError(e.__class__.__name__, str(e))


def fontforge_plugin_init(preferences_path=None, **_):
    fontforge.registerMenuItem(
        callback=lambda _, font: smartDropout.activateSmartDropout(font),  # type: ignore
        enable=lambda _, font: not smartDropout.isSmartDropoutActive(font),  # type: ignore
        context="Font",
        name="Activate smart dropout"
    )
    config.loadConfig(preferences_path + '.toml')  # type: ignore

    def generateHook(font: fontforge.font, target: str):
        postIsFixedPitchHook.fixPostIsFixedPitch(font, target)
        aaltFeatureHook.fixAaltFeature(font, target)

    addSystemHook('newFontHook', generationHookSetter(None, generateHook))
    addSystemHook('loadFontHook', generationHookSetter(None, generateHook))
