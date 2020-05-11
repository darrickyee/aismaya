import sqlite3
import os

DBFILE = os.path.realpath(os.path.dirname(
    os.path.abspath(__file__))+'/../data') + '/shape.db'


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
