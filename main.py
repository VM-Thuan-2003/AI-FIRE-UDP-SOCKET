from cus_threading import ThreadManager
from detect_fire import Detector
from read_udp import VideoClient
from socket_client import SocketClient

import cv2
import time


class Main:
    def __init__(self):
        self.thread_manager = ThreadManager(2)
        self.thread_manager.start_threads()

        self.video_client = VideoClient("http://103.167.198.50:6001", "123456")

        self.detector = Detector("best.pt", "frame")


if __name__ == "__main__":
    main = Main()
    try:
        main.thread_manager.add_task(main.video_client.connect_to_server)
        while True:
            if main.video_client.frame is not None:
                frame, con = main.detector.detect(main.video_client.frame)

                cv2.imshow("Frame", main.video_client.frame)
                cv2.imshow("Frame and Detect", frame)
                print(con)

                time.sleep(1 / 30)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    except KeyboardInterrupt:
        print("\nDetection stopped.")
        cv2.destroyAllWindows()
        exit()
