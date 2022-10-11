from time import sleep
from djitellopy import Tello
from queue import Queue
from PIL import Image, ImageQt
import time
"""
forwards
backwards
left
right
rotate_l
rotate_r
land
"""

class Controler(Tello):
	def __init__(self, IP: str, retry_count=3):
		super().__init__(host=IP, retry_count=retry_count)
		self.connect()

	def m_video(self, image_queue: Queue):
		self.streamon()
		frame_read = self.get_frame_read()
		# cv2.imwrite("image.png", frame_read.frame)
		img = Image.fromarray(frame_read.frame, mode='RGB')
		qt_img = ImageQt.ImageQt(img)
		image_queue.put(qt_img)
		
	def m_movement(self, command: str):
		if command == "up":
			self.move_up(50)
		elif command == "down":
			self.move_down(50)
		elif command == "forward":
			self.move_forward(50)
		elif command == "backwards":
			self.move_back(50)
		elif command == "left":
			self.move_left(50)
		elif command == "right":
			self.move_right(50)
		elif command == "rotate_l":
			self.move_ccw(90)
		elif command == "rotate_r":
			self .move_cw(90)
		elif command == "land":
			self.land()
		elif command == "flip_back":
			self.flip_back()
		elif command == "flip_forward":
			self.flip_forward()
		elif command == "flip_right":
			self.flip_right()
		elif command == "flip_left":
			self.flip_left()
		elif command == "jump":
			self.move_up(50)
			time.sleep(1)
			self.move_down(50)