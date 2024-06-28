from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6 import QtCore
from src.gui.label import whynotclick
import os, logging, traceback, json
from dotenv import load_dotenv
from src.language.lang import LanguageList
from src.language.lang import Language

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
            self.pageList = [1, 2, 3]
            self.curPage = 1

            self.initUI()
            self.setData()
            self.setupKR()
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
        self.back = QLabel(self) # random background image that was used back in the day.
        self.label_Title = QLabel(Language.getLanguageByEnum(LanguageList.EDITVM_TITLE), self)

        self.btn_SaveEdited = whynotclick.Label(self)
        self.btn_SaveEdited.setText(Language.getLanguageByEnum(LanguageList.CREATEVM_SAVE))
        self.btn_GeneralPage = whynotclick.Label(self)
        self.btn_GeneralPage.setText(Language.getLanguageByEnum(LanguageList.TAB_GENERAL))
        self.btn_DiskPage = whynotclick.Label(self)
        self.btn_DiskPage.setText(Language.getLanguageByEnum(LanguageList.TAB_DISK))
        self.btn_EtcPage = whynotclick.Label(self)
        self.btn_EtcPage.setText(Language.getLanguageByEnum(LanguageList.TAB_ETC))

        self.back.setPixmap(QPixmap('src/png/background/vmEditBack.png'))

        # general page
        self.pg1_label_VMName = QLabel(Language.getLanguageByEnum(LanguageList.CREATEVM_LABEL_VMNAME), self)
        self.pg1_Input_VMName = QLineEdit(self)
        self.pg1_label_VMDesc = QLabel(Language.getLanguageByEnum(LanguageList.CREATEVM_LABEL_VMDESC), self)
        self.pg1_Input_VMDesc = QLineEdit(self)
        self.pg1_label_RamSize = QLabel(Language.getLanguageByEnum(LanguageList.CREATEVM_LABEL_RAM), self)
        self.pg1_Input_RamSize = QLineEdit(self)
        self.pg1_label_ISOLoc = QLabel(Language.getLanguageByEnum(LanguageList.CREATEVM_TITLE_LOADISO), self)
        self.pg1_btn_ISOLoc = whynotclick.Label(self)
        self.pg1_btn_ISOLoc.setText(Language.getLanguageByEnum(LanguageList.CREATEVM_LABEL_LOADISO))
        self.pg1_lable_CPUSize = QLabel(Language.getLanguageByEnum(LanguageList.CREATEVM_LABEL_CPU), self)
        self.pg1_Input_CPUSize = QLineEdit(self)

        self.font_bold_title = self.label_Title.font()
        self.font_bold_title.setBold(True)
        self.font_bold_title.setPointSize(26)
        self.font_bold_title.setFamily(os.environ.get('Font'))

        self.font_normal = self.label_Title.font()
        self.font_normal.setBold(True)
        self.font_normal.setPointSize(15)
        self.font_normal.setFamily(os.environ.get('Font'))

        self.font_button = self.label_Title.font()
        self.font_button.setBold(True)
        self.font_button.setPointSize(20)
        self.font_button.setFamily(os.environ.get('Font'))

        self.label_Title.move(20, 13)
        self.label_Title.setFont(self.font_bold_title)
        self.back.move(20, 90)
        self.btn_SaveEdited.move(545, 435)
        self.btn_SaveEdited.setFont(self.font_button)
        self.btn_SaveEdited.setStyleSheet("Color : white; background-color: None;")
        self.btn_GeneralPage.move(20, 55)
        self.btn_GeneralPage.setFont(self.font_normal)
        self.btn_DiskPage.move(110, 55)
        self.btn_DiskPage.setFont(self.font_normal)
        self.btn_EtcPage.move(165, 55)
        self.btn_EtcPage.setFont(self.font_normal)
        self.pg1_label_VMName.setFont(self.font_normal)
        self.pg1_label_VMName.move(35, 100)
        self.pg1_label_VMDesc.setStyleSheet("Color : white; background-color: None;")
        self.pg1_label_VMName.setStyleSheet("Color : white; background-color: None;")
        self.pg1_label_RamSize.setStyleSheet("Color : white; background-color: None;")
        self.pg1_Input_VMName.setFont(self.font_normal)
        self.pg1_Input_VMName.move(35, 130)
        self.pg1_label_VMDesc.setFont(self.font_normal)
        self.pg1_label_VMDesc.move(350, 100)
        self.pg1_Input_VMDesc.setFont(self.font_normal)
        self.pg1_Input_VMDesc.move(350, 130)
        self.pg1_label_RamSize.setFont(self.font_normal)
        self.pg1_Input_RamSize.setFont(self.font_normal)
        self.pg1_Input_RamSize.move(35, 210)
        self.pg1_label_RamSize.move(35, 180)
        self.pg1_btn_ISOLoc.setStyleSheet("Color : #4aa4ff; background-color: None;")
        self.pg1_label_ISOLoc.setStyleSheet("Color : white; background-color: None;")
        self.pg1_btn_ISOLoc.setFont(self.font_normal)
        self.pg1_label_ISOLoc.setFont(self.font_normal)
        self.pg1_label_ISOLoc.move(35, 290)
        self.pg1_btn_ISOLoc.move(35, 310)
        self.pg1_Input_CPUSize.setFont(self.font_normal)
        self.pg1_lable_CPUSize.setFont(self.font_normal)
        self.pg1_lable_CPUSize.setStyleSheet("Color : white; background-color : None;")
        self.pg1_lable_CPUSize.move(350, 180)
        self.pg1_Input_CPUSize.move(350, 210)

        self.back.resize(600, 340)

    def setData(self):
        self.pg1_Input_VMName.setText(self.loadData()['vm_name'])
        self.pg1_Input_VMDesc.setText(self.loadData()['desc'])
        self.pg1_Input_RamSize.setText(self.loadData()['max_mem'])
        self.pg1_btn_ISOLoc.setText(self.loadData()['iso_loc'])
        self.pg1_btn_ISOLoc.adjustSize()
        self.pg1_Input_CPUSize.setText(self.loadData()['max_core'])

    def loadData(self):
        try:
            f = open('./src/vm/' + self.vmname + '/metadata.json', 'r+')
            return json.load(f)
        except (json.JSONDecodeError, PermissionError, SystemError):
            jsonDecodingError = QMessageBox.critical(self, Language.getLanguageByEnum(LanguageList.MSG_VAR_TITLE), Language.getLanguageByEnum(LanguageList.MSG_VAR_DESC))
    
    def setupKR(self):
        if(os.environ.get('Language') == 'ko_KR'):
            print('KR Lang Detected, Moving.')
            self.btn_DiskPage.move(80, 55)
        else:
            print('en_US found, ignoring.')