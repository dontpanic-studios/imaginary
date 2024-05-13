from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QListView, QAbstractItemView, QMenu, QProxyStyle, QStyle
from PyQt6.QtGui import QIcon, QPixmap, QStandardItem, QStandardItemModel
from PyQt6 import QtCore
from PyQt6.QtCore import QEvent, QMimeDatabase
import os, sys, json, subprocess, requests, psutil, traceback, shutil, shutil, platform
from src.gui.createvm import createvm
from datetime import date
from src.gui.label import whynotclick
from src.discord.intergration import Presence
from src.gui.setting import info
from src.gui.editvm import editvm
from src.gui.disktool import disk
from dotenv import load_dotenv
from pathlib import Path
from fontTools.ttLib import TTFont

print('Installing Figtree Font.')
try:
    font = TTFont('src\\font\\figtree.ttf')
except FileNotFoundError:
    print('Font File cannot be found!')
    traceback.format_exception()

githubLink = requests.get('https://api.github.com/repos/dontpanic-studios/imaginary/releases/latest')
print(f'User Platform: {platform.system()}')
usrPlatform = platform.system()

print('Load ENV')
try:
    load_dotenv('./data/setting.env')
    VER = os.environ.get('Ver')
except FileNotFoundError:
    print('Setting ENV File cannot be found!')

class MyProxyStyle(QProxyStyle):
    pass
    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

        if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
            return 60
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)

