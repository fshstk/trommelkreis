#!/bin/bash

# find . -name '*.wav' -maxdepth 3 -exec echo '{}' \;
find . -name '*.wav' -maxdepth 3 -exec /usr/local/bin/lame -V 0 -q 0 '{}' \;
find . -name '*.wav' -maxdepth 3 -exec rm '{}' \;
