from typing import Iterable


def checkExtension(filename: str, extensions: Iterable[str]) -> bool:
    return any((filename.endswith(ex) for ex in extensions))
