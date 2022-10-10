import sys
import control
import gui
import time
import threading
from queue import Queue

def main():
	t1 = threading.Thread(target=control_tread, daemon=None)
	t1.start()
	gui.start_gui()


def control_tread():
	controller = control.Controler("10.2.210.33")
	print("Test")
	controller.takeoff()
	time.sleep(5)
	controller.land()
	time.sleep(5)
	controller.end()


if __name__ == '__main__':
	main()