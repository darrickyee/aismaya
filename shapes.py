import pymel.core as pm

# IMPORT FITSKELETON

MAP = {'Root_M': 'cf_J_Kosi02',
       'Hip': 'cf_J_LegUp00',
       'Knee': 'cf_J_LegLow01',
       'Ankle': 'cf_J_Foot01',
       'Toes': 'cf_J_Toes01',
       'Spine1_M': 'cf_J_Hips',
       'Spine2_M': 'cf_J_Spine02',
       'Chest_M': 'cf_J_Spine03',
       'Scapula': 'cf_J_Shoulder',
       'Shoulder': 'cf_J_ArmUp00',
       'Elbow': 'cf_J_ArmLow01',
       'Wrist': 'cf_J_Hand',
       'PinkyFinger1': 'cf_J_Hand_Little01',
       'PinkyFinger2': 'cf_J_Hand_Little02',
       'PinkyFinger3': 'cf_J_Hand_Little03',
       'RingFinger1': 'cf_J_Hand_Ring01',
       'RingFinger2': 'cf_J_Hand_Ring02',
       'RingFinger3': 'cf_J_Hand_Ring03',
       'IndexFinger1': 'cf_J_Hand_Index01',
       'IndexFinger2': 'cf_J_Hand_Index02',
       'IndexFinger3': 'cf_J_Hand_Index03',
       'ThumbFinger1': 'cf_J_Hand_Thumb01',
       'ThumbFinger2': 'cf_J_Hand_Thumb02',
       'ThumbFinger3': 'cf_J_Hand_Thumb03',
       'MiddleFinger1': 'cf_J_Hand_Middle01',
       'MiddleFinger2': 'cf_J_Hand_Middle02',
       'MiddleFinger3': 'cf_J_Hand_Middle03',
       'Neck_M': 'cf_J_Neck',
       'Head_M': 'cf_J_Head',
       'Eye': 'cf_J_look'}

pm.ls('FitSkeleton')[0].fitSkeletonTemplate.set('bipedGame')

for src, tgt in MAP.items():
    if src.endswith('_M'):
        src = src[:-2]
    else:
        tgt += '_R'
        
    pcp = True
    if any(s in src for s in ('Finger3', 'Eye', 'Toes', 'Jaw')):
        pcp = False
        
    pm.move(src, pm.ls(tgt)[0].getTranslation(space='world'), pcp=pcp)

# BUILD SKELETON

for src, tgt in MAP.items():
    suff = [''] if src.endswith('_M') else ['_L', '_R']
    for s in suff:
        pm.orientConstraint(src+s, tgt+s, mo=True)

off = pm.createNode('transform', n='ais_HipOffset')
off.setTransformation(pm.ls('cf_J_Hips')[0].getMatrix(ws=True))
pm.parentConstraint('Root_M', off, mo=True)
pm.pointConstraint(off, 'cf_J_Hips')

CTRLMAP = {
    'IKLeg': 'ctrl_ikleg',
    'PoleLeg': 'ctrl_poleleg',
    'IKArm': 'ctrl_ikarm',
    'PoleArm': 'ctrl_polearm'
}

for src, tgt in CTRLMAP.items():
    suff = [''] if src.endswith('_M') else ['_L', '_R']
    for s in suff:
        pm.parentConstraint(src+s, tgt+s)
        
for side in '_L', '_R':
    for limb in 'arm', 'leg':
        for t in 'ik', 'pole':
            jnt = pm.createNode('joint', n='ctrl_'+t+limb+side)
            jnt.setParent('cf_J_Root')