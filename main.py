from cus_threading import ThreadManager
from detect_fire import Detector
from read_udp import VideoClient
from cus_socket.socket_client import SocketClient

import cv2
import time
import json
import numpy as np


class Main:
    def __init__(self):
        self.thread_manager = ThreadManager(3)
        self.thread_manager.start_threads()

        self.video_client = VideoClient("http://103.167.198.50:6001", "123456")
        self.client = SocketClient("http://103.167.198.50:5000")

        self.detector = Detector("best.pt", "frame")


if __name__ == "__main__":
    main = Main()
    try:
        main.thread_manager.add_task(main.video_client.connect_to_server)
        main.thread_manager.add_task(main.client.connect)

        while True:
            frame, detects = main.detector.detect(
                main.video_client.frame if main.video_client.frame is not None else None
            )

            if frame is not None:

                cv2.imshow("Frame", main.video_client.frame)
                cv2.imshow("Frame and Detect", frame)

                print(detects)

                if len(detects) > 0:
                    for detect in detects:
                        label = detect[0]
                        conf = np.float64(detect[1])
                        if conf > 0.55:
                            print(f"Drone: {label} {conf}")
                            main.client.send_message(
                                "controlMsg",
                                "web",
                                "fireDetection",
                                {
                                    "label": label,
                                    "conf": conf,
                                },
                            )

            time.sleep(1 / 30)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\nDetection stopped.")
        cv2.destroyAllWindows()
        exit()
