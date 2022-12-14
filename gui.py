import sys
from queue import Queue
import time

from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QApplication,
    QMainWindow,
    QGridLayout,
    QLabel,
    QProgressBar
)
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtCore import QObject, pyqtSignal, QThreadPool
from PyQt5.Qt import Qt

from djitellopy import TelloSwarm
import control

app = QApplication(sys.argv)

class Signals(QObject):
    running = pyqtSignal(bool)

sig = Signals()

class MainWidget(QWidget):
    def __init__(self, q: Queue, image_q: Queue, controller):
        super().__init__()
        self.q = q
        self.image_q = image_q
        self.threadmanager = QThreadPool()
        self.controller = controller
        self.runnning = True
        self.initMe()

    def initMe(self):  # Building the GUI
        self.v = QVBoxLayout(self)
        self.label = QLabel()
        self.label.setPixmap(QPixmap("loading_video.png"))
        self.grid = QGridLayout()
        self.v.addWidget(self.label)

        self.battery = QLabel("T4N14s Health:")
        self.v.addWidget(self.battery)

        if type(self.controller) == control.Controller:
            self.battery_bar = QProgressBar()  # Bar for displaying battery percentage
            self.v.addWidget(self.battery_bar)
        elif type(self.controller) == TelloSwarm:
            i = 0
            self.battery_bars = []
            for j in self.controller:
                self.battery_bars.append(QProgressBar())  # Bars for displaying battery percentage
                self.battery_bars[i].setToolTip(j.address[0])
                self.v.addWidget(self.battery_bars[i])
                i += 1

        # Buttons for controlling
        self.btn_up = QPushButton("up")
        self.btn_up.pressed.connect(lambda: self.q.put("up"))
        self.grid.addWidget(self.btn_up, 0, 0)

        self.btn_fw = QPushButton("forward")
        self.btn_fw.pressed.connect(lambda: self.q.put("forward"))
        self.grid.addWidget(self.btn_fw, 0, 1)

        self.btn_down = QPushButton("down")
        self.btn_down.pressed.connect(lambda: self.q.put("down"))
        self.grid.addWidget(self.btn_down, 0, 2)

        self.btn_left = QPushButton("left")
        self.btn_left.pressed.connect(lambda: self.q.put("left"))
        self.grid.addWidget(self.btn_left, 1, 0)

        self.btn_back = QPushButton("backward")
        self.btn_back.pressed.connect(lambda: self.q.put("backward"))
        self.grid.addWidget(self.btn_back, 1, 1)

        self.btn_right = QPushButton("right")
        self.btn_right.pressed.connect(lambda: self.q.put("right"))
        self.grid.addWidget(self.btn_right, 1, 2)

        self.btn_rl = QPushButton("rotate_l")
        self.btn_rl.pressed.connect(lambda: self.q.put("rotate_l"))
        self.grid.addWidget(self.btn_rl, 2, 0)

        self.btn_land = QPushButton("land")
        self.btn_land.pressed.connect(lambda: self.q.put("land"))
        self.grid.addWidget(self.btn_land, 2, 1)

        self.btn_rr = QPushButton("rotate_r")
        self.btn_rr.pressed.connect(lambda: self.q.put("rotate_r"))
        self.grid.addWidget(self.btn_rr, 2, 2)

        self.btn_fl = QPushButton("flip_left")
        self.btn_fl.pressed.connect(lambda: self.q.put("flip_left"))
        self.grid.addWidget(self.btn_fl, 3, 0)

        self.btn_ff = QPushButton("flip_forward")
        self.btn_ff.pressed.connect(lambda: self.q.put("flip_forward"))
        self.grid.addWidget(self.btn_ff, 3, 1)

        self.btn_fr = QPushButton("flip_right")
        self.btn_fr.pressed.connect(lambda: self.q.put("flip_right"))
        self.grid.addWidget(self.btn_fr, 3, 2)

        self.btn_start = QPushButton("start")
        self.btn_start.pressed.connect(lambda: self.q.put("start"))
        self.grid.addWidget(self.btn_start, 4, 0)

        self.btn_fb = QPushButton("flip_back")
        self.btn_fb.pressed.connect(lambda: self.q.put("flip_back"))
        self.grid.addWidget(self.btn_fb, 4, 1)

        self.btn_d = QPushButton("dance")
        self.btn_d.pressed.connect(lambda: self.q.put("dance"))
        self.grid.addWidget(self.btn_d, 4, 2)

        self.btn_emergency = QPushButton("EMERGENCY")
        self.btn_emergency.setStyleSheet("background-color: red;")
        self.btn_emergency.pressed.connect(lambda: self.q.put("emergency"))

        self.v.addLayout(self.grid)
        self.v.addWidget(self.btn_emergency)
        self.setLayout(self.v)
        self.threadmanager.start(self.update_pixmap)  # Responsible for updating the image, for displaying the camera
        self.threadmanager.start(self.update_battery)  # Responsible for updating the battery bar

        sig.running.connect(self.stop_threads)  # Signal emitted when programm is being closed

    def stop_threads(self):
        self.runnning = False

    def update_pixmap(self):
        while self.runnning:
            time.sleep(1 / 30)
            img = self.image_q.get()
            self.label.setPixmap(QPixmap.fromImage(img))

    def update_battery(self):
        while self.runnning:
            if type(self.controller) == control.Controller:
                battery_percent: int = self.controller.get_battery()
                self.battery_bar.setValue(battery_percent)
            elif type(self.controller) == TelloSwarm:
                i = 0
                for j in self.controller:
                    battery_percent: int = j.get_battery()
                    self.battery_bars[i].setValue(battery_percent)
                    i += 1

            time.sleep(30)

