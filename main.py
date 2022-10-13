import control
import gui
import time
import threading
from queue import Queue


def main():
    queue = Queue()  # Queue for commands send to the drone
    image_queue = Queue()  # Queue for every image send by the drone
    controller = control.Controller("10.2.210.33")
    t1 = threading.Thread(target=control_thread, daemon=None, args=(queue, controller, ))
    t1.start()
    t2 = threading.Thread(target=video_thread, daemon=None, args=(controller, image_queue, ))
    t2.start()
    gui.start_gui(queue, image_queue, controller)


def control_thread(q: Queue, controller: control.Controller):
    # Function for controlling the drone
    controller.takeoff()
    time.sleep(2)
    a = True
    while a:
        cmd: str = q.get()
        if cmd == "exit":
            a = False
        try:
            controller.m_movement(cmd)
        except Exception as e:
            print(e)


def video_thread(controller: control.Controller, image_queue: Queue):
    # Function for retrieving the Video
    controller.m_video(image_queue)


if __name__ == '__main__':
    main()
