from .data import loadShapeData, loadPresets
from .shaper import Shaper


def loadShaper(part='body'):
    if part not in ('body', 'head'):
        raise ValueError(
            "No part named '{}' (expected 'body', 'head')".format(part))

    return Shaper(loadShapeData(part))