class Main(QWidget):
    def __init__(self):
        print(f'Imaginary {VER}\nPyQt v{QtCore.qVersion()}')
        print('trying initallizing main frame..')
        try:
            super().__init__()
            self.checkUpdate()

            self.setWindowTitle("Imaginary")
            self.setStyleSheet("background-color: #262626; Color : white;") 
            self.setWindowIcon(QIcon('src/png/icons/128.png'))
            self.setFixedSize(1280, 720)
            self.setAcceptDrops(True)
            self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint)
            self.setupWidget()
        
            print('initallized.')
        except Exception:
            print(f"ERROR Occurred!\nLog: \n{traceback.format_exc()}")
            errInfoWinInit = QMessageBox(self)
            errInfoWinInit.setIcon(QMessageBox.Icon.Critical)
            errInfoWinInit.setWindowTitle('실행 실패')
            errInfoWinInit.setWindowIcon(QIcon('src/png/icons/remove128.png'))
            errInfoWinInit.setText('Imaginary 실행에 실패하였습니다.\n\n실행 실패엔 다양한 오류가 있습니다만, 대중적으로는 권한이 부족하여 실행에 실패할수 있습니다.\n\n더 다양한 정보는 Show Details를 확인해주세요.')
            errInfoWinInit.setDetailedText(f'Imaginary가 실행에 실패하였습니다.\n아래엔 오류 내용입니다.\n{traceback.format_exc()}')
            errInfoWinInit.exec()
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
        self.label_VMInfo = QLabel('No Metadata has been found.', self)

        # image
        self.vm_background.setPixmap(QPixmap('src/png/background/bg1.png'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

        # button
        self.createVM = whynotclick.Label(self)
        self.createVM.setText('Create VM')
        self.imaginarySetting = whynotclick.Label(self)
        self.imaginarySetting.setText('Force Reload VM List')
        self.setting = whynotclick.Label(self)
        self.setting.setText('Info')
        self.runVM = whynotclick.Label(self)
        self.runVM.setText('Start VM')
        self.editVM = whynotclick.Label(self)
        self.editVM.setText('Edit VM')
        self.diskTool = whynotclick.Label(self)
        self.diskTool.setText('Disk Tool')

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
        self.editVM.move(450, 205)
        self.label_Vm_Status.move(350, 175)
        self.setting.move(760, 15)
        self.label_VMInfo.move(350, 255)
        self.diskTool.move(660, 15)

        self.vmListView.resize(290, 645)
        self.vmListView.clicked[QtCore.QModelIndex].connect(self.on_clicked)
        self.vmListView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.imaginarySetting.clicked.connect(self.reloadList)
        self.createVM.clicked.connect(self.showCreateVMWindow)
        self.setting.clicked.connect(self.showSettingWindow)
        self.label_Title.clicked.connect(self.vmListView.clearSelection)
        self.diskTool.clicked.connect(self.showDiskToolWindow)

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

    def on_clicked(self, index): # load data
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
                args = data['addition']['args']
                desc = data['desc']

                if(len(str(args)) >= 15):
                    args = f'{args[0:10]}.. ({len(str(args[10:]))} char left)'
                elif(len(str(args)) <= 0):
                    args = 'No Arguments Found.'

                if(len(str(desc)) >= 15):
                    self.label_Vm_Desc.setText(f'{desc[0:10]}.. ({len(str(desc[10:]))} char left)')
                    self.label_Vm_Desc.setToolTip(data['desc'])
                elif(len(str(args)) <= 0):
                    self.label_Vm_Desc.setText('No Description Found.')   
                self.label_VMInfo.setText(f'Metadata Ver  |  {data['metadata_ver']}\nMax Core  |  {data['max_core']}\nMax Ram  |  {data['max_mem']}\nDisk Size  |  {data['disk']['disk_size']}\nIs Experimental On  |  {data['isaccel']['bool']}\nAccelerator Type  |  {data['isaccel']['acceltype']}\nV-GPU Type  |  {data['vga']['type']}\nAdditional Config  |  {args}')
            except:
                print('Failed to load VM metadata!, is file even?')
                print(traceback.format_exc())
                self.label_VMInfo.setText('No Metadata has been found.')
                self.label_VMInfo.adjustSize()  

            if(data['disk']['disk_size'] != 'No Disk Avaliable'):
                self.runVM.clicked.connect(self.runQemu)
                self.runVM.setStyleSheet("Color : #59d97b; background-color:#2C2C2C;")
            else:
                self.runVM.setToolTip('Cannot run this vm cause no disk has been found.')  
 
            self.editVM.clicked.connect(self.showEditWindow)    
            self.editVM.setStyleSheet("Color : #f5cb58; background-color:#2C2C2C;")

            self.label_Vm_Desc.adjustSize()
            self.label_VMInfo.adjustSize()

            self.label_Vm_Title.setText(item.text())
            self.label_Vm_Title.adjustSize()
            #Presence.update(self, details=f'Looking up {item.text()}', large_image='star') # this mf doesn't work properly
        except (FileNotFoundError, SystemError, json.decoder.JSONDecodeError, PermissionError) as e:
            print('failed to read metadata, is file even?')    
            failReadData = QMessageBox(self)
            failReadData.setWindowTitle('읽기 실패')
            failReadData.setIcon(QMessageBox.Icon.Critical)
            failReadData.setWindowIcon(QIcon('src/png/icons/remove128.png'))
            if e == json.decoder.JSONDecodeError:
                failReadData.setText('가상머신 정보를 읽는데 실패하였습니다.\n\nJSON Decoding Error, 잘못된 Value 값을 가지고 있습니다.')
            elif e == SystemError:
                failReadData.setText('가상머신 정보를 읽는데 실패하였습니다.\n\nSystemError, 시스템 상으로 오류가 발생했습니다.')
            elif e == PermissionError:
                failReadData.setText('가상머신 정보를 읽는데 실패하였습니다.\n\nNo Permission, Imaginary가 데이터를 읽는데에 권한이 부족합니다.')
            else:
                failReadData.setText('가상머신 정보를 읽는데 실패하였습니다.\n\nFile Cannot be found, Imaginary가 파일을 찾을수 없습니다.')
            failReadData.setDetailedText(f'{traceback.format_exc()}')
            failReadData.exec()    
            return

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
        self.editVM.setFont(self.font_button)
        self.editVM.setStyleSheet("Color : #4f4f4f; background-color:#2C2C2C;")
        self.label_Vm_Status.setFont(self.font_bold)
        self.label_Vm_Status.setStyleSheet("Color : white; background-color:#2C2C2C;")
        self.setting.setFont(self.font_button)
        self.setting.setStyleSheet("Color : white; background-color:#262626;")
        self.label_VMInfo.setFont(self.font_button)
        self.label_VMInfo.setStyleSheet("Color : white; background:#2C2C2C;")
        self.diskTool.setFont(self.font_button)
        self.diskTool.setStyleSheet("Color : white; background-color:#262626;")

        self.label_Vm_Title.adjustSize()
        self.label_Vm_Desc.adjustSize()

    def reloadList(self):
        try:
            # this shit is crazy! but why not?
            self.model.clear()
            self.sub_folders = [name for name in os.listdir('src/vm/') if os.path.isdir(os.path.join('src/vm/', name))]
            for i in self.sub_folders:
                if i != 'drivers':
                    f = open('./src/vm/' + i + '/metadata.json', 'r+')
                    data = json.load(f)
                    it = QStandardItem(i)
                    self.model.appendRow(it)
                    it.setData(QIcon(f'src/png/{data['vm_type']}.png'.format(i)), QtCore.Qt.ItemDataRole.DecorationRole)
                    self.vmListView.setModel(self.model)
                    if len(self.sub_folders) > 0:
                        self.label_Vm_Title.setText('Select VM to get Started!')
                        self.label_Vm_Desc.setText('or create another one')
                        self.label_Vm_Title.adjustSize()
                        self.label_Vm_Desc.adjustSize()
                    else:
                        self.label_Vm_Desc.adjustSize()
                        self.label_Vm_Title.adjustSize()
                        print('No VM(s) has been found, ignoring it.')  
                else:
                    print('driver folder found, ignoring.')
        except (FileNotFoundError, SystemError, json.decoder.JSONDecodeError, PermissionError) as e:
            print('failed to read metadata, is file even?')    
            failReadData = QMessageBox(self)
            failReadData.setWindowTitle('읽기 실패')
            failReadData.setIcon(QMessageBox.Icon.Critical)
            failReadData.setWindowIcon(QIcon('src/png/icons/remove128.png'))
            if e == json.decoder.JSONDecodeError:
                failReadData.setText('가상머신 정보를 읽는데 실패하였습니다,\n\n잘못된 Value 값을 가지고 있습니다.')
            elif e == SystemError:
                failReadData.setText('가상머신 정보를 읽는데 실패하였습니다,\n\n시스템 상으로 오류가 발생했습니다.')
            elif e == PermissionError:
                failReadData.setText('가상머신 정보를 읽는데 실패하였습니다,\n\nImaginary가 데이터를 읽는데에 권한이 부족합니다.')
            else:
                failReadData.setText('가상머신 정보를 읽는데 실패하였습니다,\n\nImaginary가 파일을 찾을수 없습니다.')
            failReadData.setDetailedText(f'{traceback.format_exc()}')
            failReadData.exec()         
            return

    def runQemu(self): # qemu run function
        print('Load Model')
        f = open('./src/vm/' + self.label_Vm_Title.text() + '/metadata.json', 'r+')
        data = json.load(f)
        try:
            if(data['isaccel']['bool'] == False):
                if(data['vga']['type'] == 'isa-vga'):
                    qemu = subprocess.Popen(["powershell", f"src/qemu/qemu-system-{data['emulate']} -display gtk,show-menubar=off -drive format={data['disk']['disk_type']},file={data['disk']['disk_loc']} -cdrom {data['iso_loc']} -name '{data['vm_name']}' -smp {data['max_core']} -m {data['max_mem']} -device {data['vga']['type']},vgamem_mb={data['vga']['mem']} {data['addition']['args']}"], stdout=subprocess.PIPE)
                else:
                    qemu = subprocess.Popen(["powershell", f"src/qemu/qemu-system-{data['emulate']} -display gtk,show-menubar=off -drive format={data['disk']['disk_type']},file={data['disk']['disk_loc']} -cdrom {data['iso_loc']} -name '{data['vm_name']}' -smp {data['max_core']} -m {data['max_mem']} -device {data['vga']['type']} {data['addition']['args']}"], stdout=subprocess.PIPE)
            else:
                qemu = subprocess.Popen(["powershell", f"src/qemu/qemu-system-{data['emulate']} -display gtk,show-menubar=off -drive format={data['disk']['disk_type']},file={data['disk']['disk_loc']} -cdrom {data['iso_loc']} -name '{data['vm_name']}' -smp {data['max_core']} -m {data['max_mem']} -device {data['vga']['type']} -accel {data['isaccel']['acceltype']},thread=multi {data['addition']['args']}"], stdout=subprocess.PIPE)
            proc = psutil.Process(qemu.pid)
            try:
                while(proc.status() == psutil.STATUS_RUNNING):
                    self.label_Vm_Status.setText('Status: VM Started')
                    self.label_Vm_Status.setStyleSheet('Color : #42f566; background-color: #2C2C2C;')
                    chkStatus = proc.status()

                    if(chkStatus == psutil.STATUS_DEAD):
                        self.label_Vm_Status.setText('Status: VM Stopped')
                        self.label_Vm_Status.setStyleSheet('Color : white; background-color: #2C2C2C;')
                    elif proc.status() == psutil.STATUS_WAITING:
                        self.label_Vm_Status.setText('Status: Waiting User response..')
                        self.label_Vm_Status.setStyleSheet('Color : #e0b44c; background-color: #2c2c2c;')
                    self.label_Vm_Status.adjustSize() 
            except psutil.NoSuchProcess:
                self.label_Vm_Status.setText('Status: VM Process cannot be found.')
                self.label_Vm_Status.setStyleSheet('Color : red; background-color: #2C2C2C;') 
                self.label_Vm_Status.adjustSize() 
        except:
            print('QEMU Run Failed!')
            trace = traceback.format_exc()
            qemuRunFailed = QMessageBox(self)
            qemuRunFailed.setIcon(QMessageBox.Icon.Critical)
            qemuRunFailed.setWindowIcon(QIcon('src/png/icons/remove128.png'))
            qemuRunFailed.setWindowTitle('QEMU 실행 실패')
            qemuRunFailed.setText(f'QEMU 실행에 실패하였습니다.\nShow Details을 눌러 오류 사항을 확인하세요.')
            qemuRunFailed.setDetailedText(f'Imaginary(이)가 QEMU 실행이 정상적으로 진행이 안되었다고 판단되었습니다,\n{trace}')
            qemuRunFailed.exec()

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

    def eventFilter(self, source, event): # context menu (right click menu)
        if event.type() == QEvent.Type.ContextMenu and source is self.vmListView:
            menu = QMenu()
            delvm = menu.addAction('Delete VM')
            export_vm = menu.addAction('Export VM')

            try:
                index = source.indexAt(event.pos())
                item = self.model.itemFromIndex(index)
                action = menu.exec(event.globalPos())
                print(f'selected item: {item.text()}')
                if action == delvm:
                    self.confirmDeleteVM(index)
                elif action == export_vm:
                    self.exportVM(index)    
            except:
                trace = traceback.format_exc()
                qemuRunFailed = QMessageBox(self)
                qemuRunFailed.setIcon(QMessageBox.Icon.Critical)
                qemuRunFailed.setWindowIcon(QIcon('src/png/icons/remove128.png'))
                qemuRunFailed.setWindowTitle('알수없는 오류 발생')
                qemuRunFailed.setText(f'가상머신을 삭제하는데 실패하였습니다.\nShow Details을 눌러 오류 사항을 확인하세요.')
                qemuRunFailed.setDetailedText(f'Imaginary(이)가 가상머신 삭제(이)가 정상적으로 진행이 안되었다고 판단되었습니다, 다음은 관련된 오류내용입니다.\n{trace}')
                qemuRunFailed.exec()  
            return True
        
        return super().eventFilter(source, event)

    def confirmDeleteVM(self, index):
        item = self.model.itemFromIndex(index)
        isTrue = QMessageBox.warning(self, '정말로 지울까요?', f'가상머신 {item.text()} (을)를 지울까요?\n다시는 취소할수 없어요!', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if(isTrue == QMessageBox.StandardButton.Yes):
            try:
                shutil.rmtree(f'src\\vm\\{item.text()}')
                success = QMessageBox.information(self, '삭제됨', f'{item.text()} (이)가 성공적으로 지워졌습니다.')
                self.reloadList()
            except:
                failed = QMessageBox(self, '삭제 이벤트 취소됨', f'가상머신 {item.text()}를 지우다가 알수없는 오류가 발생했습니다.\n자세한 내용은 Show Details.. 를 눌러 확인하세요.')
                failed.setDetailedText(f'미안해요!\nImaginary(이)가 폴더 "{item.text()}" 를 지우다가 알수없는 오류를 마주했습니다.\n\n폴더가 존재하지 않거나, 아니면 권한이 부족할수도 있습니다.')
                failed.setIcon(QMessageBox.Icon.Critical)
        else:
            print('ignoring.')

    def exportVM(self, index):
        item = self.model.itemFromIndex(index)
        vmloc = f'src/vm/{item.text()}'

        try:
            shutil.make_archive(f'{item.text()}-exported-{date.today()}', 'zip', vmloc)
            succ = QMessageBox.information(self, '가상머신 내보내짐', f'{item.text()} (이)가 {os.getcwd()} (으)로 내보내졌습니다.')
        except:
            failed = QMessageBox(self)
            failed.setWindowTitle('가상머신 내보내기 이벤트 취소됨')
            failed.setWindowIcon(QIcon('src/png/icons/remove128.png'))
            failed.setText(f'가상머신 {item.text()}를 내보내다가 알수없는 오류가 발생했습니다.\n자세한 내용은 Show Details.. 를 눌러 확인하세요.')
            failed.setDetailedText(f'미안해요!\nImaginary(이)가 "{item.text()}" 를 zip 확장자로 내보내다가 알수없는 오류를 마주했습니다.\n\n폴더가 존재하지 않거나, 아니면 권한이 부족할수도 있습니다.\n\n{traceback.format_exc()}')
            failed.setIcon(QMessageBox.Icon.Critical)
            failed.exec()

    def loadExportedVM(self, url):
        print(f'trying to unpack vm: {url}')
        try:
            filename = Path(url).stem
            shutil.unpack_archive(url, f'src/vm/{filename}', 'zip')
            self.reloadList()
            print('successfully loaded vm.')
            succ = QMessageBox.information(self, '가상머신 불러와짐', f'{filename}을 성공적으로 불러왔습니다.')
        except FileExistsError:
            failed = QMessageBox(self, '가상머신 불러오기 이벤트 취소됨', f'{filename}(이)가 이미 존재하여 취소하였습니다.')  

    def dragEnterEvent(self, event):
        if self.findExportedZip(event.mimeData()):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if self.findExportedZip(event.mimeData()):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = self.findExportedZip(event.mimeData())
        if urls:
            for url in urls:
                self.loadExportedVM(url.toLocalFile())
            event.accept()
        else:
            event.ignore()

    def findExportedZip(self, mimedata):
        urls = list()
        db = QMimeDatabase()
        for url in mimedata.urls():
            mimetype = db.mimeTypeForUrl(url)
            if mimetype.name() == "application/zip":
                urls.append(url)
        return urls  

    def showDiskToolWindow(self):
        print("Opening DisktoolWin...")
        self.w = disk.DiskTool()
        self.w.show()      

if __name__ == '__main__':
    Presence.connect()
