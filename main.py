from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QListView, QAbstractItemView, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QStandardItem, QStandardItemModel
from PyQt6 import QtCore
from PyQt6.QtCore import QEvent
import os, sys, json, subprocess, requests, psutil, traceback
from src.gui.createvm import createvm
from src.gui.label import whynotclick
from src.discord.intergration import Presence
from src.gui.setting import info
from src.gui.editvm import editvm
from src.exception.QemuRunFail import *
from dotenv import load_dotenv

githubLink = requests.get('https://api.github.com/repos/dontpanic-studios/imaginary/releases/latest')
print('Load ENV')
try:
    load_dotenv('./data/setting.env')
    VER = os.environ.get('Ver')
except FileNotFoundError:
    print('Setting ENV File cannot be found!')

class Main(QWidget):
    def __init__(self):
        print(f'Imaginary {os.environ.get('Ver')}\nPyQt v{QtCore.qVersion()}')
        print('trying initallizing main frame..')
        try:
            super().__init__()
            self.checkUpdate()

            self.setWindowTitle("Imaginary")
            self.setStyleSheet("background-color: #262626; Color : white;") 
            self.setWindowIcon(QIcon('src/png/icons/128.png'))
            self.setFixedSize(1280, 720)
            self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint)
            self.setupWidget()
        
            print('initallized.')
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"ERROR Occurred!\nLog: {exc_type}, {exc_obj}, {exc_tb}, {fname}")
            errInfoWinInit = QMessageBox.critical(self, '오류가 발생하였습니다.', '재설정을 하는 중에 오류가 발생했습니다.\n보통 프로그램이 꼬였거나, 저장된 위치에 한글이 들어있으면 안되는 경우가 있습니다.')
            print('failed to intiallized window')
            return

    def setupWidget(self):
        # label
        print('Load Widgets')
        self.vm_background = QLabel(self)
        self.label_Title = whynotclick.Label(self)
        self.label_Title.setText("🌠 Imaginary")
        self.label_Vm_Title = QLabel("No VM has been found!", self)
        self.label_Vm_Desc = QLabel("Why don't you make one?", self)
        self.label_Vm_Status = QLabel("Status: No VM status available.", self)
        self.vm_Snapshot = QLabel(self)
        self.label_Snapshot = QLabel("Last Snapshot", self)
        self.label_VMInfo = QLabel('No Metadata has been found.', self)

        # image
        self.vm_background.setPixmap(QPixmap('src/png/background/bg1.png'))        
        self.vm_Snapshot.setPixmap(QPixmap('src/png/snapshot.png'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

        # button
        self.createVM = whynotclick.Label(self)
        self.createVM.setText('Create VM')
        self.imaginarySetting = whynotclick.Label(self)
        self.imaginarySetting.setText('Force Reload VM List')
        self.setting = whynotclick.Label(self)
        self.setting.setText('Info')
        self.runVM = whynotclick.Label(self)
        self.runVM.setText('Start VM')
        self.stopVM = whynotclick.Label(self)
        self.stopVM.setText('Stop VM')
        self.editVM = whynotclick.Label(self)
        self.editVM.setText('Edit VM')

        # vm list
        self.vmListView = QListView(self)
        self.model = QStandardItemModel()
        self.sub_folders = [name for name in os.listdir('src/vm/') if os.path.isdir(os.path.join('src/vm/', name))]
        self.reloadList()
        self.vmListView.setStyleSheet("border : 2px solid black;")

        # font
        self.font_bold = self.label_Title.font()
        self.font_bold.setBold(True)
        self.font_bold.setPointSize(20)
        self.font_bold.setFamily(os.environ.get('Font'))

        self.font_bold_title = self.label_Title.font()
        self.font_bold_title.setBold(True)
        self.font_bold_title.setPointSize(30)
        self.font_bold_title.setFamily(os.environ.get('Font'))

        self.font_button = self.label_Title.font()
        self.font_button.setBold(True)
        self.font_button.setPointSize(15)
        self.font_button.setFamily(os.environ.get('Font'))

        # widget move
        self.label_Title.move(15, 13)
        self.label_Vm_Title.move(350, 75)
        self.vm_background.move(320, 50)
        self.label_Vm_Desc.move(352, 120)
        self.createVM.move(330, 15)
        self.imaginarySetting.move(450, 15)
        self.vmListView.move(15, 60)
        self.runVM.move(350, 205)
        self.stopVM.move(450, 205)
        self.editVM.move(550, 205)
        self.label_Vm_Status.move(350, 175)
        self.setting.move(660, 15)
        self.vm_Snapshot.move(835, 80)
        self.label_Snapshot.move(835, 480)
        self.label_VMInfo.move(350, 255)

        self.vmListView.resize(290, 645)
        self.vmListView.clicked[QtCore.QModelIndex].connect(self.on_clicked)
        self.vmListView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.vm_Snapshot.resize(400, 400)
        
        self.imaginarySetting.clicked.connect(self.reloadList)
        self.createVM.clicked.connect(self.showCreateVMWindow)
        self.setting.clicked.connect(self.showSettingWindow)
        self.label_Title.clicked.connect(self.vmListView.clearSelection)

        self.vmListView.installEventFilter(self)
        self.setLabelFont()

    def showCreateVMWindow(self):
        print("Opening CreateVM...")
        self.w = createvm.CreateVM()
        self.w.show()

    def showSettingWindow(self):
        print("Opening SettingWin...")
        self.w = info.CreateVM()
        self.w.show()    

    def showEditWindow(self):
        print("Opening EditWin...")
        self.w = editvm.EditVM(self.label_Vm_Title.text())
        self.w.show()        

    def on_clicked(self, index):
        print('Retriving Info from metadata.json')
        try:
            item = self.model.itemFromIndex(index)
            print('Tries to load metadata')
            try:
                f = open('./src/vm/' + item.text() + '/metadata.json', 'r+')
                data = json.load(f)
                print(f'Got package, header: \n{data}')
                for i in data['desc']:
                    self.label_Vm_Desc.setText(data['desc'])
                f.close()
                self.label_VMInfo.setText(f'Metadata Ver  |  {data['metadata_ver']}\nMax Core  |  {data['max_core']}\nMax Ram  |  {data['max_mem']}\nDisk Size  |  {data['disk_size']}\nIs Experimental On  |  {data['isaccel']['bool']}\nAccelerator Type  |  {data['isaccel']['acceltype']}\nV-GPU Type  |  {data['vga']['type']}')
            except:
                print('Failed to load VM metadata!, is file even?')
                print(traceback.print_exc())
                self.label_VMInfo.setText('No Metadata has been found.')
                self.label_VMInfo.adjustSize()    

            try:
                print('Load snapshot')
                self.label_Snapshot.setPixmap(QPixmap(data['snapshot']))
            except:
                print('File not found, returing default state.')
                self.label_Snapshot.setPixmap(QPixmap('src/png/snapshot.png'))    
            self.runVM.clicked.connect(self.runQemu)
            self.editVM.clicked.connect(self.showEditWindow)
            self.runVM.setStyleSheet("Color : #59d97b; background-color:#2C2C2C;")
            self.editVM.setStyleSheet("Color : #f5cb58; background-color:#2C2C2C;")

            self.label_Vm_Desc.adjustSize()
            self.label_VMInfo.adjustSize()

            self.label_Vm_Title.setText(item.text())
            self.label_Vm_Title.adjustSize()
            #Presence.update(self, details=f'Looking up {item.text()}', large_image='star') # this mf doesn't work properly
        except FileNotFoundError:
            print('failed to read metadata, is file even?')    

    def closeEvent(self, event):
        sys.exit(0)

    def setLabelFont(self):
        self.label_Title.setFont(self.font_bold)
        self.label_Title.setStyleSheet("Color : white; background-color:#262626;")
        self.label_Vm_Title.setFont(self.font_bold_title)
        self.label_Vm_Title.setStyleSheet("Color : white; background-color:#2C2C2C;")
        self.label_Vm_Desc.setFont(self.font_bold)
        self.label_Vm_Desc.setStyleSheet("Color : white; background-color:#2C2C2C;")
        self.createVM.setFont(self.font_button)
        self.createVM.setStyleSheet("Color : white; background-color:#262626;")
        self.imaginarySetting.setFont(self.font_button)
        self.imaginarySetting.setStyleSheet("Color : white; background-color:#262626;")
        self.vmListView.setStyleSheet("Color : white;")
        self.vmListView.setFont(self.font_button)
        self.runVM.setFont(self.font_button)
        self.runVM.setStyleSheet("Color : #4f4f4f; background-color:#2C2C2C;")
        self.stopVM.setFont(self.font_button)
        self.stopVM.setStyleSheet("Color : #4f4f4f; background-color:#2C2C2C;")
        self.editVM.setFont(self.font_button)
        self.editVM.setStyleSheet("Color : #4f4f4f; background-color:#2C2C2C;")
        self.label_Vm_Status.setFont(self.font_bold)
        self.label_Vm_Status.setStyleSheet("Color : white; background-color:#2C2C2C;")
        self.setting.setFont(self.font_button)
        self.setting.setStyleSheet("Color : white; background-color:#262626;")
        self.label_Snapshot.setFont(self.font_button)
        self.label_Snapshot.setStyleSheet("Color : white; background:#2C2C2C;")
        self.label_VMInfo.setFont(self.font_button)
        self.label_VMInfo.setStyleSheet("Color : white; background:#2C2C2C;")

    def reloadList(self):
        # this shit is crazy! but why not?
        self.model.clear()
        self.sub_folders = [name for name in os.listdir('src/vm/') if os.path.isdir(os.path.join('src/vm/', name))]
        for i in self.sub_folders:
            f = open('./src/vm/' + i + '/metadata.json', 'r+')
            data = json.load(f)
            print('Done')
            it = QStandardItem(i)
            self.model.appendRow(it)
            it.setData(QIcon(f'src/png/{data['vm_type']}.png'.format(i)), QtCore.Qt.ItemDataRole.DecorationRole)
            self.vmListView.setModel(self.model)
            print('Model setup done.')
            if len(self.sub_folders) > 0:
                self.label_Vm_Title.setText('Select VM to get Started!')
                self.label_Vm_Desc.setText('or create another one')
                self.label_Vm_Title.adjustSize()
                self.label_Vm_Desc.adjustSize()
            else:
                self.label_Snapshot.setHidden(True)
                self.vm_Snapshot.setHidden(True)
                print('No VM(s) has been found, ignoring it.')  

# idk why this thing wont work properly
    def runQemu(self):
        print('Load Model')
        f = open('./src/vm/' + self.label_Vm_Title.text() + '/metadata.json', 'r+')
        data = json.load(f)
        try:
            if(data['isaccel']['bool'] == False):
                if(data['vga']['type'] == 'isa-vga'):
                    qemu = subprocess.Popen(["powershell", f"src/qemu/qemu-system-x86_64 -display gtk,show-menubar=off -drive format=raw,file={data['disk_loc']} -cdrom {data['iso_loc']} -name '{data['vm_name']}' -smp {data['max_core']} -m {data['max_mem']} -device {data['vga']['type']},vgamem_mb={data['vga']['mem']} {data['addition']['args']}"], stdout=subprocess.PIPE)
                else:
                    qemu = subprocess.Popen(["powershell", f"src/qemu/qemu-system-x86_64 -display gtk,show-menubar=off -drive format=raw,file={data['disk_loc']} -cdrom {data['iso_loc']} -name '{data['vm_name']}' -smp {data['max_core']} -m {data['max_mem']} -device {data['vga']['type']} {data['addition']['args']}"], stdout=subprocess.PIPE)
            else:
                qemu = subprocess.Popen(["powershell", f"src/qemu/qemu-system-x86_64 -display gtk,show-menubar=off -drive format=raw,file={data['disk_loc']} -cdrom {data['iso_loc']} -name '{data['vm_name']}' -smp {data['max_core']} -m {data['max_mem']} -device {data['vga']['type']} -accel {data['isaccel']['acceltype']} {data['addition']['args']}"], stdout=subprocess.PIPE)
            self.stopVM.clicked.connect(qemu.terminate)
            proc = psutil.Process(qemu.pid)
            if(proc.status == psutil.STATUS_RUNNING):
                self.label_Vm_Status.setText('Status: Running through some kind of resistance.')
                self.label_Vm_Status.setStyleSheet('Color : #42f566; background-color: #2C2C2C;')
            self.label_Vm_Status.adjustSize() 
        except:
            print('QEMU Run Failed!')
            trace = traceback.print_exc()
            qemuRunFailed = QMessageBox(self)
            qemuRunFailed.setIcon(QMessageBox.Icon.Critical)
            qemuRunFailed.setWindowIcon(QIcon('src/png/icons/128.png'))
            qemuRunFailed.setWindowTitle('QEMU 실행 실패')
            qemuRunFailed.setText(f'QEMU 실행에 실패하였습니다.\nShow Details을 눌러 오류 사항을 확인하세요.')
            qemuRunFailed.setDetailedText(f'Imaginary(이)가 QEMU 실행이 정상적으로 진행이 안되었다고 판단되었습니다,\n{str(trace)}')
            qemuRunFailed.exec()
            raise QemuRunVaildationFail("testing")

    def checkUpdate(self):
            print('Checking update')
            githubLatestVer = githubLink.json()["name"]
            githubLastestDownload = githubLink.json()['assets']
            print(githubLastestDownload)
            print("Current path: " + os.getcwd())
            print("Current latest version: " + githubLatestVer)
            print("Current version: " + os.environ.get('Ver'))
            if(githubLatestVer > VER):
                print('Using old version!')
                print("You're currerntly using older version of Imaginary.")
                findUpdateMsg = QMessageBox(self)
                findUpdateMsg.setIcon(QMessageBox.Icon.Question)
                findUpdateMsg.setWindowIcon(QIcon('src/png/icons/128.png'))
                findUpdateMsg.setWindowTitle('업데이트 발견')
                findUpdateMsg.setText(f'새로운 버전 {githubLatestVer} 이(가) 발견되었습니다,\nShow Details... 를 눌러 자세한 업데이트 내용을 확인할수 있습니다..')
                findUpdateMsg.setDetailedText(githubLink.json()['body'])
                findUpdateMsg.exec()
            elif(githubLatestVer < VER):
                print(f"현재 개발자 버전을 사용하고 있습니다, 이 버전은 매우 불안정하며, 버그가 자주 발생합니다.")
                usingDebugVer = QMessageBox(self)
                usingDebugVer.setIcon(QMessageBox.Icon.Warning)
                usingDebugVer.setWindowIcon(QIcon('src/png/icons/128.png'))
                usingDebugVer.setWindowTitle('개발 버전 사용중')
                usingDebugVer.setText(f'현재 {githubLatestVer} 버전보다 더 높은 버전 {VER} 을 사용하고 있습니다.\n이 버전은 매우 불안정하며, 버그가 자주 발생합니다.')
                usingDebugVer.exec()
            elif(githubLatestVer == VER):
                print(f"최신버전을 사용하고 있습니다!")

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.ContextMenu and source is self.vmListView:
            menu = QMenu()
            menu.addAction('Run VM')
            menu.addAction('Edit VM')
            menu.addAction('Delete VM')
            menu.addAction('Debug')

            if menu.exec(event.globalPos()):
                item = source.itemAt(event.pos())
                print(item.text())
            return True
        
        return super().eventFilter(source, event)

    def confirmDeleteVM(self, index):
        item = self.model.itemFromIndex(index)
        isTrue = QMessageBox.warning(self, '정말로 지울까요?', f'가상머신 {item.text()} (을)를 지울까요?\n다시는 변경하지 않아요!', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        response = isTrue.exec()

        if(response == QMessageBox.Yes):
            print('watt')
        else:
            print('ignoring.')

if __name__ == '__main__':
    Presence.connect()