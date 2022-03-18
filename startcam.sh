#!/bin/bash
# shellcheck disable=SC2164
cd ~/Documents/Website/Charlie-s-Fourth-Angel/CamPhish
printf "$1\n$2\n\n" | ./camphish.sh | sed $'s,\x1b\\[[0-9;]*[a-zA-Z],,g'
