#!/bin/bash
# NOTE: Changes to this script will only propagate on the 2nd push after change.
# This is because the branch with the new script is checked out by the previous script...

BRANCH="dh-jango"
PYTHON="/home/trommelkreis_v2/opt/python-3.7.7/bin/python3"
BASE_DIR="/home/trommelkreis_v2/www"
MANAGE="${BASE_DIR}/manage.py"

printf "Checking out branch %s to ~/www/...\n" $BRANCH
# git --work-tree=/home/trommelkreis_v2/www --git-dir=/home/trommelkreis_v2/web.git checkout -f $BRANCH

# TODO: Using without explicit branch to avoid pathspec error:
git --work-tree=$BASE_DIR --git-dir=/home/trommelkreis_v2/web.git checkout -f

printf "Updating npm dependencies...\n"
npm install --prefix $BASE_DIR

if test -f $MANAGE; then
    printf "Collecting static files...\n"
    $PYTHON $MANAGE collectstatic --no-input
    printf "Migrating database...\n"
    $PYTHON $MANAGE migrate --no-input
fi

printf "Restarting server...\n"
touch /home/trommelkreis_v2/www/tmp/restart.txt

printf "Done\n"
