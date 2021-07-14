import binascii

def parse_bgcolor(bgcolor):
    if not bgcolor.startswith('#'):
        raise ValueError('A bgcolor must start with a "#"')
    return binascii.unhexlify(bgcolor[1:])

def is_bgcolor(bgcolor):
    try:
        parse_bgcolor(bgcolor)
    except Exception as e:
        return False
    else:
        return True

def rgb_to_int(tuple):
    
    rgb = tuple[0];
    rgb = (rgb << 8) + tuple[1];
    rgb = (rgb << 8) + tuple[2];

    return rgb