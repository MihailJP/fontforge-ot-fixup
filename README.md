Fontforge OT Fixup
==================

Fontforge_plugin to fix issues to generated OT font

Install
-------

```shell
pip3 install fontforge_ot_fixup
```

### Make sure Fontforge Python module is usable

In interactive mode of Python, run:

```python
import fontforge
```

If it raises ``ModuleNotFoundError`` exception, install Fontforge first. If
installed, make sure the build option set that the Python module gets also
installed. If already so, Python interpreter does not recognize the module
path where the required module.

```shell
export PYTHONPATH=/path/to/fontforge/python/module:$PYTHONPATH
```

Configuration
-------------

This plugin has configuration menu. Select File > Configure Plugins... > OT
fixup utility and click Configure to open.

Configuration will be stored in
`~/.config/fontforge/plugin/OT fixup utility.toml`
(for Linux.)

### Fix post.isFixedPitch

Table: `[hooks.post.isFixedPitch]`\
Keys: `ttf` and `ufo`\
Type: `bool`

Enable or disable the font generation hook (see below.) Can be configured
for each format, TTF (including OTF) and UFO.

### Fix OS/2.xAvgCharWidth

Table: `[hooks.OS/2.xAvgCharWidth]`\
Keys: `ttf`\
Type: `bool`

Enable or disable the font generation hook (see below.) Only applicable
for TTF.

### Fix 'aalt' feature

Table: `[hooks.GSUB.aalt]`\
Keys: `ufo`\
Type: `bool`

Enable or disable the font generation hook (see below.) Only applicable
for UFO.

Usage
-----

### In Fontforge GUI

This plugin adds following items into "Tools" menu:

- Activate smart dropout

#### Activate smart dropout

This appends the following bytecode into `prep` table:

```assembly
B8h    PUSHW
01FFh  511
85h    SCANCTRL
B0h    PUSHB
04h    4
8Dh    SCANTYPE
```

If already appended the menu will be disabled.

### Hooks

This plugin installs new/load font hook that installs font generation
hook. The latter automatically fixes certain issues in exported font.

#### Fix `post.isFixedPitch`

Fontforge may export with `post.isFixedPitch` = 0 even for monospace fonts.
This is because Fontforge requires all glyph **including** combining marks
have the same advance width in order to export with `post.isFixedPitch` = 1.
This is usually inappropriate.

This hook fixes the flag after normal export referring only U+0020 to U+007E.

Works when exporting TTF, OTF, or UFO.

#### Fix `OS/2.xAvgCharWidth`

For `OS/2.version` ≥ 3, `OS/2.xAvgCharWidth` is calculated from **all**
non-zero-width glyphs.
However, this causes misbehavior for CJK monospaced fonts
in certain environments. Such fonts have fullwidth (_zenkaku_) characters
as opposed to halfwidth (_hankaku_) ones which corresponds to any glyphs
in Western fonts.

This hook fixes the average width to what calculated
from only U+0020 to U+007E.
This is typically the advance width of halfwidth characters.

Works when exporting TTF or OTF. Monospaced fonts only.

#### Fix `aalt` feature

Fontforge can export UFO but lacks special handling for `aalt` feature.
This may result an invalid feature file (*.ufo/feature.fea); it is that
`aalt` cannot contain `script` or `language` instructions.

This hook fixes `aalt` feature, or adds it if it does not exist. Existing
lookups in `aalt` features will be included as `aalt`-only ones.

Works only when exporting UFO.

### In Python script

```python
import fontforge
import fontforge_otfixup

font = fontforge.open('path/to/font.sfd')
sdActive = fontforge_otfixup.isSmartDropoutActive(font)
fontforge_otfixup.activateSmartDropout(font)
```
