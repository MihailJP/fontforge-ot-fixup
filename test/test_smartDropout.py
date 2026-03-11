import pytest
import fontforge
from fontforge_otfixup import smartDropout


@pytest.fixture
def blankFont():
    font = fontforge.font()
    yield font
    font.close()


@pytest.mark.parametrize(('bytecode', 'expected'), [
    (None, False),
    (b'\xb8\x01\xff\x85\xb0\x04\x8d', True),
    (b'\xb8\x01\xff\x85', False),
    (b'\xb0\x04\x8d', False),
    (b'\xb8\x01\xff\x85\xb0\x04\x8d\xb0\x01\x8d', False),
    (b'\xb8\x01\xff\x85\xb0\x04\x8d\xb8\x00\x00\x85', False),
])
def test_isSmartDropoutActive(blankFont, bytecode, expected):
    blankFont.setTableData('prep', bytecode)
    assert smartDropout.isSmartDropoutActive(blankFont) == expected


@pytest.mark.parametrize(('bytecode', 'expected'), [
    (None, b'\xb8\x01\xff\x85\xb0\x04\x8d'),
    (b'\xb8\x01\xff\x85\xb0\x04\x8d', b'\xb8\x01\xff\x85\xb0\x04\x8d'),
    (b'\xb8\x01\xff\x85', b'\xb8\x01\xff\x85\xb8\x01\xff\x85\xb0\x04\x8d'),
    (b'\xb0\x04\x8d', b'\xb0\x04\x8d\xb8\x01\xff\x85\xb0\x04\x8d'),
    (
        b'\xb8\x01\xff\x85\xb0\x04\x8d\xb0\x01\x8d',
        b'\xb8\x01\xff\x85\xb0\x04\x8d\xb0\x01\x8d\xb8\x01\xff\x85\xb0\x04\x8d',
    ),
    (
        b'\xb8\x01\xff\x85\xb0\x04\x8d\xb8\x00\x00\x85',
        b'\xb8\x01\xff\x85\xb0\x04\x8d\xb8\x00\x00\x85\xb8\x01\xff\x85\xb0\x04\x8d',
    ),
])
def test_activateSmartDropout(blankFont, bytecode, expected):
    blankFont.setTableData('prep', bytecode)
    smartDropout.activateSmartDropout(blankFont)
    assert blankFont.getTableData('prep') == expected
