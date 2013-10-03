#!/bin/sh

# bash script for running the test suite
# every time a file is changed.

# requires the python package `nose` to 
# be installed.

while inotifywait -r -e modify . ; do
    nosetests
done
