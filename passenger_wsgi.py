import sys, os

INTERP = "/home/trommelkreis_v2/opt/python-3.7.7/bin/python3"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

import trommelkreis

application = trommelkreis.app
