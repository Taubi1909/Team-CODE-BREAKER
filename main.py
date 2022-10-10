import sys
import control
import gui
import time
import threading
from queue import Queue

def main():
	queue = Queue()
	controller = control.Controler("10.2.210.33")
	t1 = threading.Thread(target=control_tread, daemon=None, args=(queue, controller, ))
	t1.start()
	t2 = threading.Thread(target=control_tread, daemon=None, args=(controller, ))
	t2.start()
	gui.start_gui(queue)


def control_tread(q: Queue, controller: control.Controler):
	controller.takeoff()
	time.sleep(2)
	while True:
		cmd: str = q.get()
		if cmd == "land":
			break
		controller.m_movement(cmd)
		
	controller.land()
	time.sleep(5)
	controller.end()

def video_thread(controller: control.Controler):
	controller.m_video()

if __name__ == '__main__':
	main()