class Window(QMainWindow):
    def __init__(self, q: Queue, image_q: Queue, controller):
        super().__init__()
        self.q = q
        self.image_q = image_q
        self.controller = controller
        self.initMe()

    def initMe(self):
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle('Team Code Breaker')

        self.mainwidget = MainWidget(self.q, self.image_q, self.controller)
        self.setCentralWidget(self.mainwidget)

        self.show()

    def keyPressEvent(self, event: QKeyEvent):  # Using The Keyboard to control the drone
        if event.key() == Qt.Key_W:
            self.q.put("forward")
        elif event.key() == Qt.Key_S:
            self.q.put("backward")
        elif event.key() == Qt.Key_D:
            self.q.put("right")
        elif event.key() == Qt.Key_A:
            self.q.put("left")
        elif event.key() == Qt.Key_I:
            self.q.put("up")
        elif event.key() == Qt.Key_K:
            self.q.put("down")
        elif event.key() == Qt.Key_J:
            self.q.put("rotate_l")
        elif event.key() == Qt.Key_L:
            self.q.put("rotate_r")
        elif event.key() == Qt.Key_C:
            self.q.put("land")
        elif event.key() == Qt.Key_V:
            self.q.put("flip_forward")
        elif event.key() == Qt.Key_B:
            self.q.put("flip_back")
        elif event.key() == Qt.Key_N:
            self.q.put("flip_right")
        elif event.key() == Qt.Key_M:
            self.q.put("flip_left")
        elif event.key() == Qt.Key_G:
            self.q.put("start")
        elif event.key() == Qt.Key_Y:
            self.q.put("dance")
        elif event.key() == Qt.Key_X:
            self.q.put("emergency")
        elif event.key() == Qt.Key_Space:
            self.q.put("jump")
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):  # Called when window_close button is pressed
        self.controller.end()
        self.q.put("exit")
        sig.running.emit(False)
        return super().closeEvent(event)


def start_gui(q: Queue, image_q: Queue, controller):
    w = Window(q, image_q, controller)
    sys.exit(app.exec_())
