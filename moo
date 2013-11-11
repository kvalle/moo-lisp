#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from moolisp import repl, parse_file

if len(sys.argv) > 1:
    print parse_file(sys.argv[1])
else:
    repl()
