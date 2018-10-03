FST_HALF = True
SND_HALF = False

'''
Structure
{
    zone: {
        month: {
            fst_half: val,
            snd_half: val
        }
    }
}
'''
_table = {
    1: {
        11: {FST_HALF: 2, SND_HALF: 2.5},
        12: {FST_HALF: 3, SND_HALF: 3},
        1: {FST_HALF: 3, SND_HALF: 3},
        2: {FST_HALF: 3, SND_HALF: 3},
        3: {FST_HALF: 2.5, SND_HALF: 2.5},
        4: {FST_HALF: 2, SND_HALF: 1.5}
    },
    2: {
        11: {FST_HALF: 1, SND_HALF: 1.2},
        12: {FST_HALF: 1.5, SND_HALF: 2},
        1: {FST_HALF: 2, SND_HALF: 1.5},
        2: {FST_HALF: 1.5, SND_HALF: 1.5},
        3: {FST_HALF: 1.5, SND_HALF: 1.5},
        4: {FST_HALF: 1.2, SND_HALF: 1}

    },
    4: {
        11: {FST_HALF: 1, SND_HALF: 1},
        12: {FST_HALF: 1, SND_HALF: 1},
        1: {FST_HALF: 1, SND_HALF: 1},
        2: {FST_HALF: 1.2, SND_HALF: 1.2},
        3: {FST_HALF: 1.2, SND_HALF: 1.2},
        4: {FST_HALF: 1, SND_HALF: 1}

    },
    5: {
        11: {FST_HALF: 1, SND_HALF: 1},
        12: {FST_HALF: 1, SND_HALF: 1.2},
        1: {FST_HALF: 1.5, SND_HALF: 1.5},
        2: {FST_HALF: 1.5, SND_HALF: 1.5},
        3: {FST_HALF: 1.2, SND_HALF: 1.2},
        4: {FST_HALF: 1.0, SND_HALF: 1.0}

    },
    7: {
        11: {FST_HALF: 1, SND_HALF: 1.2},
        12: {FST_HALF: 2, SND_HALF: 2.5},
        1: {FST_HALF: 3, SND_HALF: 3},
        2: {FST_HALF: 3, SND_HALF: 3},
        3: {FST_HALF: 3, SND_HALF: 2.5},
        4: {FST_HALF: 1.2, SND_HALF: 1}

    },
    8: {
        11: {FST_HALF: 1, SND_HALF: 1},
        12: {FST_HALF: 1.2, SND_HALF: 1.2},
        1: {FST_HALF: 1.5, SND_HALF: 1.5},
        2: {FST_HALF: 2, SND_HALF: 2},
        3: {FST_HALF: 1.5, SND_HALF: 1.5},
        4: {FST_HALF: 1, SND_HALF: 1}

    },
    10: {
        11: {FST_HALF: 1, SND_HALF: 1},
        12: {FST_HALF: 1.2, SND_HALF: 1.5},
        1: {FST_HALF: 1.5, SND_HALF: 1.5},
        2: {FST_HALF: 2, SND_HALF: 1.5},
        3: {FST_HALF: 1.5, SND_HALF: 1.2},
        4: {FST_HALF: 1.0, SND_HALF: 1.0}

    },
    11: {
        11: {FST_HALF: 1, SND_HALF: 1},
        12: {FST_HALF: 1, SND_HALF: 1.2},
        1: {FST_HALF: 1.5, SND_HALF: 1.5},
        2: {FST_HALF: 1.5, SND_HALF: 1.5},
        3: {FST_HALF: 1.5, SND_HALF: 1},
        4: {FST_HALF: 1, SND_HALF: 1}

    },
    13: {
        11: {FST_HALF: 1, SND_HALF: 1},
        12: {FST_HALF: 1, SND_HALF: 1},
        1: {FST_HALF: 1.2, SND_HALF: 1.2},
        2: {FST_HALF: 1.2, SND_HALF: 1.2},
        3: {FST_HALF: 1, SND_HALF: 1},
        4: {FST_HALF: 1, SND_HALF: 1}

    },
    14: {
        11: {FST_HALF: 1, SND_HALF: 1},
        12: {FST_HALF: 1, SND_HALF: 1},
        1: {FST_HALF: 1, SND_HALF: 1.2},
        2: {FST_HALF: 1.5, SND_HALF: 1.5},
        3: {FST_HALF: 1.5, SND_HALF: 1.2},
        4: {FST_HALF: 1.2, SND_HALF: 1.0}

    }
}


def calculate(zone, dt, *, default=None):
    if zone not in _table:
        raise ValueError('Invalid zone: {z}'.format(z=zone))
    if dt.month not in _table[zone]:
        if default == None:
            raise ValueError('Invalid month: {m}'.format(m=dt.month))
        return default
    return _table[zone][dt.month][dt.day <= 15]
