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
    QAbstractItemView
)
from PyQt5.QtGui import QIcon, QPixmap, QKeyEvent
from PyQt5.QtCore import QObject, Qt, pyqtSignal, QThreadPool


app = QApplication(sys.argv)

class MainWidget(QWidget):
    def __init__(self, q: Queue, image_q: Queue):
        super().__init__()
        self.q = q
        self.image_q = image_q
        self.initMe()
        self.threadmanager = QThreadPool()

    def initMe(self):
        self.v = QVBoxLayout(self)
        self.label = QLabel()
        # self.label.setPixmap(QPixmap.fromImage(self.image_q.get()))
        # self.label.setPixmap(QPixmap("image.png"))
        self.v.addWidget(self.label)
        self.btn_up = QPushButton("up")
        self.btn_up.pressed.connect(self.up)
        self.v.addWidget(self.btn_up)

        self.btn_down = QPushButton("down")
        self.btn_down.pressed.connect(self.down)
        self.v.addWidget(self.btn_down)
        self.setLayout(self.v)
        self.threadmanager.start(self.update_pixmap)

    def up(self, *args):
        self.q.put("up")

    def down(self, *args):
        self.q.put("down")

    def update_pixmap(self):
        while True:
            time.sleep(1 / 30)
            img = self.image_q.get_nowait()
            if img is not None:
                self.label.setPixmap(QPixmap.fromImage(img))

class Window(QMainWindow):
    def __init__(self, q: Queue, image_q: Queue):
        super().__init__()
        self.q = q
        self.image_q = image_q
        self.initMe()

    def initMe(self):

        self.state = QStatusBar(self)  # Create Statusbar


        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle('Team Code Breaker')


        self.mainwidget = MainWidget(self.q, self.image_q)
        self.setCentralWidget(self.mainwidget)

        self.show()


def start_gui(q: Queue, image_q: Queue):
    w = Window(q, image_q)
    sys.exit(app.exec_())
