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

### In Python script

```python
import fontforge
import fontforge_otfixup

font = fontforge.open('path/to/font.sfd')
sdActive = fontforge_otfixup.isSmartDropoutActive(font)
fontforge_otfixup.activateSmartDropout(font)
```
