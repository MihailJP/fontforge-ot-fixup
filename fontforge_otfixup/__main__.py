import fontforge
from . import smartDropout


def fontforge_plugin_init(**kw):
    fontforge.registerMenuItem(
        callback=lambda _, font: smartDropout.activateSmartDropout(font),
        enable=lambda _, font: not smartDropout.isSmartDropoutActive(font),
        context="Font",
        name="Activate smart dropout"
    )
