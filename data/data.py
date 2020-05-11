import csv
import json
import os
pth = os.getcwd() + '/'


XFNAMES = ('tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz')


def loadCSV(filename):
    lst = list()
    with open(filename, 'r', encoding='utf-8-sig') as f:
        lst = [l for l in csv.reader(f)]

    return lst


def getCurves(row):
    xf_raw = dict(zip(XFNAMES, zip(*[row[i+1:i+10]
                                     for i in range(0, len(row), 10)])))
    return {k: [round(float(v), 6) for v in vals]
            for k, vals in xf_raw.items()}
    # if any(round(float(val), 6) != round(float(vals[0]), 6) for val in vals)}


def getCustomData(part='body'):
    curves = {r[0]: getCurves(r[1:])
              for r in loadCSV(pth + '{}_anmshp.csv'.format(part))}
    prows = loadCSV(pth + '{}_custom.csv'.format(part))
    custom = {tuple(r[0:2]): dict(zip(XFNAMES, [float(v)
                                                for v in r[2:]])) for r in prows}

    props = {r[0]: [row[1] for row in prows if row[0] == r[0]] for r in prows}
    prop_dict = {r: {k: v for k, v in curves.items() if k in vals}
                 for r, vals in props.items()}

    for prop, shpdict in prop_dict.items():
        for shape in shpdict:
            shpdict[shape] = {
                xf: val for xf, val in shpdict[shape].items() if custom[prop, shape][xf]}

    return prop_dict


def _curveRows(data):
    return [['{0}_{1}'.format(j, t)] + crv for prop in data.values() for j,
            x in prop.items() for t, crv in x.items()]


def _getDistinctCurves(data, curves):
    if isinstance(data, list):
        if data not in curves:
            curves.append(data)
    else:
        for k in data:
            _getDistinctCurves(data[k], curves)


def _getCurvesFromData(data):
    curves = []
    if isinstance(data, dict):
        for val in data.values():
            curves.extend(_getCurvesFromData(val))
    else:
        curves = [data]

    return curves


def _replaceCurves(data, curves, coef_map):
    return {prop: {jnt: {xf: [round(c, 8) for c in coef_map[f'c{curves.index(crv):03}']]
                         for xf, crv in data[prop][jnt].items()}
                   for jnt in data[prop]}
            for prop in data}


def _replaceJoints(data, joint_map):
    return {prop: {jnt[1]: xforms for shp, xforms in data[prop].items(
    ) for jnt in joint_map if jnt[0] == shp} for prop in data}


def getCurveList(data):
    curves = _getCurvesFromData(data)
    out = []
    for curve in curves:
        if curve not in out:
            out.append(curve)

    return out


DT_BODY = getCustomData('body')
DT_HEAD = getCustomData('head')
JNTS_HEAD = [r for r in loadCSV('head_joints.csv') if r[1]]
JNTS_BODY = [r for r in loadCSV('body_joints.csv') if r[1]]

CRVS = getCurveList({'head': DT_HEAD, 'body': DT_BODY})

# Export curve ref list
with open(pth + 'curve_list.csv', 'w', newline='') as f:
    csv.writer(f).writerows(
        [f'c{i:03}'] + [r - 360 if r > 180 else r for r in row]
        for i, row in enumerate(CRVS)
    )


# Import curve coefs
COEFS = {r[0]: [float(v) for v in r[1:]]
         for r in loadCSV(pth + 'crv_coefs.csv')}


# Export shape data table
def exportShapeData(part, data):
    with open(pth + f'ShapeData_{part}.csv', 'w', newline='') as f:
        csv.writer(f).writerows([[prop, jnt, xf, *coefs]
                                 for prop in data
                                 for jnt in data[prop]
                                 for xf, coefs in data[prop][jnt].items()])


exportShapeData('head', _replaceJoints(
    _replaceCurves(DT_HEAD, CRVS, COEFS), JNTS_HEAD))
# NEEDS MANUAL CHANGES TO JOINTS
exportShapeData('body', _replaceJoints(
    _replaceCurves(DT_BODY, CRVS, COEFS), JNTS_BODY))


def getXformValue(crv, shapeval, coefs):
    idx = 0 if shapeval < 0 else 3
    coef = coefs[crv][idx:idx+3]
    return round(coef[0] + coef[1]*shapeval + coef[2]*shapeval**2, 3)
