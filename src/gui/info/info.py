from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QMessageBox, QListView
from PyQt6.QtGui import QIcon, QPixmap, QStandardItem, QStandardItemModel, QShortcut, QKeySequence
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
import os, sys, logging

log = logging
logFilePath = './log/debug-log.log'

class CreateVM(QWidget):
    def __init__(self):
        log.info('trying initallizing frame..')
        try:
            super().__init__()

            self.top = 200
            self.left = 500
            self.width = 640
            self.height = 480

            self.setWindowTitle("Imaingary INFO")
            self.setStyleSheet("background-color: #262626;") 
            self.setWindowIcon(QIcon('./src/png/icons/128.png'))
            self.setGeometry(self.top, self.left, self.width, self.height)
            self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint)
            self.initUI()
            log.info('initallized.')
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.critical(f"ERROR Occurred!\nLog: {exc_type}, {exc_obj}, {exc_tb}, {fname}")
            errInfoWinInit = QMessageBox.critical(self, '오류가 발생하였습니다.', '재설정을 하는 중에 오류가 발생했습니다.\n보통 프로그램이 꼬였거나, 저장된 위치에 한글이 들어있으면 안되는 경우가 있습니다.')
            log.critical('failed to intiallized window')

    def initUI(self):
        self.label_Logo = QLabel(self)
        self.label_Logo.setPixmap(QPixmap('./src/png/icons/128.png')) 

        self.label_Logo.move(15, 15)