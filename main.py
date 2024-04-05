from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot
import os, logging, sys, subprocess

log = logging
logFilePath = './log/debug-log.log'

try:
    print("Reading..")
    print(os.path.isfile(logFilePath))
    print("Setting up debug log..")
    log.basicConfig(format="[%(asctime)s] %(levelname)s:%(message)s", filename='./log/debug-log.log', level=logging.DEBUG, encoding="utf-8")
    print("Resetting..")
    f = open('./log/debug-log.log', 'w')
    f.close()
except FileNotFoundError:
    if os.path.isfile(logFilePath) == False:
        print("Logging file not exists, making...")
        try:
            f = open('./log/debug-log.log', 'w')
            f.close()
        except:
            print("An error occurred while writing log file.")
            print("It may the file exists or no permission to write file to location.")

class Main(QWidget):
    def __init__(self):
        log.info('trying initallizing main frame..')
        try:
            super().__init__()

            self.top = 200
            self.left = 500
            self.width = 1280
            self.height = 720

            self.setWindowTitle("Imaginary")
            self.setStyleSheet("background-color: #262626;") 
            self.setWindowIcon(QIcon('./src/png/icons/128.png'))
            self.setGeometry(self.top, self.left, self.width, self.height)
            self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint)
            self.setupWidget()
            log.info('initallized.')
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.critical(f"ERROR Occurred!\nLog: {exc_type}, {exc_obj}, {exc_tb}, {fname}")
            errInfoWinInit = QMessageBox.critical(self, '오류가 발생하였습니다.', '재설정을 하는 중에 오류가 발생했습니다.\n보통 프로그램이 꼬였거나, 저장된 위치에 한글이 들어있으면 안되는 경우가 있습니다.')
            log.critical('failed to intiallized window')

    def setupWidget(self):
        # label
        self.vm_background = QLabel(self)
        self.label_Title = QLabel("🌠 Imaginary", self)
        self.label_Vm_Title = QLabel("No VM has been found in Folder!", self)
        self.label_Vm_Desc = QLabel("Why don't you make one?", self)

        # image
        self.vm_background.setPixmap(QPixmap('./src/png/background/bg1.png'))

        # button
        self.createVM = QPushButton("Create VM", self)
        self.createVM.clicked.connect(self.showCreateVMWindow)

        # font
        font_bold = self.label_Title.font()
        font_bold.setBold(True)
        font_bold.setPointSize(20)
        font_bold.setFamily('Figtree')

        font_bold_title = self.label_Title.font()
        font_bold_title.setBold(True)
        font_bold_title.setPointSize(30)
        font_bold_title.setFamily('Figtree')

        self.label_Title.setFont(font_bold)
        self.label_Title.setStyleSheet("Color : white; background-color:#262626;")
        self.label_Vm_Title.setFont(font_bold_title)
        self.label_Vm_Title.setStyleSheet("Color : white; background-color:#2C2C2C;")
        self.label_Vm_Desc.setFont(font_bold)
        self.label_Vm_Desc.setStyleSheet("Color : white; background-color:#2C2C2C;")

        # widget move
        self.label_Title.move(15, 13)
        self.label_Vm_Title.move(350, 75)
        self.vm_background.move(320, 50)
        self.label_Vm_Desc.move(352, 120)
        self.createVM.move(320, 15)

    def openVmFolder(self):
        print('opening!')

    def runQemu(self, iso_loc, disk_loc, mem_size, sys_core):
        subprocess.run(f'./src/qemu/qemu.exe -enable-kvm -m {mem_size} -smp {sys_core} -cdrom {iso_loc} -hda {disk_loc} -vga qxl -device AC97 -netdev user,id=net0,net=192.168.0.0,dhcpstart=192.168.0.9')        

    def showCreateVMWindow(self):
        log.info("Opening CreateVM...")
        self.w = CreateVM()
        self.w.show()

class CreateVM(QWidget):
    def __init__(self):
        log.info('trying initallizing main frame..')
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
            log.info('initallized.')
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.critical(f"ERROR Occurred!\nLog: {exc_type}, {exc_obj}, {exc_tb}, {fname}")
            errInfoWinInit = QMessageBox.critical(self, '오류가 발생하였습니다.', '재설정을 하는 중에 오류가 발생했습니다.\n보통 프로그램이 꼬였거나, 저장된 위치에 한글이 들어있으면 안되는 경우가 있습니다.')
            log.critical('failed to intiallized window')

if __name__ == '__main__':
    app = QApplication(sys.argv[0:])
    win = Main()
    win.setupWidget()
    win.show()
    app.exec()
