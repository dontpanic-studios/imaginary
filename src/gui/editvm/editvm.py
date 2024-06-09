from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QTabWidget, QFormLayout, QLineEdit
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6 import QtCore
from PyQt6.QtCore import QSize
from src.gui.label import whynotclick
import os, logging, traceback, json
from dotenv import load_dotenv
from src.language.lang import LanguageList
from src.language.lang import Language
from difflib import SequenceMatcher

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

            self.setWindowTitle(Language.getLanguageByEnum(LanguageList.EDITVM_TITLE))
            self.setStyleSheet("background-color: #262626; Color : white;") 
            self.setWindowIcon(QIcon('src/png/icons/128.png'))
            self.setFixedSize(self.width, self.height)
            self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint)
            self.vmname = vmname

            self.initUI()
            log.info('initallized.')
        except Exception as e:
            print(f"ERROR Occurred!\nLog: \n{traceback.format_exc()}")
            errInfoWinInit = QMessageBox(self)
            errInfoWinInit.setWindowTitle(Language.getLanguageByEnum(LanguageList.MSG_VAR_TITLE))
            errInfoWinInit.setText(Language.getLanguageByEnum(LanguageList.MSG_VAR_DESC))
            errInfoWinInit.setDetailedText(traceback.format_exc())
            errInfoWinInit.setIcon(QMessageBox.Icon.Critical)
            errInfoWinInit.exec()
            print('failed to intiallized window')
            exit("Program Exited cause unknown problem has been appeared.")
    
    def initUI(self):
        #self.back = QLabel(self) # random background image that was used back in the day.
        self.label_Title = QLabel(Language.getLanguageByEnum(LanguageList.EDITVM_TITLE), self)
        self.btn_SaveEdited = whynotclick.Label(self)
        self.btn_SaveEdited.setText(Language.getLanguageByEnum(LanguageList.CREATEVM_SAVE))

        #self.back.setPixmap(QPixmap('src/png/background/vmEditBack.png'))   

        self.vmEditTile = QTabWidget(self)
        self.vmEditTile.setMovable(False)
        self.vmEditTile.setTabPosition(QTabWidget.TabPosition.West)

        generalPage = QWidget(self.vmEditTile)
        generalPageLayout = QFormLayout()
        generalPageLayout.addRow('VM Name', QLineEdit(self.loadData()['vm_name'], self))

        generalPage.setLayout(generalPageLayout)

        self.vmEditTile.addTab(generalPage, Language.getLanguageByEnum(LanguageList.TAB_GENERAL))

        font_bold_title = self.label_Title.font()
        font_bold_title.setBold(True)
        font_bold_title.setPointSize(26)
        font_bold_title.setFamily(os.environ.get('Font'))

        font_normal = self.label_Title.font()
        font_normal.setBold(True)
        font_normal.setPointSize(15)
        font_normal.setFamily(os.environ.get('Font'))

        font_button = self.label_Title.font()
        font_button.setBold(True)
        font_button.setPointSize(20)
        font_button.setFamily(os.environ.get('Font'))

        self.label_Title.move(20, 13)
        self.label_Title.setFont(font_bold_title)
        #self.back.move(20, 60)
        self.btn_SaveEdited.move(535, 413)
        self.btn_SaveEdited.setFont(font_button)
        self.btn_SaveEdited.setStyleSheet("Color : white; background-color: None;")
        self.vmEditTile.setStyleSheet("background-color: #262626")
        self.vmEditTile.move(20, 60)

    def loadData(self):
        try:
            f = open('./src/vm/' + self.vmname + '/metadata.json', 'r+')
            return json.load(f)
        except (json.JSONDecodeError, PermissionError, SystemError):
            jsonDecodingError = QMessageBox.critical(self, Language.getLanguageByEnum(LanguageList.MSG_VAR_TITLE), Language.getLanguageByEnum(LanguageList.MSG_VAR_DESC))
    