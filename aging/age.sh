#!/bin/bash

touch /degrade

while [ -e /degrade ]; do
  dpkg --get-selections \
    | awk '$2 == "install" { print $1 }' \
    | sort -R \
    | head -n 5 \
    | xargs apt-get install --reinstall -y
  dpkg --configure -a
done
