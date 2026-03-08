import fontforge
from tomlkit.toml_file import TOMLFile, TOMLDocument

_configPath = None
config = TOMLDocument()


def _makeSureItemIsInstanceOf(item: str, typeobj: type, d=config):
    from typing import Iterable

    itmHead, *itmTail = item.split('.')
    if len(itmTail) == 0:
        if itmHead in d and not isinstance(d[itmHead], typeobj):
            if issubclass(typeobj, Iterable):
                d[itmHead] = typeobj()
            else:
                d[itmHead] = typeobj(d[itmHead])
        elif itmHead not in d:
            d[itmHead] = typeobj()
    else:
        _makeSureItemIsInstanceOf(itmHead, dict, d)
        _makeSureItemIsInstanceOf('.'.join(itmTail), typeobj, d[itmHead])


def _fixTypeOfConf():
    _makeSureItemIsInstanceOf('hooks.post.isFixedPitch.ttf', bool)
    _makeSureItemIsInstanceOf('hooks.post.isFixedPitch.ufo', bool)


def loadConfig(filename: str):
    global _configPath, config
    _configPath = filename
    configFile = TOMLFile(_configPath)
    try:
        config = configFile.read()
    except FileNotFoundError:
        pass

    _fixTypeOfConf()


def saveConfig():
    configFile = TOMLFile(_configPath)
    configFile.write(config)


def configInterface():
    ans = fontforge.askMulti(
        'Configuration',
        [
            {
                'type': 'choice',
                'question': 'Fix post.isFixedPitch',
                'multiple': True,
                'checks': True,
                'tag': 'hooks.post.isFixedPitch',
                'answers': [
                    {
                        'name': 'TTF', 'tag': 'ttf',
                        'default': config['hooks']['post']['isFixedPitch']['ttf'],
                    },
                    {
                        'name': 'UFO', 'tag': 'ufo',
                        'default': config['hooks']['post']['isFixedPitch']['ufo'],
                    },
                ]
            }
        ]
    )
    if ans:
        config['hooks']['post']['isFixedPitch']['ttf'] = ('ttf' in ans['hooks.post.isFixedPitch'])
        config['hooks']['post']['isFixedPitch']['ufo'] = ('ufo' in ans['hooks.post.isFixedPitch'])
        saveConfig()
