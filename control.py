from djitellopy import Tello
from queue import Queue
from PIL import Image, ImageQt
import time


class Controller(Tello):
    def __init__(self, IP: str, retry_count=3):
        super().__init__(host=IP, retry_count=retry_count)
        self.connect()

    def m_video(self, image_queue: Queue):  # recieving the frames from the drone
        self.streamon()
        frame_read = self.get_frame_read()
        while True:
            time.sleep(1 / 30)
            f = frame_read.frame
            if f is not None:
                img = Image.fromarray(f, mode='RGB')
                qt_img = ImageQt.ImageQt(img)
                image_queue.put(qt_img)

    def m_movement(self, command: str):  # handling commands send by the GUI
        if command == "up":
            self.move_up(50)
        elif command == "down":
            self.move_down(50)
        elif command == "forward":
            self.move_forward(50)
        elif command == "backward":
            self.move_back(50)
        elif command == "left":
            self.move_left(50)
        elif command == "right":
            self.move_right(50)
        elif command == "rotate_l":
            self.rotate_counter_clockwise(90)
        elif command == "rotate_r":
            self.rotate_clockwise(90)
        elif command == "land":
            self.land()
        elif command == "flip_back":
            self.streamoff()
            time.sleep(1)
            self.flip_back()
            time.sleep(1)
            self.streamon()
        elif command == "flip_forward":
            self.streamoff()
            time.sleep(1)
            self.flip_forward()
            time.sleep(1)
            self.streamon()
        elif command == "flip_right":
            self.streamoff()
            time.sleep(1)
            self.flip_right()
            time.sleep(1)
            self.streamon()
        elif command == "flip_left":
            self.streamoff()
            time.sleep(1)
            self.flip_left()
            time.sleep(1)
            self.streamon()
        elif command == "start":
            self.takeoff()
        elif command == "dance":
            self.move_left(50)
            self.move_right(100)
            self.move_left(50)
            self.rotate_clockwise(360)
            # self.flip_forward()
            # self.flip_back()
        elif command == "emergency":
            self.emergency()
        elif command == "jump":
            self.move_up(50)
            self.move_down(50)
