#!/bin/bash

[ -e ${HOME}/tutorial/solution/ptf/lib ] &&
    [ ! -e lib ] &&
    ln -s ${HOME}/tutorial/solution/ptf/lib lib

SETUP_FILE=./setup.py
if test -f "$SETUP_FILE"; then
    sudo python3 setup.py install
fi
