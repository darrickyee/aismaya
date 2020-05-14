import pymel.core as pm


def _constrain(jnt_map, constraintFn=pm.orientConstraint, mo=True):
    constraints = []
    for src, tgt in jnt_map.items():
        sides = [''] if src.endswith('_M') else ['_L', '_R']
        for side in sides:
            constraints.append(constraintFn(src+side, tgt+side, mo=mo))

    return constraints


def _attachHips():
    offset = pm.createNode('transform', n='ais_hipsOffset')
    offset.setTransformation(pm.ls('cf_J_Hips')[0].getMatrix(ws=True))

    pm.parentConstraint('Root_M', offset, mo=True)
    pm.pointConstraint(offset, 'cf_J_Hips')
