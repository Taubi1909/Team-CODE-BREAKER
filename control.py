from djitellopy import Tello
from queue import Queue

tello = Tello()

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

	def m_movement(self, command: str):
		pass