import numpy as np
import numpy
import functools
import time
import threading
import datetime
import cv2 as cv
import cv2
import fastapi
import fastapi.responses

class Test:
    def __init__(self):
        self.state = dict(
            frame=None,
            workers=dict(),
        )

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

                cv2.putText(frame, f"{datetime.datetime.now().isoformat()}", (900, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                # print('\r%s', frame.shape, end='')
                # if frame is read correctly ret is True
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                # Our operations on the frame come here
                #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                gray = frame

                # frame2 = numpy.pad(
                #     frame,
                #     [
                #         (
                #             (1920 - frame.shape[0]) // 2,
                #         ) * 2,
                #         #(
                #         #    (1920 - frame.shape[1]) // 2,
                #         #) * 2,
                #         (0, 0),
                #         (0,0)
                #     ]
                # )[:, -1080:, :]
                # frame2 = cv2.resize(
                #    frame,
                #    #(1280 // 2, 720 // 2),
                #    (1920, 1080),
                #    interpolation=cv2.INTER_AREA
                # )
                frame2 = frame

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

    def camera_feed(self):
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
                    [cv2.IMWRITE_JPEG_QUALITY, 80, cv2.IMWRITE_JPEG_PROGRESSIVE, 1],
                )[1].tobytes()

            yield (
                b'--frame\r\n' +
                b'Content-Type: image/jpeg\r\n\r\n' +
                frame_bytes + b'\r\n'
            )
            #time.sleep(1.0)
            time.sleep(1 / 30)

    def video_feed(self, *args, **kwargs):
        # return the response generated along with the specific media
        # type (mime type)
        return fastapi.responses.StreamingResponse(
            self.camera_feed(),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )

    def index(*args, **kwargs):
        return fastapi.responses.HTMLResponse(r'''
    <html>
      <head>
        <title>Pi Video Surveillance</title>
      </head>
      <body>
        <h1>Pi Video Surveillance</h1>
        <img src="/juggling/video_feed">
      </body>
    </html>
        ''')


    def run(
        self,
        transform_cb,
    ):
        self.cap = cv2.VideoCapture(4, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, 250)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_FPS, 60.0)

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
                frame_set=lambda frame: self.state.update(frame_ml=frame),
                frame_cv=self.state['frame_cv'],
            )
        )
        self.state['workers']['ml'].start()

        app = fastapi.FastAPI()
        app.route("/juggling/video_feed")(self.video_feed)
        app.route("/juggling/index.html")(self.index)

        self.app = app

if __name__ == '__main__':
    t = Test()
    t.run()
    app = t.app
