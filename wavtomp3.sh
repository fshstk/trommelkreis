#!/bin/bash

file="$1"

# find . -name '*.wav' -maxdepth 2 -exec /usr/local/bin/lame -V 0 -q 0 '{}' \;
# find . -name '*.wav' -maxdepth 2 -exec rm '{}' \;
find . -name '*.mp3' -maxdepth 2 -exec echo 'files/{}' \;
