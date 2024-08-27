#!/usr/bin/env python3
# vim : set filetype=python

import subprocess
import sys


def c(*argv):
    return subprocess.check_call([
        'sudo',
        'docker',
        'compose',
        *argv,
    ])

def wm(*argv):
    return c(
        'exec',
        '-e',
        'TERM=xterm-256color',
        '-it',
        'web',
        'python3',
        '-m',
        'python.io_atomgroup.soccer.manage',
        *argv,
    )

if sys.argv[1] == 'c':
    c(*sys.argv[2:])
elif sys.argv[1] == 'lint':
    c('exec', '-it', 'web', 'mypy', 'python')
elif sys.argv[1] == 'wm':
    wm(*sys.argv[2:])
elif sys.argv[1] == 'wmr':
    c('exec', '-it', 'web', 'pkill', '-HUP', 'gunicorn')
else:
    raise NotImplementedError
