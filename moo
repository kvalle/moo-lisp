#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from moolisp.interpreter import interpret_file
from moolisp.repl import repl

if len(sys.argv) > 1:
    print interpret_file(sys.argv[1])
else:
    repl()
