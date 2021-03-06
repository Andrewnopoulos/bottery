
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

def get_micro(value, position, size):
    retval = ((value % ( 10 ** position )) - (value % (10 ** (position - size)))) / (10 ** (position - size))
    return int(retval)
