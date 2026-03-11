import pytest
from fontforge_otfixup import utils


@pytest.mark.parametrize(('filename', 'expected'), [
    ('spam.sfd', False),
    ('spam.ttf', True),
    ('spam.otf', True),
    ('spam.ttc', False),
    ('spam.ufo', True),
])
def test_checkExtension(filename, expected):
    assert utils.checkExtension(filename, ['.ttf', '.otf', '.ufo']) == expected
