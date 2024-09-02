import subprocess
import traceback
import time
import logging
import io
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

tasks =dict(
    juggling=lambda : subprocess.Popen(
        [
            '/usr/bin/bash',
            'run_in_docker.sh',
            '--no-listen-output'
        ],
        #stdout=subprocess.DEVNULL,
        #stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
    ),
    #ffmpeg=lambda : subprocess.Popen(
    #    [
    #        'ffmpeg', '-i',
    #        'rtmp://127.0.0.1:1935/live/app', '-vcodec:copy',
    #        'rtmp://nginx:1935/live/test',
    #    ],
    #    stdout=subprocess.DEVNULL,
    #    stderr=subprocess.DEVNULL,
    #    stdin=subprocess.DEVNULL,
    #)
)

process = dict()


restart = False

while True:
    if len(process) == 0:
        for k, v in tasks.items():
            process[k] = v()

    for k, v in process.items():
        if not v.poll() is None:
            restart = True

    if restart:
        for k, v in process.items():
            try:
                v.terminate()
                v.wait(timeout=4)
            except:
                logger.error(traceback.format_exc())
                v.kill()
        process.clear()
        restart = False

    time.sleep(1)
