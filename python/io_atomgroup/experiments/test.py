import numpy as np
import asyncio
import json
import sys
import numpy
import functools
import time
import threading
import datetime
import cv2 as cv
import cv2
import fastapi
import fastapi.middleware
import fastapi.responses
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from typing import (Optional, Any,)

class Test:
    def __init__(
        self,
        video_args: Optional[list[Any]] = None,
        url_prefix: Optional[str] = None,
        need_cors: Optional[bool] = None,
        padding: Optional[Any] = None,
        feed_fps: Optional[int] = None,
        frame_width: Optional[int] = None,
        frame_height: Optional[int] = None,
        timestamp_font_size: Optional[int | float] = None,
        timestamp_offset: Optional[Any] = None,
    ):
        self.frame_width = frame_width
        self.frame_height = frame_height

        if need_cors is None:
            need_cors = False


        self.need_cors = need_cors

        if timestamp_font_size is None:
            timestamp_font_size = 0.5

        self.timestamp_font_size = timestamp_font_size

        if feed_fps is None:
            feed_fps = 60

        if url_prefix is None:
            url_prefix = '/juggling',

        self.timestamp_offset = timestamp_offset
        self.feed_fps = feed_fps
        self.padding = padding
        self.url_prefix = url_prefix

        if video_args is None:
            if sys.platform == 'linux':
                video_args = [
                    0,
                    cv2.CAP_V4L2
                ]
            elif sys.platform == 'darwin':
                self.camera_check()
                video_args = [
                    0,
                ]
            else:
                raise NotImplementedError

        self.video_args = video_args
        self.state = dict(
            frame=None,
            workers=dict(),
        )

    def camera_check(self):
        if sys.platform == 'linux':
            raise NotImplementedError
        elif sys.platform == 'darwin':
            cap = None
            try:
                cap = cv2.VideoCapture(1)
            finally:
                if not cap is None and cap.isOpened():
                    cap.release()
        else:
            raise NotImplementedError

    def camera_worker(self):
        state = self.state
        cap = self.cap
        lock = self.lock

        # cv.namedWindow('frame', cv.WINDOW_GUI_NORMAL | cv.WINDOW_AUTOSIZE)
        try:
            if not cap.isOpened():
                print("Cannot open camera")
            while True:
                # Capture frame-by-frame
                ret, frame = cap.read()

                if frame is None:
                    time.sleep(0.1)
                    continue

                if not self.timestamp_offset is None:
                    cv2.putText(
                        frame,
                        f"{datetime.datetime.now().isoformat()}",
                        self.timestamp_offset,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        self.timestamp_font_size,
                        (0, 255, 0), 2
                    )
                # print('\r%s', frame.shape, end='')
                # if frame is read correctly ret is True
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                # Our operations on the frame come here
                #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                gray = frame

                if not self.padding is None:
                    frame2 = numpy.pad(
                        frame,
                        [
                            (
                                (self.padding['height'] - frame.shape[0]) // 2,
                            ) * 2,
                            (
                                (self.padding['width'] - frame.shape[1]) // 2,
                            ) * 2,
                            (0,0)
                        ]
                    )[:, -self.padding['crop_height_from_bottom']:, :]
                else:
                    frame2 = frame
                #frame2 = cv2.resize(
                #    frame,
                #    #(1280 // 2, 720 // 2),
                #    (1280, 720),
                #    interpolation=cv2.INTER_AREA
                #)

                with lock:
                    with self.state['frame_cv']:
                        state['frame'] = frame2
                        self.state['frame_cv'].notify()
                    # state['frame'] = frame

                # Display the resulting frame
                # cv.imshow('frame', gray)
                # if cv.waitKey(1) == ord('q'):
                #     break
            # When everything done, release the capture
        finally:
            cap.release()
            # cv.destroyAllWindows()

    async def camera_feed(self):
        state = self.state
        # cap = self.cap
        lock = self.lock

        while True:
            with lock:
                with self.state['frame_cv']:
                    if 'frame_ml' in state:
                        frame = state['frame_ml']
                    else:
                        frame = state['frame']

            if frame is None:
                frame_bytes = b''
            else:
                frame_bytes = cv2.imencode(
                    ".jpg",
                    frame,
                    #[cv2.IMWRITE_JPEG_QUALITY, 50, cv2.IMWRITE_JPEG_PROGRESSIVE, 1],
                    [cv2.IMWRITE_JPEG_QUALITY, 75, cv2.IMWRITE_JPEG_PROGRESSIVE, 1],
                )[1].tobytes()

            yield (
                b'--frame\r\n' +
                b'Content-Type: image/jpeg\r\n\r\n' +
                frame_bytes + b'\r\n'
            )
            #time.sleep(1.0)
            #time.sleep(1 / self.feed_fps)
            await asyncio.sleep(1 / self.feed_fps)

    async def video_feed(self, *args, **kwargs):
        # return the response generated along with the specific media
        # type (mime type)
        async def generator():
            async for o in self.camera_feed():
                yield o

        return fastapi.responses.StreamingResponse(
            generator(),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )

    def index(self, *args, **kwargs):
        return fastapi.responses.HTMLResponse(r'''
    <html>
      <head>
        <title>Pi Video Surveillance</title>
      </head>
      <body>
        <h1>Pi Video Surveillance</h1>
        <img src="{URL_PREFIX}/video_feed">
      </body>
    </html>
        '''.replace(
            '{URL_PREFIX}',
            self.url_prefix,
        ))


    async def ws(self, websocket: fastapi.WebSocket):
        state = self.state
        cap = self.cap
        lock = self.lock

        await websocket.accept()

        while True:
            with lock:
                with self.state['frame_cv']:
                    boxes = state.get('boxes'),

            # data = await websocket.receive_text()

            if not boxes is None:
                try:
                    await websocket.send_json(dict(
                        boxes=boxes,
                    ))
                except fastapi.WebSocketDisconnect:
                    break


            await asyncio.sleep(1 / self.feed_fps)

    def run(
        self,
        transform_cb,
    ):
        # self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.cap = cv2.VideoCapture(*self.video_args)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, 250)
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
        if not self.frame_width is None:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)

        if not self.frame_height is None:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)

        self.cap.set(cv2.CAP_PROP_FPS, 30.0)

        logger.error(json.dumps(dict(
            width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
            height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
            fps=self.cap.get(cv2.CAP_PROP_FPS),
        )))

        assert self.cap.isOpened()

        self.lock = threading.Lock()

        self.transform_cb = transform_cb

        self.state['frame_cv'] = threading.Condition()
        self.state['workers']['cv'] = threading.Thread(target=self.camera_worker)
        self.state['workers']['cv'].start()

        self.state['workers']['ml'] = threading.Thread(
            target=functools.partial(
                transform_cb,
                frame_get=lambda: self.state['frame'],
                frame_set=lambda frame, **kwargs: self.state.update(
                    frame_ml=frame, **kwargs
                ),
                frame_cv=self.state['frame_cv'],
            )
        )
        self.state['workers']['ml'].start()

        app = fastapi.FastAPI()

        if not self.need_cors:
            app.add_middleware(
                fastapi.middleware.cors.CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        app.route("%s/video_feed" % self.url_prefix)(self.video_feed)
        app.route("%s/index.html" % self.url_prefix)(self.index)

        app.websocket("%s/ws" % self.url_prefix)(self.ws)

        self.app = app

if __name__ == '__main__':
    t = Test()
    t.run()
    app = t.app
