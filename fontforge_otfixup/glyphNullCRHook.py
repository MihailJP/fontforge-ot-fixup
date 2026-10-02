from copy import deepcopy
from pathlib import Path
from subprocess import run, CalledProcessError
from tempfile import TemporaryDirectory

import fontforge
from fontTools.ttLib import TTFont

from . import config, utils
from .translation import tr


class SubsetterFailed(RuntimeError):
    pass


def _run_subsetter(font: fontforge.font, target: str, tmpdir: str, outputfont: Path):
    glyphlist = Path(tmpdir, 'glyph.lst').resolve()
    with Path(tmpdir, 'glyph.lst').open('w') as gl:
        gl.writelines([g + "\n" for g in font])
    try:
        run([
            'fonttools', 'subset',
            '--notdef-glyph',
            '--notdef-outline',
            '--layout-features=*',
            '--layout-scripts=*',
            '--drop-tables=',
            '--passthrough-tables',
            '--legacy-kern',
            '--name-IDs=*',
            '--name-legacy',
            '--name-languages=*',
            '--glyph-names',
            '--legacy-cmap',
            '--symbol-cmap',
            '--no-prune-unicode-ranges',
            '--no-prune-codepage-ranges',
            '--glyphs-file=' + str(glyphlist),
            '--output-file=' + str(outputfont),
            target,
        ], check=True)
    except CalledProcessError as e:
        errmsg = tr.get('`fonttools subset` ended with error code {}.').format(e.returncode)
        fontforge.logWarning(errmsg)
        fontforge.postError(tr.get('Subprocess abnormally ends'), errmsg)
        raise SubsetterFailed()
    except FileNotFoundError:
        errmsg = tr.get('`fonttools` does not seem installed.')
        fontforge.logWarning(errmsg)
        fontforge.postError(tr.get('Fonttools not found'), errmsg)
        raise SubsetterFailed()


def _cmap_workaround(font: fontforge.font, target: str, outputfont: Path):
    redundant = [g for g in ['.null', 'nonmarkingreturn'] if g not in list(font)]
    with TTFont(target) as ttf:
        tables = deepcopy(ttf['cmap'].tables)
    for table in tables:
        table.cmap = dict((k, v) for (k, v) in table.cmap.items() if v not in redundant)
    with TTFont(outputfont) as ttf:
        ttf['cmap'].tables = tables
        ttf.save(outputfont)


def _removeNullAndNonmarkingreturn_ttf(font: fontforge.font, target: str):
    with TemporaryDirectory() as tmpdir:
        try:
            outputfont = Path(tmpdir).joinpath(Path(target).name).resolve()
            _run_subsetter(font, target, tmpdir, outputfont)
            _cmap_workaround(font, target, outputfont)
            outputfont.move(target)
        except SubsetterFailed:
            pass


def removeNullAndNonmarkingreturn(font: fontforge.font, target: str):
    if (
        utils.checkExtension(target, ['.ttf', '.otf']) and
        config.config['hooks']['glyph']['null_CR']['ttf']  # pyright: ignore[reportIndexIssue]
    ):
        _removeNullAndNonmarkingreturn_ttf(font, target)
