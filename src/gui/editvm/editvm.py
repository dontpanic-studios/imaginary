from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit, QFileDialog, QTabWidget
from PyQt6.QtGui import QIcon
from PyQt6 import QtCore
from src.gui.label import whynotclick
import os, sys, logging, json
from dotenv import load_dotenv

log = logging
logFilePath = './log/debug-log.log'
load_dotenv('./data/setting.env')

class EditVM(QWidget):
    def __init__(self, vmname):
        log.info('trying initallizing frame..')
        try:
            super().__init__()

            self.width = 640
            self.height = 480
            self.vmname = vmname

            self.setWindowTitle("Edit VM")
            self.setStyleSheet("background-color: #262626;") 
            self.setWindowIcon(QIcon('src/png/icons/128.png'))
            self.setFixedSize(self.width, self.height)
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
        self.label_Title = QLabel('Edit VM', self)
        self.label_VM_Name = QLabel('Dummy', self)
        self.label_createVM = whynotclick.Label(self)
        self.label_createVM.setText('Save')

        self.generalTab = QWidget()
        self.systemTab = QWidget()
        self.debugTab = QWidget()

        # font
        font_bold_title = self.label_Title.font()
        font_bold_title.setBold(True)
        font_bold_title.setPointSize(30)
        font_bold_title.setFamily(os.environ.get('Font'))

        font_bold = self.label_Title.font()
        font_bold.setBold(True)
        font_bold.setPointSize(20)
        font_bold.setFamily(os.environ.get('Font'))

        font_button = self.label_Title.font()
        font_button.setBold(True)
        font_button.setPointSize(13)
        font_button.setFamily(os.environ.get('Font'))      

        self.label_Title.move(20, 15)
        self.label_createVM.move(550, 430)
        self.label_VM_Name.move(20, 70)

        self.label_Title.setFont(font_bold_title)
        self.label_createVM.setFont(font_bold)
        self.label_VM_Name.setFont(font_button)

        self.label_Title.setStyleSheet("Color : white;")
        self.label_createVM.setStyleSheet("Color : white;")
        self.label_VM_Name.setStyleSheet("Color : white;")

        self.label_createVM.adjustSize()
        self.label_Title.adjustSize()
        self.label_createVM.clicked.connect(self.saveEdit)

        self.label_VM_Name.setText(self.vmname)

    def saveEdit(self):
        self.close()    

    def loadData(self, name):
        f = open(f'./src/vm/{name}/metadata.json', 'r+')   
        self.data = json.load(f)
        print(f'Got package, header: \n{self.data}')