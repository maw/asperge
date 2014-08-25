import datetime

def dbg(msg):
    n = datetime.datetime.now()
    print("[dbg[%s {%s}]] %s" % (n.ctime(), round(n.timestamp()), msg))
