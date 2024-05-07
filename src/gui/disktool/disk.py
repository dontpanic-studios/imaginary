from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QCheckBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6 import QtCore
import os, sys, logging
from dotenv import load_dotenv

log = logging
logFilePath = './log/debug-log.log'
load_dotenv('./data/setting.env')

class DiskTool(QWidget):
    def __init__(self):
        log.info('trying initallizing frame..')
        try:
            super().__init__()

            self.setWindowTitle("Imaginary - Disk Tool")
            self.setStyleSheet("background-color: #262626;") 
            self.setWindowIcon(QIcon('./src/png/icons/128.png'))
            self.setFixedSize(640, 200)
            self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint)
            self.initUI()
            log.info('initallized.')
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.critical(f"ERROR Occurred!\nLog: {exc_type}, {exc_obj}, {exc_tb}, {fname}")
            errInfoWinInit = QMessageBox.critical(self, '오류가 발생하였습니다.', '재설정을 하는 중에 오류가 발생했습니다.\n보통 프로그램이 꼬였거나, 저장된 위치에 한글이 들어있으면 안되는 경우가 있습니다.')
            log.critical('failed to intiallized window')

    def initUI(self):
        self.label_Logo = QLabel(self)
        self.label_InfoTitle = QLabel("Disk Tool", self)

        font_bold_title = self.label_InfoTitle.font()
        font_bold_title.setBold(True)
        font_bold_title.setPointSize(30)
        font_bold_title.setFamily(os.environ.get('Font'))

        self.font_bold = self.label_InfoTitle.font()
        self.font_bold.setBold(True)
        self.font_bold.setPointSize(20)
        self.font_bold.setFamily(os.environ.get('Font'))

        self.font_smol = self.label_InfoTitle.font()
        self.font_smol.setBold(True)
        self.font_smol.setPointSize(17)
        self.font_smol.setFamily(os.environ.get('Font'))

        self.label_Logo.move(15, 15)
        self.label_Logo.resize(64, 64)
        self.label_InfoTitle.move(150, 15)

        self.label_InfoTitle.setFont(font_bold_title)
        self.label_InfoTitle.setStyleSheet("Color : white; background-color: #262626;")   

        self.label_Logo.adjustSize()
        self.label_InfoTitle.adjustSize()