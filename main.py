import sys
import control
import gui
import time
import threading
from queue import Queue

def main():
	queue = Queue()
	image_queue = Queue()
	controller = control.Controler("10.2.210.33")
	t1 = threading.Thread(target=control_thread, daemon=None, args=(queue, controller, ))
	t1.start()
	t2 = threading.Thread(target=video_thread, daemon=None, args=(controller, image_queue, ))
	t2.start()
	gui.start_gui(queue, image_queue, controller)


def control_thread(q: Queue, controller: control.Controler):
	controller.takeoff()
	time.sleep(2)
	while True:
		cmd: str = q.get()
		try:
			controller.m_movement(cmd)
		except Exception as e:
			print(e)
		
	controller.land()
	time.sleep(5)
	controller.end()

def video_thread(controller: control.Controler, image_queue: Queue):
	controller.m_video(image_queue)

if __name__ == '__main__':
	main()