import os

def nested_dic(dic):
    """Check whether a python dictionary nested more than tree layers.

    Args:
        dic: python dictionary to check

    Returns:
        state: bool indicates the result of checking
    """
    state = False
    for top_k, top_v in dic.items():
        if isinstance(top_v, dict):
            for k, v in top_v.item():
                if isinstance(v, dict):
                    state = True
    return state

def get_field(dic, k, required=True):
    if required:
        assert k in dic, 'expected {} to be defined in experiment'.format(k)
    return dic[k] if k in dic else None