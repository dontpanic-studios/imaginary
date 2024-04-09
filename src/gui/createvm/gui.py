from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit, QFileDialog
from PyQt6.QtGui import QIcon
from PyQt6 import QtCore
from src.gui.label import whynotclick
import os, sys, logging, json

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

            self.setWindowTitle("Create VM")
            self.setStyleSheet("background-color: #262626;") 
            self.setWindowIcon(QIcon('./src/png/icons/128.png'))
            self.setGeometry(self.top, self.left, self.width, self.height)
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
        self.label_Title = QLabel('Create QEMU VM', self)
        self.label_InputLabel = QLabel('VM Name', self)
        self.label_InputLabel_desc = QLabel('VM Description', self)

        self.label_createVM = whynotclick.Label(self)
        self.label_createVM.setText('Save')
        self.label_loadISO = whynotclick.Label(self)
        self.label_loadISO.setText('Select ISO Location..')

        self.Input_VMName = QLineEdit(self)
        self.Input_VMDesc = QLineEdit(self)

        # font
        font_bold_title = self.label_Title.font()
        font_bold_title.setBold(True)
        font_bold_title.setPointSize(30)
        font_bold_title.setFamily('Figtree')

        font_bold = self.label_Title.font()
        font_bold.setBold(True)
        font_bold.setPointSize(20)
        font_bold.setFamily('Figtree')

        font_button = self.label_Title.font()
        font_button.setBold(True)
        font_button.setPointSize(15)
        font_button.setFamily('Figtree')      

        self.label_Title.move(20, 15)
        self.label_InputLabel.move(20, 100)
        self.label_createVM.move(550, 430)
        self.Input_VMName.move(20, 130)
        self.label_InputLabel_desc.move(20, 170)
        self.Input_VMDesc.move(20, 200)

        self.label_Title.setFont(font_bold_title)
        self.Input_VMName.setFont(font_button)
        self.label_createVM.setFont(font_bold)
        self.label_InputLabel.setFont(font_button)
        self.label_InputLabel_desc.setFont(font_button)
        self.Input_VMDesc.setFont(font_button)

        self.label_Title.setStyleSheet("Color : white;")
        self.Input_VMName.setStyleSheet("Color : white;")
        self.label_createVM.setStyleSheet("Color : white;")
        self.label_InputLabel_desc.setStyleSheet("Color : white;")
        self.Input_VMDesc.setStyleSheet("Color : white;")
        self.label_loadISO.setStyleSheet("Color : white;")
        self.label_InputLabel.setStyleSheet("Color : white;")

        self.label_createVM.adjustSize()
        self.label_InputLabel.adjustSize()
        self.label_Title.adjustSize()
        self.label_InputLabel_desc.adjustSize()

        self.Input_VMName.setPlaceholderText('eg) Windows 11')
        self.Input_VMDesc.setPlaceholderText('eg) wow!!')

        self.label_createVM.clicked.connect(self.saveChange)
        self.label_loadISO.clicked.connect(self.loadISO)

    def saveChange(self):
        metadata = {
            'vm_name': self.Input_VMName.text(),
            'desc': self.Input_VMDesc.text(),
            'iso_loc': self.label_loadISO.text(),
            'max_core': 1,
            'max_mem': 1,
            'disk_loc': f'.\\src\\vm\\{self.Input_VMName.text()}.qcow2',
            'project': f'.\\src\\vm\\{self.Input_VMName.text()}'
        }
        print(f'vm setting: \n{metadata}')

        if not os.path.exists(f'./src/vm/{metadata['vm_name']}'):
            os.makedirs(f'./src/vm/{metadata['vm_name']}')
            with open(metadata['project'] + '\\metadata.json', 'w+') as f:
                try:
                    for i in metadata['vm_name']:
                        if(i == '!' or i == '?' or i == '/' or i == ',' or i == '.' or i == '<' or i == '>'):
                            self.label_InputLabel.setText('VM Name cannot contain "!", "?", ".", ",", "<", ">"')
                            self.label_InputLabel.setStyleSheet('Color : red;')

                    json.dump(metadata, f)
                    f.close()    
                    self.close()        

                except FileExistsError:
                    log.critical('File already exists.')
                    self.label_InputLabel.setText('VM already Exists!')
                    self.label_InputLabel.setStyleSheet('Color : red;')
                f.close()
        else:
            msgbox_vmExist = QMessageBox.warning(self, 'VM Project Folder Exists!', 'vm already exist')

    def loadISO(self):
        fname = QFileDialog.getOpenFileName(self)        

        if fname[0]:
            if(fname[0] != ''):
                self.label_loadISO.setText(fname[0])
        else:
            log.info('canceled')