ffmpeg \
  -stream_loop -1 \
  -re \
  -i tmp/static/football-v5.x264.mp4 \
  -vcodec copy \
  -f flv "rtmp://127.0.0.1:1935/live/test"
