while true; do
    # python3 -m python.io_atomgroup.soccer.manage collectstatic;
    gunicorn \
        --reload \
        python.io_atomgroup.soccer.asgi \
        -b 0.0.0.0 \
        --worker-class uvicorn.workers.UvicornWorker;
done
