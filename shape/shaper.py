

class Shaper(object):

    def __init__(self, shape_data, apply_shape=None):
        self._shape_data = shape_data
        self._shapes = {row[0]: 50 for row in shape_data}
        self.apply_shape = apply_shape

    @property
    def shapes(self):
        return self._shapes

    @property
    def joints(self):
        return tuple(set(row[1] for row in self._shape_data))

    @property
    def _coefdicts(self):
        props_jnts = list(set(tuple([r[0], r[1]]) for r in self._shape_data))
        props_jnts.sort()
        return [[pj[0], pj[1], {r[2]: tuple(float(v) for v in r[3:])
                                for r in self._shape_data if (r[0], r[1]) == pj}] for pj in props_jnts]

    def getTransforms(self):

        vals = [r[0:2] + [self._xform(self.shapes[r[0]]/50.0 - 1, r[2])]
                for r in self._coefdicts]

        xfdict = dict()
        for r in vals:
            _, joint, xforms = r
            if joint not in xfdict:
                xfdict[joint] = xforms
            else:
                currxforms = xfdict[joint]
                for xf, val in xforms.items():
                    if xf.startswith('s'):
                        xfdict[joint][xf] = currxforms.get(xf, 1)*val
                    else:
                        xfdict[joint][xf] = currxforms.get(xf, 0) + val

        return xfdict

    def setShape(self, prop, val):
        if prop in self._shapes:
            self._shapes[prop] = val
            if self.apply_shape:
                self.apply_shape(self.getTransforms())

    def setShapes(self, prop_dict):
        for prop, val in prop_dict.items():
            self.setShape(prop, val)

    def _xform(self, val, coef_dict):
        return {k: self._f(val, v) for k, v in coef_dict.items()}

    def _f(self, val, coefs):
        idx = 0 if val < 0 else 3
        c = coefs[idx: idx+3]
        return sum(c[i]*val**i for i in range(3))
