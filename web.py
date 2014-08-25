from optparse import OptionParser
import sqlite3
import sys

from flask import Flask
app = Flask(__name__)

@app.route('/load')
def load():
    pass

@app.route('/')
def hello_world():
    return 'Hello World!'



def main(args):
    p = OptionParser()
    p.add_option("-t", "--table", dest="table", default="main")
    p.add_option("-d", "--dbfile", dest="test", default="./myspreadsheet.db")
    p.add_option("-p", "--port", dest="port", default=2304)
    p.add_option("-b", "--background", dest="background" , default=True)
    
    (options, args) = p.parse_args()
    
    app.run()
    
    pass
    
if __name__ == '__main__':
    sys.exit(main(sys.argv))
