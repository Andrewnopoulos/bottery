

def get_micro(value, position, size):
    retval = ((value % ( 10 ** position )) - (value % (10 ** (position - size)))) / (10 ** (position - size))
    return int(retval)
