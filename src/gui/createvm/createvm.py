from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit, QFileDialog, QCheckBox, QComboBox, QRadioButton
from PyQt6.QtGui import QIcon
from PyQt6 import QtCore
from src.gui.label import whynotclick
import os, sys, logging, json, subprocess, traceback
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

            self.setWindowTitle("VM Setup Wizard")
            self.setStyleSheet("background-color: #262626; Color : white;") 
            self.setWindowIcon(QIcon('src/png/icons/128.png'))
            self.setFixedSize(self.width, self.height)
            self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint)
            self.initUI()
            self.frame1()
            log.info('initallized.')
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.critical(f"ERROR Occurred!\nLog: {exc_type}, {exc_obj}, {exc_tb}, {fname}")
            errInfoWinInit = QMessageBox.critical(self, '오류가 발생하였습니다.', '재설정을 하는 중에 오류가 발생했습니다.\n보통 프로그램이 꼬였거나, 저장된 위치에 한글이 들어있으면 안되는 경우가 있습니다.')
            log.critical('failed to intiallized window')

    def initUI(self):
        self.experimental_GPUType_List = ['virtio-gpu', 'qxl', 'isa-vga', 'vmware-svga', 'none', 'virtio-gpu-gl']
        self.experimental_VMType_List = ['x86_64', 'arm', 'aarch64', 'i386', 'ppc', 'riscv32', 'riscv64']

        self.label_Title = QLabel('Setup your VM', self)
        self.label_InputLabel = QLabel('VM Name', self)
        self.label_InputLabel_disk = QLabel('Disk Size', self)
        self.label_InputLabel_desc = QLabel('VM Description', self)

        self.label_createVM = whynotclick.Label(self)
        self.label_createVM.setText('Save')
        self.label_loadISO = whynotclick.Label(self)
        self.label_turnFrameBack = whynotclick.Label(self)
        self.label_turnFrameBack.setText('Back')
        self.label_loadISO_title = QLabel('Load ISO File', self)
        self.label_loadISO.setText('Select ISO Location..')
        self.label_RamSize = QLabel('RAM Size', self)
        self.label_VGAMemSize= QLabel('Virtual GPU Memory Size (Mb)', self)
        self.label_GPUType = QLabel('Select GPU Type', self)
        self.label_DiskType = QLabel('Select Disk Type', self)
        self.label_SysCoreSize = QLabel('CPU Core Size', self)

        self.Input_VMName = QLineEdit(self)
        self.Input_VMDesc = QLineEdit(self)
        self.Input_DiskSize = QLineEdit(self)
        self.Input_RamSize = QLineEdit(self)
        self.Input_VGAMemSize = QLineEdit(self)        
        self.experimental_Input_StartupArg = QLineEdit(self)
        self.Input_SysCoreSize = QLineEdit(self)

        self.experimental_HAX_Accel = QCheckBox(self)
        self.experimental_HAX_Accel.setText('Lab: Enable TCG (Tiny Code Generator)')
        self.whybutdontcreatedisk = QCheckBox(self, text='Skip Disk Creation')
        self.experimental_OpenGL_Accel = QCheckBox(self)
        self.experimental_OpenGL_Accel.setText('Add Driver Disk to VM') 
        
        self.experimental_GPUType = QComboBox(self)
        #self.experimental_VMType = QComboBox(self)

        self.diskType_RAW = QRadioButton(self)
        self.diskType_RAW.setText('RAW : RAW Disk image format, size of image is big but pretty fast')
        self.diskType_QCOW2 = QRadioButton(self)
        self.diskType_QCOW2.setText('QCow2 : QEMU image format v2, the most versatile format.')
        self.diskType_VHDX = QRadioButton(self)
        self.diskType_VHDX.setText('VMDK : Hyper-V Compatible image format, ...you want more?')

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

        font_radio = self.label_Title.font()
        font_radio.setBold(True)
        font_radio.setPointSize(int(13.5))
        font_radio.setFamily(os.environ.get('Font'))    

        self.label_Title.move(20, 15)
        self.label_InputLabel.move(20, 80)
        self.label_createVM.move(550, 430)
        self.label_turnFrameBack.move(450, 430)
        self.Input_VMName.move(20, 110)
        self.label_InputLabel_desc.move(300, 80)
        self.Input_VMDesc.move(300, 110)
        self.label_loadISO_title.move(20, 145)
        self.label_loadISO.move(19, 170)
        self.label_InputLabel_disk.move(300, 210)
        self.Input_DiskSize.move(300, 240)
        self.Input_RamSize.move(20, 240)
        self.label_RamSize.move(20, 210)
        self.experimental_HAX_Accel.move(20, 355)
        self.experimental_GPUType.move(20, 315)
        self.label_GPUType.move(20, 285)
        self.Input_VGAMemSize.move(300, 315)
        self.label_VGAMemSize.move(300, 285)
        self.experimental_Input_StartupArg.move(20, 395)
        self.whybutdontcreatedisk.move(20, 420)
        self.Input_SysCoreSize.move(300, 240)
        self.label_SysCoreSize.move(300, 210)

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
        self.Input_SysCoreSize.setFont(font_button)
        self.experimental_Input_StartupArg.setFont(font_button)
        self.whybutdontcreatedisk.setFont(font_button)
        self.experimental_OpenGL_Accel.setFont(font_button)
        self.label_turnFrameBack.setFont(font_bold)
        self.diskType_VHDX.setFont(font_radio)
        self.diskType_QCOW2.setFont(font_radio)
        self.diskType_RAW.setFont(font_radio)
        self.label_DiskType.setFont(font_button)
        self.label_SysCoreSize.setFont(font_button)

        self.label_Title.setStyleSheet("Color : white;")
        self.Input_VMName.setStyleSheet("Color : white;")
        self.label_createVM.setStyleSheet("Color : white;")
        self.label_InputLabel_desc.setStyleSheet("Color : white;")
        self.Input_VMDesc.setStyleSheet("Color : white;")
        self.label_loadISO.setStyleSheet("Color : white;")
        self.label_InputLabel.setStyleSheet("Color : white;")
        self.label_loadISO.setStyleSheet("Color : #4aa4ff;")
        self.label_loadISO_title.setStyleSheet("Color : white;")
        self.label_InputLabel_disk.setStyleSheet("Color : white;")
        self.Input_DiskSize.setStyleSheet("Color : white;")
        self.experimental_OpenGL_Accel.setStyleSheet("Color : white;")
        self.label_RamSize.setStyleSheet("Color : white;")
        self.Input_RamSize.setStyleSheet("Color : white;")
        self.Input_VGAMemSize.setStyleSheet("Color : white;")
        self.experimental_HAX_Accel.setStyleSheet("Color : white;")
        self.label_VGAMemSize.setStyleSheet("Color : white;")
        self.experimental_GPUType.setStyleSheet("Color : white;")
        self.label_GPUType.setStyleSheet("Color : white;")
        self.experimental_Input_StartupArg.setStyleSheet("Color : white;")
        self.whybutdontcreatedisk.setStyleSheet("Color : white;")
        self.label_turnFrameBack.setStyleSheet("Color : #4E4F50;")
        self.diskType_QCOW2.setStyleSheet("Color : white;")
        self.diskType_RAW.setStyleSheet("Color : white;")
        self.diskType_VHDX.setStyleSheet("Color : white;")
        self.Input_SysCoreSize.setStyleSheet("Color : white;")
        self.label_SysCoreSize.setStyleSheet("Color : white;")

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
        self.experimental_OpenGL_Accel.adjustSize()
        self.Input_RamSize.adjustSize()
        self.label_RamSize.adjustSize()
        self.experimental_HAX_Accel.adjustSize()
        self.Input_VGAMemSize.adjustSize()
        self.Input_VGAMemSize.adjustSize()
        self.label_VGAMemSize.adjustSize()
        self.experimental_GPUType.adjustSize()
        self.label_GPUType.adjustSize()
        self.experimental_Input_StartupArg.adjustSize()
        self.whybutdontcreatedisk.adjustSize()
        self.label_turnFrameBack.adjustSize()
        self.Input_SysCoreSize.adjustSize()
        self.label_SysCoreSize.adjustSize()

        self.Input_VMName.setPlaceholderText('eg) Windows 11')
        self.Input_VMDesc.setPlaceholderText('eg) Description Text')
        self.Input_DiskSize.setPlaceholderText('eg) 64G')
        self.Input_RamSize.setPlaceholderText('eg) 4G')
        self.Input_VGAMemSize.setPlaceholderText('1 ~ 256')
        self.Input_SysCoreSize.setPlaceholderText('eg) 2')
        self.experimental_Input_StartupArg.setPlaceholderText('Startup Arguments')
        self.label_loadISO.clicked.connect(self.loadISO)

        self.experimental_GPUType.addItems(self.experimental_GPUType_List)

    def saveChange(self):
        metadata = {
            'metadata_ver': os.environ.get('Ver'),
            'vm_name': self.Input_VMName.text(),
            'vm_type': 'unknown',
            'desc': self.Input_VMDesc.text(),
            'iso_loc': self.label_loadISO.text(),
            'max_core': self.Input_SysCoreSize.text(),
            'max_mem': self.Input_RamSize.text(),
            'disk': {
                'disk_size': self.Input_DiskSize.text(),
                'disk_loc': f'.\\src\\vm\\{self.Input_VMName.text()}\\{self.Input_VMName.text()}.img',
                'disk_type': ''
            },
            'project': f'.\\src\\vm\\{self.Input_VMName.text()}',
            'snapshot': f'.\\src\\vm\\{self.Input_VMName.text()}\\snapshot.png',
            'isaccel' : {
                'bool': self.experimental_HAX_Accel.isChecked(),
                'acceltype': 'tcg',
            },
            'vga': {
                'mem': self.Input_VGAMemSize.text(),
                'type': self.experimental_GPUType.currentText()
            },
            'audio': {
                'type': 'ac97'
            },
            'addition': {
                'args': self.experimental_Input_StartupArg.text()
            }
        }
        print(f'vm setting: \n{metadata}')

        if metadata['isaccel']['bool'] == True:
            msg = QMessageBox.warning(self, '실험적 기능 켜짐', '경고!\n\n하드웨어 가상화가 켜져있습니다!\n해당 기능은 특정 기기에서 작동이 안될수 있습니다!')
        if metadata['vga']['type'] != 'virtio-gpu' or 'virtio-gpu-gl':
            msg = QMessageBox.warning(self, '저속 그래픽 사용', 'virtio-gpu 그래픽과 달리 저속 그래픽 세팅을 사용하고 있습니다!\n가상머신의 성능 저하가 있을수 있습니다.')
        if metadata['vga']['type'] == 'virtio-gpu' and metadata['vga']['mem'] != '':
            msg = QMessageBox.critical(self, '그래픽 메모리 지원 안됨', '선택한 그래픽 세팅은 메모리 변경이 불가능한 세팅입니다,\n"qxl" 또는 "isa-vga" 로 바꿔주세요.')    
            return
        if(self.diskType_QCOW2.isEnabled() == True and self.diskType_RAW.isEnabled() == False and self.diskType_VHDX.isEnabled() == False):
            metadata['disk']['disk_type'] = 'qcow2'
        elif(self.diskType_QCOW2.isEnabled() == False and self.diskType_RAW.isEnabled() == True and self.diskType_VHDX.isEnabled() == False):
            metadata['disk']['disk_type'] = 'raw' 
        else:
            metadata['disk']['disk_type'] = 'vhdx'   
        if self.experimental_OpenGL_Accel.isChecked() == True:
            metadata['addition']['args'] = self.experimental_Input_StartupArg.text() + ' -hdb fat:rw:src/vm/drivers/' 
        if not os.path.exists(f'src/vm/{metadata['vm_name']}'):
            os.mkdir(f'.\\src\\vm\\{metadata['vm_name']}')
            with open(metadata['project'] + '\\metadata.json', 'w+') as f:
                try:
                    for i in metadata['vm_name']:
                        if(i == '!' or i == '?' or i == '/' or i == ',' or i == '.' or i == '<' or i == '>'):
                            self.label_InputLabel.setText('VM Name cannot contain "!", "?", ".", ",", "<", ">"')
                            self.label_InputLabel.setStyleSheet('Color : red;') 
                            return
                        if metadata['vm_name'] in ['Win', 'win', 'Windows']:
                            metadata['vm_type'] == 'win'
                        else:
                            metadata['vm_type'] == 'unknown'
                    if(metadata['desc'] == ''):
                        metadata['desc'] = 'No Description Avaliable' 
                    if(metadata['disk']['disk_size'] == ''):
                        metadata['disk']['disk_size'] = 'No Disk Avaliable'           
                    json.dump(metadata, f, indent=3, sort_keys=True)
                    f.close()    
                    self.close()
                    try:
                        if self.whybutdontcreatedisk.isChecked() == False:
                            process = subprocess.check_call(f'cd src/qemu & qemu-img create -f {metadata['disk']['disk_type']} -o size={metadata['disk']["disk_size"]} "{metadata['vm_name']}.img" & qemu-img info "{metadata["vm_name"]}.img"', shell=True)  
                            os.rename(f'src/qemu/{metadata['vm_name']}.img', metadata['disk']['disk_loc'])
                    except:
                        findUpdateMsg = QMessageBox(self)
                        findUpdateMsg.setIcon(QMessageBox.Icon.Critical)
                        findUpdateMsg.setWindowIcon(QIcon('src/png/icons/128.png'))
                        findUpdateMsg.setWindowTitle('우리는평화를원한다')
                        findUpdateMsg.setText(f'Imaginary가 가상머신을 생성중에 오류가 발생했다고 판단했습니다.\nShow Details... 를 눌러 자세한 정보를 확인가능합니다.')
                        findUpdateMsg.setDetailedText(f'{traceback.format_exc()}')
                        findUpdateMsg.exec()   
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
            
    def frame1(self): # general
        print("Frame1 On, Frame 2 Off")
        self.label_InputLabel.setHidden(False)
        self.label_InputLabel_desc.setHidden(False)
        self.label_loadISO.setHidden(False)
        self.Input_VMDesc.setHidden(False)
        self.label_SysCoreSize.setHidden(False)
        self.experimental_OpenGL_Accel.setHidden(True)
        self.Input_SysCoreSize.setHidden(False)
        self.Input_VMName.setHidden(False)
        self.label_loadISO_title.setHidden(False)
        self.label_InputLabel_disk.setHidden(True)
        self.Input_DiskSize.setHidden(True)
        self.Input_RamSize.setHidden(False)
        self.label_RamSize.setHidden(False)
        self.experimental_HAX_Accel.setHidden(True)
        self.Input_VGAMemSize.setHidden(True)
        self.Input_VGAMemSize.setHidden(True)
        self.label_VGAMemSize.setHidden(True)
        self.experimental_GPUType.setHidden(True)
        self.label_GPUType.setHidden(True)
        self.experimental_Input_StartupArg.setHidden(True)
        self.diskType_QCOW2.setHidden(True)
        self.diskType_VHDX.setHidden(True)
        self.diskType_RAW.setHidden(True)
        self.label_DiskType.setHidden(True)
        self.whybutdontcreatedisk.setHidden(True)

        self.label_Title.setText('General Setup')
        self.label_createVM.clicked.connect(self.frame3)
        self.label_createVM.setText('Next')

    def frame2(self): # etc type
        print("Frame1 Off, Frame 2 On")
        self.label_Title.setText('Others')

        self.label_InputLabel.setHidden(True)
        self.Input_SysCoreSize.setHidden(True)
        self.experimental_OpenGL_Accel.setHidden(False)
        self.label_SysCoreSize.setHidden(True)
        self.label_InputLabel_desc.setHidden(True)
        self.label_loadISO.setHidden(True)
        self.Input_VMDesc.setHidden(True)
        self.Input_VMName.setHidden(True)
        self.label_loadISO_title.setHidden(True)
        self.label_InputLabel_disk.setHidden(True)
        self.Input_DiskSize.setHidden(True)
        self.Input_RamSize.setHidden(True)
        self.label_RamSize.setHidden(True)
        self.experimental_HAX_Accel.setHidden(False)
        self.Input_VGAMemSize.setHidden(False)
        self.Input_VGAMemSize.setHidden(False)
        self.label_VGAMemSize.setHidden(False)
        self.experimental_GPUType.setHidden(False)
        self.label_GPUType.setHidden(False)
        self.experimental_Input_StartupArg.setHidden(False)
        self.whybutdontcreatedisk.setHidden(True)
        self.label_DiskType.setHidden(True)
        self.diskType_QCOW2.setHidden(True)
        self.diskType_RAW.setHidden(True)
        self.diskType_VHDX.setHidden(True)
        self.whybutdontcreatedisk.setHidden(True)

        self.label_Title.move(20, 15)
        self.label_InputLabel.move(20, 80)
        self.label_createVM.move(520, 430)
        self.Input_VMName.move(20, 110)
        self.label_InputLabel_desc.move(300, 80)
        self.Input_VMDesc.move(300, 110)
        self.label_loadISO_title.move(20, 145)
        self.label_loadISO.move(19, 170)
        self.label_InputLabel_disk.move(300, 210)
        self.Input_DiskSize.move(300, 240)
        self.Input_RamSize.move(20, 240)
        self.label_RamSize.move(20, 210)
        self.experimental_HAX_Accel.move(20, 150)
        self.experimental_GPUType.move(20, 115)
        self.label_GPUType.move(20, 80)
        self.Input_VGAMemSize.move(300, 115)
        self.label_VGAMemSize.move(300, 80)
        self.experimental_Input_StartupArg.move(20, 395)
        self.whybutdontcreatedisk.move(20, 417) 
        self.experimental_OpenGL_Accel.move(20, 190)

        self.label_createVM.clicked.connect(self.saveChange)
        self.label_createVM.setText("Create")
        self.label_createVM.adjustSize()
        self.label_turnFrameBack.clicked.connect(self.frame3)
        self.label_turnFrameBack.setStyleSheet("Color : white;")

    def frame3(self): # disk
        print("Frame2 Off, Frame 3 On")
        self.label_Title.setText('Disk Setup')

        self.label_InputLabel.setHidden(True)
        self.label_InputLabel_desc.setHidden(True)
        self.label_loadISO.setHidden(True)
        self.experimental_OpenGL_Accel.setHidden(True)
        self.label_SysCoreSize.setHidden(True)
        self.Input_SysCoreSize.setHidden(True)
        self.Input_VMDesc.setHidden(True)
        self.Input_VMName.setHidden(True)
        self.label_loadISO_title.setHidden(True)
        self.whybutdontcreatedisk.setHidden(False)
        self.label_InputLabel_disk.setHidden(False)
        self.Input_DiskSize.setHidden(False)
        self.Input_RamSize.setHidden(True)
        self.label_RamSize.setHidden(True)
        self.experimental_HAX_Accel.setHidden(True)
        self.Input_VGAMemSize.setHidden(True)
        self.Input_VGAMemSize.setHidden(True)
        self.label_VGAMemSize.setHidden(True)
        self.experimental_GPUType.setHidden(True)
        self.label_GPUType.setHidden(True)
        self.experimental_Input_StartupArg.setHidden(True)
        self.whybutdontcreatedisk.setHidden(False)
        self.label_DiskType.setHidden(False)
        self.diskType_QCOW2.setHidden(False)
        self.diskType_RAW.setHidden(False)
        self.diskType_VHDX.setHidden(False)
        self.label_DiskType.setHidden(False)

        self.diskType_RAW.move(20, 120)
        self.diskType_QCOW2.move(20, 145)
        self.diskType_VHDX.move(20, 170)
        self.label_DiskType.move(20, 90)
        self.Input_DiskSize.move(20, 250)
        self.label_InputLabel_disk.move(20, 220)

        self.label_createVM.clicked.connect(self.frame2)
        self.label_createVM.setText("Next")
        self.label_createVM.adjustSize()
        self.label_turnFrameBack.clicked.connect(self.frame1)
        self.label_turnFrameBack.setStyleSheet("Color : white;")    