#!/usr/bin/env python3

import datetime
from optparse import OptionParser
import subprocess
import sys

import xlrd

from dbg import dbg

def bail(msg, err=1):
    print("%s" % (msg,))
    sys.exit(err)

def load(f, sheet=None):
    dbg("loading spreadsheet...")
    if sheet is None:
        sheet = 0

    x = xlrd.open_workbook(f)
    if type(sheet) == type('string'):
        sh = x.sheet_by_name(sheet)
    elif type(sheet) == type(1):
        sh = x.sheet_by_index(sheet)
    else:
        bail('bugger all, I dunno', err=2)
    
    dbg("spreadsheet loaded")
    return sh

def get_colnames(s, x=0):
    return [v.value for v in s.row(x)]

def setup_db(dest, cols, table):
    import sqlite3
    conn = sqlite3.connect(dest)
    
    ct0 = """CREATE TABLE %s (""" % (table,)
    ctX = ["%s %s" % (col[0], col[1]) for col in cols]
    ctN = """)"""
    
    ct = "%s %s %s" % (ct0, ", ".join(ctX), ctN)
    dbg(ct)

    c = conn.cursor()
    c.execute(ct)
    c.close()
    
    return conn

def populate_db(conn, sh, table, defn):
    c = conn.cursor()

    # first = 1 will change when we implement origin    
    first = 1

    # tmpl0_0 = """INSERT INTO %s (""" % (table,)
    tmpl0_0 = """INSERT INTO %s VALUES (""" % (table,)
    tmplA_slots = ", ".join(['?' for cell in sh.row(first)])

    tmplA_vals = []
    tmpl0_1 = """) VALUES ("""
    
    tmplB_slots = []
    tmplB_vals = []

    tmplN = """)"""

    print("%s" % (defn,))
    
    tmpl = "%s %s %s" % (tmpl0_0, tmplA_slots, tmplN)
    dbg("tmpl: %s" % (tmpl,))
    
    
    dbg("now working")

    for idx in range(first, sh.nrows):
        row = sh.row(idx)
        
        #tmplA_slots = "?"
        #tmplB_values = "?"
        vals = tuple([cell.value for cell in row])
        
        conn.execute(tmpl, vals)
        #dbg("did something")
        if idx == 0:
            continue
    conn.commit()
    

def main(args):
    p = OptionParser()
    p.add_option("-d", "--dbfile", dest="dest", default="./myspreadsheet.db",
                 help="destination file")
    p.add_option("-t", "--table", dest="table", default="main",
                 help="name of table")
    p.add_option("-p", "--port", dest="port", default=2304,
                 help="port")
    p.add_option("-o", "--origin", dest="origin", default="a,1",
                 help="the origin (not yet implemented)")
    p.add_option("-x", "--origin-x", dest="xorigin", default="a",
                 help="x origin")
    p.add_option("-y", "--origin-y", dest="yorigin", default="1",
                 help="y origin")
    p.add_option("-s", "--sheet=", dest="sheet",
                 help="file to load")
    p.add_option("-r", "--run-sqlite", dest="run",
                 help="run sqlite upon load")
    p.add_option("-w", "--start-webserver", dest="web",
                 help="start webserver upon load")

    (options, args) = p.parse_args()
    
    dbg("options: %s; args: %s" % (options, args))
    if len(args) != 1:
        bail("need exactly one non-flag argument")
    s = load(args[0])
    cols = get_colnames(s)
    print("%s" % (cols,))
    from sniffer import sniff_types
    defn = sniff_types(s, cols, fast=True)
    conn = setup_db(options.dest, defn, options.table)
    populate_db(conn, s, options.table, defn)
    dbg("database populated")
    
    if opts.web:
        subprocess.getstatusoutput("python ./web.py")
    
if __name__ == '__main__':
    sys.exit(main(sys.argv))
