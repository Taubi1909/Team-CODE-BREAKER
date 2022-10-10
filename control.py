from djitellopy import Tello
from queue import Queue
from PIL import Image, QtImage
"""
up
down
forwards
backwards
left
right
rotate_l
rotate_r
"""

class Controler(Tello):
	def __init__(self, IP: str, retry_count=3):
		super().__init__(host=IP, retry_count=retry_count)
		self.connect()

	def m_video(self):
		self.streamon()
		frame_read = self.get_frame_read()
		f = frame_read.frame
		img = Image.fromarray(table, mode='RGB')
		qt_img = ImageQt.ImageQt(img)

	def m_movement(self, command: str):
		if command == "up":
			self.move_up(50)
		elif command == "down":
			self.move_down(50)