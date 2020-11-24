import sqlite3
import os

DBFILE = os.path.realpath(os.path.dirname(
    os.path.abspath(__file__))+'/../data') + '/shape.db'

HEAD_JNTS = ['cf_J_FaceRoot',
             'cf_J_FaceBase',
             'cf_J_FaceLowBase',
             'cf_J_FaceLow_s',
             'cf_J_CheekLow_L',
             'cf_J_CheekLow_R',
             'cf_J_CheekUp_L',
             'cf_J_CheekUp_R',
             'cf_J_Chin_rs',
             'cf_J_ChinTip_s',
             'cf_J_ChinLow',
             'cf_J_MouthBase_tr',
             'cf_J_MouthBase_s',
             'cf_J_MouthMove',
             'cf_J_Mouth_L',
             'cf_J_Mouth_R',
             'cf_J_MouthLow',
             'cf_J_Mouthup',
             'cf_J_MouthCavity',
             'cf_J_FaceUp_ty',
             'cf_J_EarBase_s_L',
             'cf_J_EarLow_L',
             'cf_J_EarUp_L',
             'cf_J_EarBase_s_R',
             'cf_J_EarLow_R',
             'cf_J_EarUp_R',
             'cf_J_FaceUp_tz',
             'cf_J_Eye_t_L',
             'cf_J_Eye_s_L',
             'cf_J_Eye_r_L',
             'cf_J_Eye01_L',
             'cf_J_Eye01_s_L',
             'cf_J_Eye02_L',
             'cf_J_Eye02_s_L',
             'cf_J_Eye03_L',
             'cf_J_Eye03_s_L',
             'cf_J_Eye04_L',
             'cf_J_Eye04_s_L',
             'cf_J_EyePos_rz_L',
             'cf_J_look_L',
             'cf_J_eye_rs_L',
             'cf_J_pupil_s_L',
             'cf_J_Eye_t_R',
             'cf_J_Eye_s_R',
             'cf_J_Eye_r_R',
             'cf_J_Eye01_R',
             'cf_J_Eye01_s_R',
             'cf_J_Eye02_R',
             'cf_J_Eye02_s_R',
             'cf_J_Eye03_R',
             'cf_J_Eye03_s_R',
             'cf_J_Eye04_R',
             'cf_J_Eye04_s_R',
             'cf_J_EyePos_rz_R',
             'cf_J_look_R',
             'cf_J_eye_rs_R',
             'cf_J_pupil_s_R',
             'cf_J_Mayu_L',
             'cf_J_MayuMid_s_L',
             'cf_J_MayuTip_s_L',
             'cf_J_Mayu_R',
             'cf_J_MayuMid_s_R',
             'cf_J_MayuTip_s_R',
             'cf_J_NoseBase_trs',
             'cf_J_NoseBase_s',
             'cf_J_Nose_r',
             'cf_J_Nose_t',
             'cf_J_Nose_tip',
             'cf_J_NoseWing_tx_L',
             'cf_J_NoseWing_tx_R',
             'cf_J_NoseBridge_t',
             'cf_J_NoseBridge_s',
             'cf_J_FaceRoot_s']


def _loadDbTable(dbfile, tblname):
    conn = sqlite3.connect(dbfile)
    out = list()
    try:
        with conn:
            cursor = conn.execute('SELECT * FROM {}'.format(tblname))
            out = [r for r in cursor.fetchall()]
    except sqlite3.OperationalError:
        pass

    conn.close()
    return out


def _loadPartData(curves_or_presets, part='body'):
    if part not in ('body', 'head'):
        raise ValueError(
            "Invalid part '{}'; expected 'body' or 'head'".format(part))

    return _loadDbTable(DBFILE, '{0}_{1}'.format(curves_or_presets, part))


def loadShapeData(part='body'):
    return [row for row in _loadPartData('curves', part) if any(v != 0 for v in row[3:])]


def loadPresets(part='body'):
    rows = _loadPartData('presets', part)
    return {r[0]: dict(enumerate(r[1:])) for r in rows}
