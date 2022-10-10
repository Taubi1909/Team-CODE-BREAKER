class Controler():
	def __init__(self) -> None:
		self.i = 2

	def start(self, a: int):
		print(a)
		print(self.i)

controller = Controler()
controller.start(7)