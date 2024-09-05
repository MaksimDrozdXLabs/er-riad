#!/usr/bin/env python3
# vim : set filetype=python

import os

import subprocess
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.dirname(__file__),
)

os.environ['PROJECT_ROOT'] = PROJECT_ROOT

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
elif sys.argv[1] == 'drift-up':
    executable_path = os.path.join(
        PROJECT_ROOT,
        'tmp',
        'drift',
        'env3',
        'bin',
        'python3',
    )

    if not os.path.exists(executable_path):
        subprocess.check_call([
            sys.executable,
            'docker/drift/setup.py',
        ])

    subprocess.check_call([
        executable_path,
        'deps/drift-ml/python/io_atomgroup/drift/server.py',
    ])
else:
    raise NotImplementedError
