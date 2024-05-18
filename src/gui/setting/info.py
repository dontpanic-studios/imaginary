from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QComboBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6 import QtCore
import os, sys, logging, dotenv, traceback
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
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.critical(f"ERROR Occurred!\nLog: {exc_type}, {exc_obj}, {exc_tb}, {fname}")
            errInfoWinInit = QMessageBox.critical(self, '오류가 발생하였습니다.', '재설정을 하는 중에 오류가 발생했습니다.\n보통 프로그램이 꼬였거나, 저장된 위치에 한글이 들어있으면 안되는 경우가 있습니다.')
            log.critical('failed to intiallized window')

    def initUI(self):
        self.label_Logo = QLabel(self)
        self.label_InfoTitle = QLabel("Imaginary", self)
        self.label_Version = QLabel(f"{os.environ.get('Ver')}\nOpen-source QEMU GUI Tool", self)
        self.label_Logo.setPixmap(QPixmap('./src/png/icons/128.png')) 

        self.enableLabSetting = QComboBox(self)
        self.enableLabSetting.addItems(['en_US', 'ko_KR'])

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
        self.label_Version.move(150, 65)
        self.enableLabSetting.move(15, 150)

        self.label_InfoTitle.setFont(font_bold_title)
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
                inf = QMessageBox.information(self, "언어 저장됨", "프로그램을 재시작하여 언어 변경을 완료하세요.")
            except (FileNotFoundError, SystemError,  PermissionError) as e:
                print('failed to read metadata, is file even?')    
                failReadData = QMessageBox(self)
                failReadData.setWindowTitle('데이터 저장 실패')
                failReadData.setIcon(QMessageBox.Icon.Critical)
                failReadData.setWindowIcon(QIcon('src/png/icons/remove128.png'))
                if e == SystemError:
                    failReadData.setText('가상머신 정보를 읽는데 실패하였습니다.\n\nSystemError, 시스템 상으로 오류가 발생했습니다.')
                elif e == PermissionError:
                    failReadData.setText('가상머신 정보를 읽는데 실패하였습니다.\n\nNo Permission, Imaginary가 데이터를 쓰는데 권한이 부족합니다.')
                else:
                    failReadData.setText('가상머신 정보를 읽는데 실패하였습니다.\n\nFile Cannot be found, Imaginary가 파일을 찾을수 없습니다.')
                failReadData.setDetailedText(f'{traceback.format_exc()}')
                failReadData.exec()    
                return
        else:
            print("No Data has been changed.")