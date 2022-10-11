import os
import shutil
import sys
import subprocess
from os.path import expanduser
from queue import Queue
import time

from PyQt5.QtWidgets import (
    QStatusBar, QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QMainWindow,
    QAction,
    QGridLayout,
    QScrollArea,
    QLabel,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QProgressBar
)
from PyQt5.QtGui import QIcon, QPixmap, QKeyEvent
from PyQt5.QtCore import QObject, pyqtSignal, QThreadPool
from PyQt5.Qt import Qt


app = QApplication(sys.argv)

class MainWidget(QWidget):
    def __init__(self, q: Queue, image_q: Queue, controller):
        super().__init__()
        self.q = q
        self.image_q = image_q
        self.threadmanager = QThreadPool()
        self.controller = controller
        self.initMe()

    def initMe(self):
        self.v = QVBoxLayout(self)
        self.label = QLabel()
        # self.label.setPixmap(QPixmap.fromImage(self.image_q.get()))
        self.label.setPixmap(QPixmap("loading_video.png"))
        self.grid = QGridLayout()
        self.v.addWidget(self.label)
        self.btn_up = QPushButton("up")
        self.btn_up.pressed.connect(lambda: self.q.put("up"))

        self.battery = QLabel("T4N14s Health:")
        self.v.addWidget(self.battery)

        self.battery_bar = QProgressBar()

        self.v.addWidget(self.battery_bar)

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
        self.threadmanager.start(self.update_pixmap)
        self.threadmanager.start(self.update_battery)

    def update_pixmap(self):
        while True:
            time.sleep(1 / 30)
            img = self.image_q.get()
            self.label.setPixmap(QPixmap.fromImage(img))

    def update_battery(self):
        while True:
            battery_percent: int = self.controller.get_battery()
            self.battery_bar.setValue(battery_percent)
            # if battery_percent <= 15:
            #    self.battery_bar.
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

    def keyPressEvent(self, event: QKeyEvent):
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

    def closeEvent(self, event):
        self.controller.end()
        return super().closeEvent(event)


def start_gui(q: Queue, image_q: Queue, controller):
    w = Window(q, image_q, controller)
    sys.exit(app.exec_())
