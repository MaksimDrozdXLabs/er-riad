while true; do
    # python3 -m python.io_atomgroup.soccer.manage collectstatic;
    gunicorn python.io_atomgroup.soccer.wsgi -b 0.0.0.0;
done
