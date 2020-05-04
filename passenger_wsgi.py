# Django version of passenger_wsgi.py
import sys, os

INTERP = "/home/trommelkreis_v2/opt/python-3.7.7/bin/python3"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + "/trommelkreis")

# Do virtualenv stuff here:
# sys.path.insert(0, cwd + "/home/trommelkreis_v2/opt/python-3.7.7/bin")
# sys.path.insert(
#     0, cwd + "/home/trommelkreis_v2/opt/python-3.7.7/lib/python3.7/site-packages/"
# )

os.environ["DJANGO_SETTINGS_MODULE"] = "trommelkreis.settings"
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
