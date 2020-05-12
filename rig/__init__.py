import pymel.core as pm
from .pre import _alignAs5
from .post import _constrain, _attachHips
from .data import JOINTMAP, CTRLMAP, AS5CURVES


def preBuild():
    _alignAs5(JOINTMAP)


def postBuild():
    # Apply colors
    pm.mel.eval(AS5CURVES)
    # Constrain deform joints to AS5 joints
    _constrain(JOINTMAP)
    # Hip setup
    _attachHips()
    # Constrain ik/other control joints to control curves
    _constrain(CTRLMAP, pm.parentConstraint, mo=False)
    # Set up spaces
