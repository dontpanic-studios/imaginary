from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QListView, QAbstractItemView, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QStandardItem, QStandardItemModel
from PyQt6 import QtCore
from PyQt6.QtCore import QEvent, QMimeDatabase
import os, sys, json, subprocess, requests, psutil, traceback, shutil, shutil, platform
from src.gui.createvm import createvm
from datetime import date
from src.language.lang import Language, LanguageList
from src.gui.label import whynotclick
from src.discord.intergration import Presence
from src.gui.setting import info
from src.support.iupl import loadPlugin, loadedPlugins
from src.support.library.ipl_exception import Exceptions
from src.gui.editvm import editvm
from src.gui.disktool import disk
from dotenv import load_dotenv
from pathlib import Path
from fontTools.ttLib import TTFont
from src.notification.wrapper import Notifiaction
from pyqttoast import Toast, ToastPreset


print('Installing Figtree Font.')
try:
    font = TTFont('src\\font\\wanted.ttf')
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
    LANG = os.environ.get('Language')
    print('Current Language: ' + LANG)
except FileNotFoundError:
    print('Setting ENV File cannot be found!')

class Main(QWidget):
    def __init__(self):
        print(f'Imaginary {VER}\nPyQt v{QtCore.qVersion()}')
        print('trying initallizing main frame..')
        try:
            super().__init__()

            self.setWindowTitle("Imaginary")
            self.setStyleSheet("background-color: #262626; Color : white;") 
            self.setWindowIcon(QIcon('src/png/icons/128.png'))
            self.setFixedSize(1280, 720)
            self.setAcceptDrops(True)
            self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint)
            self.setupWidget()
            self.loadPlugins()
            self.checkUpdate()
        
            print('initallized.')
        except (Exception, TypeError, PermissionError) as e:
            print(f"ERROR Occurred!\nLog: \n{traceback.format_exc()}")
            errInfoWinInit = QMessageBox(self)
            errInfoWinInit.setWindowTitle(Language.getLanguageByEnum(LanguageList.MSG_VAR_TITLE))
            if(e == PermissionError):
                errInfoWinInit.setText(Language.getLanguageByEnum(LanguageList.MSG_VAR_PERMISSION))
            else:
                errInfoWinInit.setText(Language.getLanguageByEnum(LanguageList.MSG_VAR_DESC))
            errInfoWinInit.setDetailedText(traceback.format_exc())
            errInfoWinInit.setIcon(QMessageBox.Icon.Critical)
            errInfoWinInit.exec()
            print('failed to intiallized window')
            exit("Program Exited cause unknown problem has been appeared.")

    def setupWidget(self):
        # label
        print('Load Widgets')
        self.vm_background = QLabel(self)
        self.label_Title = whynotclick.Label(self)
        self.label_Title.setText("🌠 Imaginary")
        self.label_Vm_Title = QLabel(Language.getLanguageByEnum(LanguageList.NO_VM_AVALIABLE), self)
        self.label_Vm_Desc = QLabel(Language.getLanguageByEnum(LanguageList.NO_VM_AVALIABLE_DESC), self)
        self.label_Vm_Status = QLabel(Language.getLanguageByEnum(LanguageList.MAIN_STATUS_NULL), self) #DEBUG
        self.label_VMInfo = QLabel(Language.getLanguageByEnum(LanguageList.NO_METADATA_FOUND), self)
        self.label_LoadedPlugins = QLabel(text=Language.getLanguageByEnum(LanguageList.MAIN_LOADEDPLUGINS) + str(loadedPlugins.copy()), parent=self)

        # image
        self.vm_background.setPixmap(QPixmap('src/png/background/bg1.png'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

        # button
        self.createVM = whynotclick.Label(self)
        self.createVM.setText(Language.getLanguageByEnum(LanguageList.CREATE_VM))
        self.imaginarySetting = whynotclick.Label(self)
        self.imaginarySetting.setText(Language.getLanguageByEnum(LanguageList.FORCE_RELOAD_LIST))
        self.setting = whynotclick.Label(self)
        self.setting.setText(Language.getLanguageByEnum(LanguageList.IMAGINARY_INFO))
        self.runVM = whynotclick.Label(self)
        self.runVM.setText(Language.getLanguageByEnum(LanguageList.MAIN_VMSTART))
        self.editVM = whynotclick.Label(self)
        self.editVM.setText(Language.getLanguageByEnum(LanguageList.MAIN_VMEDIT))
        self.diskTool = whynotclick.Label(self)
        self.diskTool.setText(Language.getLanguageByEnum(LanguageList.DISK_TOOL))

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
        self.label_LoadedPlugins.move(350, 640)

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
        self.setKRLocation()

        if(self.checkIfClientModded() == True):
            print("Modded Client Found!")
            self.label_LoadedPlugins.show()
        else:
            self.label_LoadedPlugins.hide()

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
        self.w = editvm.EditVM(vmname=self.label_Vm_Title.text())
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
                if data['desc'] != '':
                    for i in data['desc']:
                        self.label_Vm_Desc.setText(data['desc'])
                    f.close()
                    desc = data['desc']
                else:
                    desc = Language.getLanguageByEnum(LanguageList.NO_DESCRIPTION_FOUND) 
                args = data['addition']['args']

                if(len(str(args)) >= 15):
                    args = f'{args[0:10]}.. ({len(str(args[10:]))} char left)'
                elif(len(str(args)) <= 0):
                    args = Language.getLanguageByEnum(LanguageList.NO_ARGUMENTS_FOUND)

                if(len(str(desc)) >= 25):
                    self.label_Vm_Desc.setText(f'{desc[0:20]}.. ({len(str(desc[20:]))} char left)')
                    self.label_Vm_Desc.setToolTip(data['desc'])
                elif(len(str(args)) <= 0):
                    self.label_Vm_Desc.setText(Language.getLanguageByEnum(LanguageList.NO_DESCRIPTION_FOUND))   
                self.label_VMInfo.setText(f'Metadata Ver  |  {data['metadata_ver']}\nMax Core  |  {data['max_core']}\nMax Ram  |  {data['max_mem']}\nDisk Size  |  {data['disk']['disk_size']}\nIs Experimental On  |  {data['isaccel']['bool']}\nAccelerator Type  |  {data['isaccel']['acceltype']}\nV-GPU Type  |  {data['vga']['type']}\nAdditional Config  |  {args}')
            except (FileNotFoundError, SystemError, json.decoder.JSONDecodeError, PermissionError) as e:
                print('Failed to load VM metadata!, is file even?')
                print(traceback.format_exc())
                self.label_VMInfo.setText(Language.getLanguageByEnum(LanguageList.NO_METADATA_FOUND))
                self.label_VMInfo.adjustSize()
                Notifiaction.showErrorStr(LanguageList.NO_METADATA_FOUND, 'the fuck is wrong w u', 2500, True, self)
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
            metadataInvaild = Toast(self)
            metadataInvaild.setTitle(Language.getLanguageByEnum(LanguageList.MSG_MAIN_METADATA_FAILED_TITLE))
            if e == json.decoder.JSONDecodeError:
                metadataInvaild.setText(Language.getLanguageByEnum(LanguageList.MSG_MAIN_METADATA_FAILED_JSON) + '\n' + traceback.format_exc)
            elif e == SystemError:
                metadataInvaild.setText(Language.getLanguageByEnum(LanguageList.MSG_MAIN_METADATA_FAILED_SYSTEM) + '\n' + traceback.format_exc())
            elif e == PermissionError:
                metadataInvaild.setText(Language.getLanguageByEnum(LanguageList.MSG_MAIN_METADATA_FAILED_PERMISSION) + '\n' + traceback.format_exc)
            else:
                metadataInvaild.setText(Language.getLanguageByEnum(LanguageList.MSG_MAIN_METADATA_FAILED_NOFILEFOUND) + '\n' + traceback.format_exc)
            metadataInvaild.applyPreset(ToastPreset.ERROR_DARK)
            metadataInvaild.show()
            return

    def checkIfClientModded(self):
        sub_folders = [name for name in os.listdir('src/plugins/') if os.path.isdir(os.path.join('src/plugins/', name))]
        if(len(sub_folders) > 0):
            return True
        else:
            return False

    def loadPlugins(self):
        try:
            loadPlugin()
        except (Exceptions.InvaildCodeInjection, Exceptions.InvaildData, Exceptions.InvaildModule, TypeError):
            print("Code Injection Failed!")
            print(f"Raise Exceptions\n{traceback.format_exc()}")
            Notifiaction.showError(LanguageList.MSG_IUPL_INITALLIZE_FAIL_TITLE, LanguageList.MSG_IUPL_INITALLIZE_FAIL_DESC, 2500, True, self)

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
        self.label_LoadedPlugins.setFont(self.font_button)
        self.label_LoadedPlugins.setStyleSheet("Color : white; background-color:#2c2c2c;")

        self.label_Vm_Title.adjustSize()
        self.label_LoadedPlugins.adjustSize()
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
                        self.label_Vm_Title.setText(Language.getLanguageByEnum(LanguageList.SELECT_VM))
                        self.label_Vm_Desc.setText(Language.getLanguageByEnum(LanguageList.SELECT_VM))
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
            failReadData.setWindowTitle(Language.getLanguageByEnum(LanguageList.MSG_MAIN_METADATA_FAILED_TITLE))
            failReadData.setIcon(QMessageBox.Icon.Critical)
            failReadData.setWindowIcon(QIcon('src/png/icons/remove128.png'))
            if e == json.decoder.JSONDecodeError:
                failReadData.setText(Language.getLanguageByEnum(LanguageList.MSG_MAIN_METADATA_FAILED_JSON))
            elif e == SystemError:
                failReadData.setText(Language.getLanguageByEnum(LanguageList.MSG_MAIN_METADATA_FAILED_SYSTEM))
            elif e == PermissionError:
                failReadData.setText(Language.getLanguageByEnum(LanguageList.MSG_MAIN_METADATA_FAILED_PERMISSION))
            else:
                failReadData.setText(Language.getLanguageByEnum(LanguageList.MSG_MAIN_METADATA_FAILED_NOFILEFOUND))
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
                    qemu = subprocess.Popen(["powershell", f"src/qemu/qemu-system-{data['emulate']} -display gtk,show-menubar=off -drive format={data['disk']['disk_type']},file={data['disk']['disk_loc']} -cdrom {data['iso_loc']} -name '{data['vm_name']}' -smp {data['max_core']} -m {data['max_mem']} -device {data['vga']['type']},vgamem_mb={data['vga']['mem']} {data['addition']['args']}"], stdout=subprocess.PIPE) #DEBUG
                else:
                    qemu = subprocess.Popen(["powershell", f"src/qemu/qemu-system-{data['emulate']} -display gtk,show-menubar=off -drive format={data['disk']['disk_type']},file={data['disk']['disk_loc']} -cdrom {data['iso_loc']} -name '{data['vm_name']}' -smp {data['max_core']} -m {data['max_mem']} -device {data['vga']['type']} {data['addition']['args']}"], stdout=subprocess.PIPE) #DEBUG
            else:
                qemu = subprocess.Popen(["powershell", f"src/qemu/qemu-system-{data['emulate']} -display gtk,show-menubar=off -drive format={data['disk']['disk_type']},file={data['disk']['disk_loc']} -cdrom {data['iso_loc']} -name '{data['vm_name']}' -smp {data['max_core']} -m {data['max_mem']} -device {data['vga']['type']} -accel {data['isaccel']['acceltype']},thread=multi {data['addition']['args']}"], stdout=subprocess.PIPE) #DEBUG
            proc = psutil.Process(qemu.pid) #DEBUG
            try:
                while(proc.status() == psutil.STATUS_RUNNING):
                    self.label_Vm_Status.setText(Language.getLanguageByEnum(LanguageList.MAIN_STATUS_RUNNING))
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
                Notifiaction.showErrorStr(LanguageList.MSG_QEMU_FAILED_TITLE, f'{Language.getLanguageByEnum(LanguageList.MSG_QEMU_FAILED_DESC_NOPROCESS)}\n{traceback.__name__}', 2500, True, self)
        except:
            print('QEMU Run Failed!')
            Notifiaction.showErrorStr(LanguageList.MSG_QEMU_FAILED_TITLE, f'{Language.getLanguageByEnum(LanguageList.MSG_QEMU_FAILED_DESC)}\n{traceback.__name__}', 2500, True, self)

    def checkUpdate(self):
            print('Checking update')
            response = requests.get("https://github.com/dontpanic-studios/imaginary/releases/latest")
            version = response.url.split("/").pop()
            print('Current Version: '+ VER + '\nGithub Lastest: '+ version)
            if(version > VER):
                print('Newer version installed, bug may appear during run status.')
                Notifiaction.showWarnStr(LanguageList.MSG_UPDATE_DEV_VERSION_TITLE, f'{Language.getLanguageByEnum(LanguageList.MSG_UPDATE_DEV_VERSION_DESC)} {VER} {Language.getLanguageByEnum(LanguageList.MSG_UPDATE_DEV_VERSION_DESC2)}', 2500, True, self)
            elif (version < VER):
                print('Older version installed, please update imaginary for new feature and bug fixes.')
                Notifiaction.showInfoStr(LanguageList.MSG_UPDATE_FOUND_TITLE, f'{Language.getLanguageByEnum(LanguageList.MSG_UPDATE_FOUND_DESC)} {version} {Language.getLanguageByEnum(LanguageList.MSG_UPDATE_FOUND_DESC_2)}', 2500, True, self)
            else:
                print('Unknown Version found.')
                Notifiaction.showErrorStr(LanguageList.MSG_UPDATE_UNKNOWN_TITLE, f'the fuck version u using rn', 2500, True, self)

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
        isTrue = QMessageBox.warning(self, Language.getLanguageByEnum(LanguageList.MSG_CONTEXT_DELETEVM_CONFIRM_TITLE), Language.getLanguageByEnum(LanguageList.MSG_CONTEXT_DELETEVM_CONFIRM_DESC) + item.text() + Language.getLanguageByEnum(LanguageList.MSG_CONTEXT_DELETEVM_CONFIRM_DESC_2), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if(isTrue == QMessageBox.StandardButton.Yes):
            try:
                shutil.rmtree(f'src\\vm\\{item.text()}')
                Notifiaction.showSuccessStr(LanguageList.MSG_CONTEXT_DELETEVM_SUCCESS_TITLE, f'{Language.getLanguageByEnum(LanguageList.MSG_CONTEXT_DELETEVM_SUCCESS_DESC)} {item.text()} {Language.getLanguageByEnum(LanguageList.MSG_CONTEXT_DELETEVM_SUCCESS_DESC_2)}', 2500, True, self)
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
            Notifiaction.showSuccessStr(LanguageList.MSG_EXPORTVM_SUCCESS_TITLE, f'{Language.getLanguageByEnum(LanguageList.MSG_EXPORTVM_SUCCESS_DESC)} {vmloc} {Language.getLanguageByEnum(LanguageList.MSG_EXPORTVM_SUCCESS_DESC2)}', 2500, True, self)
        except:
            Notifiaction.showErrorStr(LanguageList.MSG_EXPORTVM_FAILED_TITLE, f'{Language.getLanguageByEnum(LanguageList.MSG_EXPORTVM_FAILED_DESC)} {traceback.__name__}', 2500, True, self)

    def loadExportedVM(self, url):
        print(f'trying to unpack vm: {url}')
        try:
            filename = Path(url).stem
            shutil.unpack_archive(url, f'src/vm/{filename}', 'zip')
            self.reloadList()
            print('successfully loaded vm.')
            Notifiaction.showSuccess(LanguageList.MSG_LOADVM_SUCCESS_TITLE, LanguageList.MSG_LOADVM_SUCCESS_DESC, 2500, True, self)
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
            else:
                fileNotCompatible = QMessageBox.warning(self, Language.getLanguageByEnum(LanguageList.MSG_MAIN_METADATA_FAILED_TITLE), Language.getLanguageByEnum(LanguageList.MSG_MAIN_METADATA_FAILED_INCOMPATIBLE))
        return urls  

    def showDiskToolWindow(self):
        print("Opening DisktoolWin...")
        self.w = disk.DiskTool()
        self.w.show()      

    def setKRLocation(self):
        if LANG == 'ko_KR':
            print('KR Lang Detected, ')
            self.editVM.move(465, 205)
            self.imaginarySetting.move(480, 15)
        else:
            print('Dont Change Location, ENUS Detected.')    

if __name__ == '__main__':
    Presence.connect()
