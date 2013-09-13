#!/bin/bash

function fail {
    echo -e "\033[31m->" $1 "\033[0m"
}

function info {
    echo -e "\033[32m-->" $1 "\033[0m"
}

# Only verify staged code
git stash -q --keep-index

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../.."

# Run tests
info "running tests"
nosetests
CODE=$?

if [[ $CODE -ne 0 ]] 
then
    fail "aborting commit: there are failing tests"
else
    # Run flake8 to check for code problems
    info "checking for code smells"
    flake8 *.py
fi

# Put back un-staged code
git stash pop -q

# exit with status code from tests
exit $CODE
