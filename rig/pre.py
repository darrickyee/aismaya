import pymel.core as pm


def _alignAs5(joint_map):
    for src, tgt in joint_map.items():
        if src.endswith('_M'):
            src = src[:-2]
        else:
            tgt += '_R'

        if pm.ls(src) and pm.ls(tgt):
            pcp = False if any(s in src for s in (
                'Finger3', 'Eye', 'Toes', 'Jaw')) else True

            pm.move(src, pm.ls(tgt)[0].getTranslation(space='world'), pcp=pcp)
