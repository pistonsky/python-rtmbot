def fast_urlencode(_dict):
    return '&'.join([k + '=' + str(v) for k, v in _dict.items()])
