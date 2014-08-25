from dbg import dbg

def sniff_types(s, cols):
    ret = []

    def to_int(s):
        try:
            return int(s)
        except ValueError as ve:
            return None
    
    def to_float(s):
        try:
            return float(s)
        except ValueError as ve:
            return None
    
    def to_date(s):
        import dateutil.parser
        try:
            return dateutil.parser.parse(s)
        except TypeError as te:
            return None
    
    class eno(object):
        def __init__(self):
            pass
        
        def res(self):
            # this is the conservative choice
            if self.s >= max(self.i, self.f, self.d):
                return 'TEXT'
            elif self.i > max(self.s, self.f, self.d):
                return 'INTEGER'
            elif self.f > max(self.s, self.i, self.d):
                return 'REAL'
            elif self.d > max(self.s, self.i, self.f):
                # return 'DATE'
                return 'TEXT'
            else:
                return 'TEXT'
    
    for idx, c in enumerate(cols):
        vv = eno()
        vv.i, vv.f, vv.d, vv.s = 0, 0, 0, 0
        
        vvww = {
            'i': 0,
            'f': 0,
            'd': 0,
            's': 0
        }
        for jdx, val in enumerate(s.col(idx)):
            v = s.cell(jdx, idx).value
            if to_int(v):
                vv.i += 1
            elif to_float(v):
                vv.f += 1
            elif to_date(v):
                vv.d += 1
            else:
                vv.s += 1
        
        dbg("I think col %s (%d) is type %s" % (c, idx, vv.res()))
        ret.append(vv.res())
    
    return zip(cols, ret)

