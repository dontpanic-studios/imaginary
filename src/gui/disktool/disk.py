from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit, QComboBox, QFileDialog
from PyQt6.QtGui import QIcon
from PyQt6 import QtCore
from src.gui.label import whynotclick
import os, sys, logging, subprocess, traceback
from dotenv import load_dotenv
from src.language.lang import Language, LanguageList

log = logging
logFilePath = './log/debug-log.log'
load_dotenv('./data/setting.env')

class DiskTool(QWidget):
    def __init__(self):
        log.info('trying initallizing frame..')
        try:
            super().__init__()

            self.setWindowTitle(Language.getLanguageByEnum(LanguageList.DISK_TOOL))
            self.setStyleSheet("background-color: #262626; Color : white;") 
            self.setWindowIcon(QIcon('./src/png/icons/128.png'))
            self.setFixedSize(640, 200)
            self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint)
            self.initUI()
            log.info('initallized.')
        except Exception:
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
        diskType = ["qcow2", "raw", "vhdx"]

        self.label_InfoTitle = QLabel(Language.getLanguageByEnum(LanguageList.DISKTOOL_TITLE), self)
        self.label_DiskSize = QLabel(Language.getLanguageByEnum(LanguageList.DISKTOOL_LABEL_DISKSIZE), self)
        self.label_DiskType = QLabel(Language.getLanguageByEnum(LanguageList.DISKTOOL_LABEL_DISKTYPE), self)
        self.label_DiskName = QLabel(Language.getLanguageByEnum(LanguageList.DISKTOOL_LABEL_DISKNAME), self)

        self.createDisk = whynotclick.Label(self)
        self.createDisk.setText(Language.getLanguageByEnum(LanguageList.DISKTOOL_CREATE_DISK))

        self.Input_DiskSize = QLineEdit(self)
        self.Input_DiskName = QLineEdit(self)

        self.diskTypeList = QComboBox(self)
        self.diskTypeList.addItems(diskType)

        #self.createToAnotherLocation = QCheckBox(self, text="Create Disk to Another Location")

        font_bold_title = self.label_InfoTitle.font()
        font_bold_title.setBold(True)
        font_bold_title.setPointSize(30)
        font_bold_title.setFamily(os.environ.get('Font'))

        font_button = self.label_InfoTitle.font()
        font_button.setBold(True)
        font_button.setPointSize(15)
        font_button.setFamily(os.environ.get('Font'))   

        self.label_InfoTitle.move(15, 15)
        self.Input_DiskName.move(15, 100)
        self.label_DiskName.move(15, 70)
        self.label_DiskSize.move(350, 70)
        self.Input_DiskSize.move(350, 100)
        self.label_DiskType.move(15, 135)
        self.diskTypeList.move(15, 163)

        self.createDisk.move(510, 163)

        self.Input_DiskSize.setPlaceholderText("16G")
        self.Input_DiskName.setPlaceholderText("Windows11")

        self.Input_DiskName.setToolTip("Disk image name must not include word '.', ',', '/', '\\'")

        self.label_InfoTitle.setFont(font_bold_title)
        self.label_InfoTitle.setStyleSheet("Color : white; background-color: #262626;")   
        self.Input_DiskSize.setFont(font_button)
        self.Input_DiskSize.setStyleSheet("Color : white; background-color: #262626;")
        self.createDisk.setFont(font_button)
        self.createDisk.setStyleSheet("Color : white; background-color: #262626;")
        self.label_DiskSize.setFont(font_button)
        self.label_DiskSize.setStyleSheet("Color : white; background-color: #262626;")
        self.diskTypeList.setFont(font_button)
        self.diskTypeList.setStyleSheet("Color : white; background-color: #262626;")
        self.label_DiskType.setFont(font_button)
        self.label_DiskType.setStyleSheet("Color : white; background-color: #262626;")
        self.Input_DiskName.setFont(font_button)
        self.Input_DiskName.setStyleSheet("Color : white; background-color: #262626;")
        self.label_DiskName.setFont(font_button)
        self.label_DiskName.setStyleSheet("Color : white; background-color: #262626;")

        self.label_InfoTitle.adjustSize()

        self.createDisk.clicked.connect(self.generateDisk)

    def generateDisk(self):
        fname = QFileDialog.getExistingDirectoryUrl(self)        
        diskLoc = ""

        if fname.toString():
            if(fname.toString() != ''):
                    diskLoc = fname.toString()
        else:
            msg = QMessageBox.question(self, Language.getLanguageByEnum(LanguageList.MSG_DISKTOOL_CANCEL_TITLE), Language.getLanguageByEnum(LanguageList.MSG_DISKTOOL_CANCEL_DESC), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if(msg == QMessageBox.StandardButton.Yes):
                return
            else:
                self.generateDisk()

        try:
            process = subprocess.check_call(f'cd src/qemu & qemu-img create -f {self.diskTypeList.currentText()} -o size={self.Input_DiskSize.text()} "{self.Input_DiskName.text()}.img" & qemu-img info "{self.Input_DiskName.text()}.img"', shell=True)
            os.rename(f'src/qemu/{self.Input_DiskName.text()}.img', diskLoc)
            
            msg = QMessageBox.information(self, Language.getLanguageByEnum(LanguageList.MSG_DISKTOOL_CREATED_TITLE), Language.getLanguageByEnum(LanguageList.MSG_DISKTOOL_CREATED_DESC) + diskLoc + Language.getLanguageByEnum(LanguageList.MSG_DISKTOOL_CREATED_DESC_2))
        except:
            msg = QMessageBox(self)
            msg.setWindowTitle(Language.getLanguageByEnum(LanguageList.MSG_DISKTOOL_CREATE_FAILURE_TITLE))
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowIcon(QIcon('src/png/icons/remove128.png'))
            msg.setText(Language.getLanguageByEnum(LanguageList.MSG_DISKTOOL_CREATE_FAILURE_DESC))
            msg.setDetailedText(f'{traceback.format_exc()}')
            msg.exec()