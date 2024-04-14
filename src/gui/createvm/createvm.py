from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit, QFileDialog, QCheckBox, QComboBox
from PyQt6.QtGui import QIcon
from PyQt6 import QtCore
from src.gui.label import whynotclick
import os, sys, logging, json, subprocess
from dotenv import load_dotenv

log = logging
logFilePath = './log/debug-log.log'
load_dotenv('./data/setting.env')

class CreateVM(QWidget):
    def __init__(self):
        log.info('trying initallizing frame..')
        try:
            super().__init__()

            self.width = 640
            self.height = 480

            self.setWindowTitle("Create VM")
            self.setStyleSheet("background-color: #262626; Color : white;") 
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
        self.experimental_GPUType_List = ['qxl', 'virtio-gpu', 'isa-vga']
        self.label_Title = QLabel('Create QEMU VM', self)
        self.label_InputLabel = QLabel('VM Name', self)
        self.label_InputLabel_disk = QLabel('Disk Size', self)
        self.label_InputLabel_desc = QLabel('VM Description', self)

        self.label_createVM = whynotclick.Label(self)
        self.label_createVM.setText('Save')
        self.label_loadISO = whynotclick.Label(self)
        self.label_loadISO_title = QLabel('Load ISO File', self)
        self.label_loadISO.setText('Select ISO Location..')
        self.label_RamSize = QLabel('RAM Size', self)
        self.label_VGAMemSize= QLabel('Virtual GPU Memory Size (Mb)', self)
        self.label_GPUType = QLabel('Select GPU Type', self)

        self.Input_VMName = QLineEdit(self)
        self.Input_VMDesc = QLineEdit(self)
        self.Input_DiskSize = QLineEdit(self)
        self.Input_RamSize = QLineEdit(self)
        self.Input_VGAMemSize = QLineEdit(self)        

        self.experimental_HAX_Accel = QCheckBox(self)
        self.experimental_HAX_Accel.setText('EXPERIMENTAL : Enable HAXM')
        #self.experimental_OpenGL_Accel = QCheckBox(self)
        #self.experimental_OpenGL_Accel.setText('EXPERIMENTAL : Enable OpenGL (Linux Only)') 
        self.experimental_GPUType = QComboBox(self)

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
        font_button.setPointSize(15)
        font_button.setFamily(os.environ.get('Font'))      

        self.label_Title.move(20, 15)
        self.label_InputLabel.move(20, 100)
        self.label_createVM.move(550, 430)
        self.Input_VMName.move(20, 130)
        self.label_InputLabel_desc.move(300, 100)
        self.Input_VMDesc.move(300, 127)
        self.label_loadISO_title.move(20, 170)
        self.label_loadISO.move(19, 195)
        self.label_InputLabel_disk.move(300, 240)
        self.Input_DiskSize.move(300, 270)
        self.Input_RamSize.move(20, 270)
        self.label_RamSize.move(20, 240)
        self.experimental_HAX_Accel.move(20, 380)
        self.experimental_GPUType.move(20, 340)
        self.label_GPUType.move(20, 310)
        self.Input_VGAMemSize.move(300, 340)
        self.label_VGAMemSize.move(300, 310)

        self.label_Title.setFont(font_bold_title)
        self.Input_VMName.setFont(font_button)
        self.label_createVM.setFont(font_bold)
        self.label_InputLabel.setFont(font_button)
        self.label_InputLabel_desc.setFont(font_button)
        self.Input_VMDesc.setFont(font_button)
        self.label_loadISO.setFont(font_bold)
        self.label_loadISO_title.setFont(font_button)
        self.label_InputLabel_disk.setFont(font_button)
        self.Input_DiskSize.setFont(font_button)
        self.label_RamSize.setFont(font_button)
        self.Input_RamSize.setFont(font_button)
        self.experimental_HAX_Accel.setFont(font_button)
        self.Input_VGAMemSize.setFont(font_button)
        self.label_VGAMemSize.setFont(font_button)
        self.experimental_GPUType.setFont(font_button)
        self.label_GPUType.setFont(font_button)

        self.label_Title.setStyleSheet("Color : white;")
        self.Input_VMName.setStyleSheet("Color : white;")
        self.label_createVM.setStyleSheet("Color : white;")
        self.label_InputLabel_desc.setStyleSheet("Color : white;")
        self.Input_VMDesc.setStyleSheet("Color : white;")
        self.label_loadISO.setStyleSheet("Color : white;")
        self.label_InputLabel.setStyleSheet("Color : white;")
        self.label_loadISO.setStyleSheet("Color : white;")
        self.label_loadISO_title.setStyleSheet("Color : white;")
        self.label_InputLabel_disk.setStyleSheet("Color : white;")
        self.Input_DiskSize.setStyleSheet("Color : white;")
        self.label_RamSize.setStyleSheet("Color : white;")
        self.Input_RamSize.setStyleSheet("Color : white;")
        self.Input_VGAMemSize.setStyleSheet("Color : white;")
        self.experimental_HAX_Accel.setStyleSheet("Color : white;")
        self.label_VGAMemSize.setStyleSheet("Color : white;")
        self.experimental_GPUType.setStyleSheet("Color : white;")
        self.label_GPUType.setStyleSheet("Color : white;")

        self.label_createVM.adjustSize()
        self.label_InputLabel.adjustSize()
        self.label_Title.adjustSize()
        self.label_InputLabel_desc.adjustSize()
        self.label_loadISO.adjustSize()
        self.Input_VMDesc.adjustSize()
        self.Input_VMName.adjustSize()
        self.label_loadISO_title.adjustSize()
        self.label_InputLabel_disk.adjustSize()
        self.Input_DiskSize.adjustSize()
        self.Input_RamSize.adjustSize()
        self.label_RamSize.adjustSize()
        self.experimental_HAX_Accel.adjustSize()
        self.Input_VGAMemSize.adjustSize()
        self.Input_VGAMemSize.adjustSize()
        self.label_VGAMemSize.adjustSize()
        self.experimental_GPUType.adjustSize()
        self.label_GPUType.adjustSize()

        self.Input_VMName.setPlaceholderText('eg) Windows 11')
        self.Input_VMDesc.setPlaceholderText('eg) Description Text')
        self.Input_DiskSize.setPlaceholderText('eg) 64G')
        self.Input_RamSize.setPlaceholderText('eg) 4G')
        self.Input_VGAMemSize.setPlaceholderText('1 ~ 256')

        self.label_createVM.clicked.connect(self.saveChange)
        self.label_loadISO.clicked.connect(self.loadISO)

        self.experimental_GPUType.addItems(self.experimental_GPUType_List)

    def saveChange(self):
        metadata = {
            'metadata_ver': os.environ.get('Ver'),
            'vm_name': self.Input_VMName.text(),
            'desc': self.Input_VMDesc.text(),
            'iso_loc': self.label_loadISO.text(),
            'max_core': 2,
            'max_mem': self.Input_RamSize.text(),
            'disk_size': self.Input_DiskSize.text(),
            'disk_loc': f'.\\src\\vm\\{self.Input_VMName.text()}\\{self.Input_VMName.text()}.img',
            'project': f'.\\src\\vm\\{self.Input_VMName.text()}',
            'snapshot': f'.\\src\\vm\\{self.Input_VMName.text()}\\snapshot.png',
            'isaccel' : {
                'bool': self.experimental_HAX_Accel.isChecked(),
                'acceltype': 'tcg'
            },
            'vga': {
                'mem': self.Input_VGAMemSize.text(),
                'type': self.experimental_GPUType.currentText()
            },
            'addition': {
                'args': ''
            }
        }
        print(f'vm setting: \n{metadata}')

        if metadata['isaccel']['bool'] == True:
            msg = QMessageBox.warning(self, '실험적 기능 켜짐', '경고!\n\n실험적 기능인 하드웨어 가상화가 켜져있습니다.\n이 기능은 오직 Intel(Windows) 에서만 작동하며,\nHAXM이 설치된 상태에서 실행이 되어야합니다.')
        if not os.path.exists(f'src/vm/{metadata['vm_name']}'):
            os.mkdir(f'.\\src\\vm\\{metadata['vm_name']}')
            with open(metadata['project'] + '\\metadata.json', 'w+') as f:
                try:
                    for i in metadata['vm_name']:
                        if(i == '!' or i == '?' or i == '/' or i == ',' or i == '.' or i == '<' or i == '>'):
                            self.label_InputLabel.setText('VM Name cannot contain "!", "?", ".", ",", "<", ">"')
                            self.label_InputLabel.setStyleSheet('Color : red;')

                    json.dump(metadata, f, indent=3, sort_keys=True)
                    f.close()    
                    self.close()
                    subprocess.check_call(f'cd src/qemu & qemu-img create -f raw -o size={metadata["disk_size"]} "{metadata['vm_name']}.img" & qemu-img info "{metadata["vm_name"]}.img"', shell=True)  
                    os.rename(f'src/qemu/{metadata['vm_name']}.img', metadata['disk_loc'])
                except FileExistsError:
                    log.critical('File already exists.')
                    self.label_InputLabel.setText('VM already Exists!')
                    self.label_InputLabel.setStyleSheet('Color : red;')
                    self.label_InputLabel.adjustSize()
                f.close()
        else:
            msgbox_vmExist = QMessageBox.warning(self, '가상머신 존재', '생성할려는 가상머신은 이미 존재합니다!')

    def loadISO(self):
        fname = QFileDialog.getOpenFileName(self)        

        if fname[0]:
            if(fname[0] != ''):
                self.label_loadISO.setText(fname[0])
                self.label_loadISO.adjustSize()
        else:
            log.info('canceled')