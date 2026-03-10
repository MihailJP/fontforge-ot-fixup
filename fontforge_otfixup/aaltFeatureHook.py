import fontforge
import re
from . import config, utils
from pathlib import Path


def _aaltExists(font: fontforge.font) -> bool:
    tags = []
    for i in font.gsub_lookups:
        for j in font.getLookupInfo(i)[2]:
            tags.append(j[0])
    return 'aalt' in tags


def _allGSUBTags(font: fontforge.font) -> set[str]:
    tags = []
    for i in font.gsub_lookups:
        for j in font.getLookupInfo(i)[2]:
            tags.append(j[0])
    return set(tags) - set(['aalt'])  # do not include 'aalt' itself


def _fixAaltFeature_ufo(font: fontforge.font, target: str):
    with open(Path(target, "features.fea")) as featFile:
        feat = featFile.read()

    if _aaltExists(font) or _allGSUBTags(font):
        existingAalt = ''
        aaltPattern = r'(?s)\bfeature\s+aalt\s*\{\n?(.*)\}\s*aalt\*;\s*'
        featPosPattern = r'(?=feature\s+\w{1,4}\s*\{)'
        removeFromAaltPattern = r'(?m)^\s*(script|language)\s+.*?;\s*'
        if result := re.search(aaltPattern, feat):
            existingAalt = re.sub(removeFromAaltPattern, "", result[1])
            feat = re.sub(aaltPattern, "", feat)
        aaltInclude = "".join(['  feature ' + x + ';\n' for x in sorted(_allGSUBTags(font))])
        newAalt = ''
        if aaltInclude or existingAalt:
            newAalt = "feature aalt {\n" + aaltInclude + existingAalt + "} aalt;\n\n"
        feat = re.sub(featPosPattern, newAalt, feat, count=1)

    with open(Path(target, "features.fea"), "w") as featFile:
        featFile.write(feat)


def fixAaltFeature(font: fontforge.font, target: str):
    if (
        utils.checkExtension(target, ['.ufo', '.ufo2', '.ufo3']) and
        config.config['hooks']['GSUB']['aalt']['ufo']
    ):
        _fixAaltFeature_ufo(font, target)
