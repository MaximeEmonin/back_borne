
def diff(l1: list, l2: list) -> list:
    """ compute the symmetric difference of two lists"""
    return [i for i in l1 + l2 if i not in l1 or i not in l2]


def as_dict(obj):
    """ returns class object as dict """
    return {c: getattr(obj, c) for c in dir(obj) if not c.startswith('_') and not c == 'metadata' and not c == 'registry'}