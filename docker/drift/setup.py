import subprocess

subprocess.check_call(r'''
    mkdir -p tmp/drift/env3
    python3 -m venv --system-site-packages tmp/drift/env3
    pip3 install -r deps/drift-ml/requirements.txt
    pip3 install ipython ipdb
    pip3 install fastapi 'fastapi[standard]' uvicorn
''', shell=True,)
