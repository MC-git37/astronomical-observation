import sys
import traceback
from threading import Thread
from time import sleep
from PyQt5.QtWidgets import QApplication
from numpy import true_divide
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox
from youhua import MainWindow,mainWindows



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow(sys.argv)
    mainWindow.show()  # 软件界面
    app.exec_()