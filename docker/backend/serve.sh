while true; do
    python3 -m python.io_atomgroup.soccer.manage collectstatic --noinput;
    mkdir -p /app/tmp/backend/ipython
    ln -sf /app/tmp/backend/ipython ~/.ipython
    ipython3 profile create
    ln -sf /app/docker/backend/ipython_config.py ~/.ipython/profile_default/ipython_config.py
    gunicorn \
        --reload \
        python.io_atomgroup.soccer.asgi \
        -b 0.0.0.0 \
        --worker-class uvicorn.workers.UvicornWorker;
done
