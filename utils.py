from typing import Dict, List


def diff(l1: list, l2: list) -> list:
    """ compute the symmetric difference of two lists"""
    return [i for i in l1 + l2 if i not in l1 or i not in l2]


def as_dict(obj):
    """ returns class object as dict """
    return {c: getattr(obj, c) for c in dir(obj) if not c.startswith('_') and not c == 'metadata' and not c == 'registry'}


def dict_are_same(d1: Dict, d2: Dict):
    """ returns true if two dicts are the same """
    for k, v in list(d1.items()) + list(d2.items()):
        if k not in d2 or k not in d1:
            return False
        if d2[k] != v or d1[k] != v:
            return False
    return True


def dict_in_list(d: Dict, l: List[Dict]):
    """ returns true if dict is in list """
    # print(f'searching for {d} in {l}')
    for i in l:
        if dict_are_same(d, i):
            return True
    return False
