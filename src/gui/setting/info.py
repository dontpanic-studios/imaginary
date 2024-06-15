from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QComboBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6 import QtCore
import os, logging, dotenv, traceback
from src.language.lang import Language, LanguageList
from dotenv import load_dotenv

log = logging
logFilePath = './log/debug-log.log'
load_dotenv('./data/setting.env')
file = dotenv.find_dotenv('data/setting.env')

class CreateVM(QWidget):
    def __init__(self):
        log.info('trying initallizing frame..')
        try:
            super().__init__()

            self.setWindowTitle("Info")
            self.setStyleSheet("background-color: #262626; Color: white;") 
            self.setWindowIcon(QIcon('./src/png/icons/128.png'))
            self.setFixedSize(640, 200)
            self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint)
            self.initUI()
            log.info('initallized.')
        except:
            errInfoWinInit = QMessageBox(self)
            errInfoWinInit.setWindowTitle(Language.getLanguageByEnum(LanguageList.MSG_VAR_TITLE))
            errInfoWinInit.setText(Language.getLanguageByEnum(LanguageList.MSG_VAR_DESC))
            errInfoWinInit.setDetailedText(traceback.format_exc())

            log.critical('failed to intiallized window')

    def initUI(self):
        self.languages = ['en_US', 'ko_KR']
        self.label_Logo = QLabel(self)
        self.label_InfoTitle = QLabel("Imaginary", self)
        self.label_Version = QLabel(f"{os.environ.get('Ver')}\nOpen-source QEMU GUI Wrapper", self)
        self.label_Logo.setPixmap(QPixmap('./src/png/icons/128.png')) 

        self.enableLabSetting = QComboBox(self)
        self.enableLabSetting.addItems(self.languages)

        self.font_bold_title = self.label_InfoTitle.font()
        self.font_bold_title.setBold(True)
        self.font_bold_title.setPointSize(30)
        self.font_bold_title.setFamily(os.environ.get('Font'))

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
        self.label_Version.move(150, 65)
        self.enableLabSetting.move(15, 150)

        self.label_InfoTitle.setFont(self.font_bold_title)
        self.label_InfoTitle.setStyleSheet("Color : white; background-color: #262626;")
        self.label_Version.setFont(self.font_bold)
        self.label_Version.setStyleSheet("Color : white; background-color: #262626;")
        self.enableLabSetting.setFont(self.font_smol)
        self.enableLabSetting.setStyleSheet("Color : white; background-color: #262626;")        

        self.label_Logo.adjustSize()
        self.label_InfoTitle.adjustSize()
        self.label_Version.adjustSize()

        self.enableLabSetting.setCurrentText(os.environ.get("Language"))

    def closeEvent(self, event):
        if os.environ.get("Language") != self.enableLabSetting.currentText():
            try:
                dotenv.set_key(file, "Language", self.enableLabSetting.currentText())
                inf = QMessageBox.information(self, Language.getLanguageByEnum(LanguageList.MSG_INFO_LANGUAGE_SAVED_TITLE), Language.getLanguageByEnum(LanguageList.MSG_INFO_LANGUAGE_SAVED_DESC))
            except (FileNotFoundError, SystemError,  PermissionError) as e:
                print('failed to read metadata, is file even?')    
                failReadData = QMessageBox(self)
                failReadData.setWindowTitle(Language.getLanguageByEnum(LanguageList.MSG_INFO_LANGUAGE_SAVE_FAIL_TITLE))
                failReadData.setIcon(QMessageBox.Icon.Critical)
                failReadData.setWindowIcon(QIcon('src/png/icons/remove128.png'))
                if e == SystemError:
                    failReadData.setText(Language.getLanguageByEnum(LanguageList.MSG_INFO_LANGUAGE_SAVE_FAIL_SYSTEM))
                elif e == PermissionError:
                    failReadData.setText(Language.getLanguageByEnum(LanguageList.MSG_INFO_LANGUAGE_SAVE_FAIL_PERMISSION))
                else:
                    failReadData.setText(Language.getLanguageByEnum(LanguageList.MSG_INFO_LANGUAGE_SAVE_FAIL_NOFILEFOUND))
                failReadData.setDetailedText(f'{traceback.format_exc()}')
                failReadData.exec()    
                return
        else:
            print("No Data has been changed.")

    def checkLangFiles(self):
        for f in os.listdir('./data/language/'):
            if f.endswith('.lgf'):
                self.languages.append(f)
        print("Detected Language list: " + self.languages)       