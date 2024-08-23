while true; do
    python3 -m python.io_atomgroup.soccer.manage collectstatic --noinput;
    ln -sf /app/docker/backend/ipython_config.py ~/.ipython/profile_default/ipython_config.py
    gunicorn \
        --reload \
        python.io_atomgroup.soccer.asgi \
        -b 0.0.0.0 \
        --worker-class uvicorn.workers.UvicornWorker;
done
