from functools import partial
from .shape import loadShaper, loadPresets
import pymel.core as pm


def setTransforms(root, xform_dict):
    root = pm.ls(root)
    if root:
        joints = root + root[0].listRelatives(ad=True, type='joint')
        for joint in joints:
            if joint.name() in xform_dict:
                for xf, val in xform_dict[joint.name()].items():
                    # combdict = {'t': op.add, 'r': lambda x, y: y, 's': op.mul}
                    v = -val if xf in ['tx', 'ry'] else val
                    joint.attr(xf).set(v)


class AisShaper:

    def __init__(self, part='body'):
        if part not in ('body', 'head'):
            raise ValueError(
                "No part named '{}' (expected 'body', 'head')".format(part))
        self._shaper = loadShaper(part)
        self._presets = loadPresets(part)
        self._shaper.apply_shape = partial(
            setTransforms, 'cf_J_Root' if part == 'body' else 'cf_J_FaceRoot')

        self.setShape = self._shaper.setShape
        self.setShapes = self._shaper.setShapes
        self.shapes = self._shaper.shapes

    def applyPreset(self, preset):
        if preset in self._presets:
            self.setShapes(self._presets[preset])
        else:
            raise ValueError("No preset named '{}'".format(preset))

    @property
    def presets(self):
        return list(self._presets.keys())
