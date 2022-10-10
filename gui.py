#! /usr/bin/env python3

# Entrypoint to the Application
import os
import shutil
import sys
import subprocess
from os.path import expanduser
from queue import Queue


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
from PyQt5.QtCore import QObject, Qt, pyqtSignal



app = QApplication(sys.argv)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.v = QVBoxLayout(self)
        self.btn = QPushButton("up")
        
        # self.label = QLabel()
        # self.img = QPixmap()
        # self.label.setPixmap(self.img)
        # self.v.addWidget(self.label)
        self.btn.connect()
        self.v.addLayout(self.btn)
        self.setLayout(self.v)

    def up(self, *args):


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):

        self.state = QStatusBar(self)  # Create Statusbar


        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle('Team Code Breaker')


        self.mainwidget = MainWidget()
        self.setCentralWidget(self.mainwidget)

        self.show()


def start_gui():
    w = Window()
    sys.exit(app.exec_())
