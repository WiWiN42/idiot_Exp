

def check_dic(dic):
    """Check whether a python dictionary nested more than tree layers.

    Args:
        dic: python dictionary to check

    Returns:
        state: bool indicates the result of checking
    """
    state = False
    for top_k, top_v in dic.items():
        if isinstance(top_v, (dict)):
            for k, v in top_v.item():
                if isinstance(v, (dict)):
                    state = True
    return state