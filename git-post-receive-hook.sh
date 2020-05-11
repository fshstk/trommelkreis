#!/bin/sh

# Checkout current branch to ~/www/:
git --work-tree=/home/trommelkreis_v2/www --git-dir=/home/trommelkreis_v2/web.git checkout -f


# If django script exists, collect static files and migate database:
if test -f "/home/trommelkreis_v2/www/manage.py"; then
    /home/trommelkreis_v2/opt/python-3.7.7/bin/python3 /home/trommelkreis_v2/www/manage.py collectstatic --no-input
    /home/trommelkreis_v2/opt/python-3.7.7/bin/python3 /home/trommelkreis_v2/www/manage.py migrate --no-input
fi

# Restart server:
touch /home/trommelkreis_v2/www/tmp/restart.txt
echo "Server restarted."