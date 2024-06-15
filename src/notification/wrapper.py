from pyqttoast import Toast, ToastPreset
from src.language.lang import Language, LanguageList
from PyQt6.QtGui import QFont

class Notifiaction():

    def showError(title: LanguageList, desc: LanguageList, duration: int,  isDark: bool, self):
        font = QFont()
        font.setFamily('Wanted Sans Variable')
        font.setPointSize(10)
        font.setBold(False)
        if(duration == None):
            duration = 21000
        
        errorNoti = Toast(self)
        errorNoti.setTitle(Language.getLanguageByEnum(title))
        errorNoti.setText(Language.getLanguageByEnum(desc))
        if(isDark == True):
            errorNoti.applyPreset(ToastPreset.ERROR_DARK)
        else:
            errorNoti.applyPreset(ToastPreset.ERROR)
        errorNoti.setDuration(duration)
        errorNoti.setTitleFont(font)
        errorNoti.setTextFont(font)
        errorNoti.show()
    
    def showInfo(title: LanguageList, desc: LanguageList, duration: int, isDark: bool, self):
        font = QFont()
        font.setFamily('Wanted Sans Variable')
        font.setPointSize(10)
        font.setBold(False)
        if(duration == None):
            duration = 21000

        errorNoti = Toast(self)
        errorNoti.setTitle(Language.getLanguageByEnum(title))
        errorNoti.setText(Language.getLanguageByEnum(desc))
        if(isDark == True):
            errorNoti.applyPreset(ToastPreset.INFORMATION_DARK)
        else:
            errorNoti.applyPreset(ToastPreset.INFORMATION)
        errorNoti.setDuration(duration)
        errorNoti.setTitleFont(font)
        errorNoti.setTextFont(font)
        errorNoti.show()

    def showWarn(title: LanguageList, desc: LanguageList, duration: int, isDark: bool, self):
        font = QFont()
        font.setFamily('Wanted Sans Variable')
        font.setPointSize(10)
        font.setBold(False)
        if(duration == None):
            duration = 21000

        errorNoti = Toast(self)
        errorNoti.setTitle(Language.getLanguageByEnum(title))
        errorNoti.setText(Language.getLanguageByEnum(desc))
        if(isDark == True):
            errorNoti.applyPreset(ToastPreset.WARNING_DARK)
        else:
            errorNoti.applyPreset(ToastPreset.WARNING)
        errorNoti.setDuration(duration)
        errorNoti.setTitleFont(font)
        errorNoti.setTextFont(font)
        errorNoti.show()

    def showSuccess(title: LanguageList, desc: LanguageList, duration: int, isDark: bool, self):
        font = QFont()
        font.setFamily('Wanted Sans Variable')
        font.setPointSize(10)
        font.setBold(False)
        if(duration == None):
            duration = 21000

        errorNoti = Toast(self)
        errorNoti.setTitle(Language.getLanguageByEnum(title))
        errorNoti.setText(Language.getLanguageByEnum(desc))
        if(isDark == True):
            errorNoti.applyPreset(ToastPreset.SUCCESS_DARK)
        else:
            errorNoti.applyPreset(ToastPreset.SUCCESS)
        errorNoti.setDuration(duration)
        errorNoti.setTitleFont(font)
        errorNoti.setTextFont(font)
        errorNoti.show()

    def showErrorStr(title: LanguageList, desc: str, duration: int,  isDark: bool, self):
        font = QFont()
        font.setFamily('Wanted Sans Variable')
        font.setPointSize(10)
        font.setBold(False)
        if(duration == None):
            duration = 21000
        
        errorNoti = Toast(self)
        errorNoti.setTitle(Language.getLanguageByEnum(title))
        errorNoti.setText(desc)
        if(isDark == True):
            errorNoti.applyPreset(ToastPreset.ERROR_DARK)
        else:
            errorNoti.applyPreset(ToastPreset.ERROR)
        errorNoti.setDuration(duration)
        errorNoti.setTitleFont(font)
        errorNoti.setTextFont(font)
        errorNoti.show()
    
    def showInfoStr(title: LanguageList, desc: str, duration: int, isDark: bool, self):
        font = QFont()
        font.setFamily('Wanted Sans Variable')
        font.setPointSize(10)
        font.setBold(False)
        if(duration == None):
            duration = 21000
        
        errorNoti = Toast(self)
        errorNoti.setTitle(Language.getLanguageByEnum(title))
        errorNoti.setText(desc)
        if(isDark == True):
            errorNoti.applyPreset(ToastPreset.INFORMATION_DARK)
        else:
            errorNoti.applyPreset(ToastPreset.INFORMATION)
        errorNoti.setDuration(duration)
        errorNoti.setTitleFont(font)
        errorNoti.setTextFont(font)
        errorNoti.show()

    def showWarnStr(title: LanguageList, desc: str, duration: int, isDark: bool, self):
        font = QFont()
        font.setFamily('Wanted Sans Variable')
        font.setPointSize(10)
        font.setBold(False)
        if(duration == None):
            duration = 21000
        
        errorNoti = Toast(self)
        errorNoti.setTitle(Language.getLanguageByEnum(title))
        errorNoti.setText(desc)
        if(isDark == True):
            errorNoti.applyPreset(ToastPreset.WARNING_DARK)
        else:
            errorNoti.applyPreset(ToastPreset.WARNING)
        errorNoti.setDuration(duration)
        errorNoti.setTitleFont(font)
        errorNoti.setTextFont(font)
        errorNoti.show()

    def showSuccessStr(title: LanguageList, desc: str, duration: int, isDark: bool, self):
        font = QFont()
        font.setFamily('Wanted Sans Variable')
        font.setPointSize(10)
        font.setBold(False)
        if(duration == None):
            duration = 21000
        
        errorNoti = Toast(self)
        errorNoti.setTitle(Language.getLanguageByEnum(title))
        errorNoti.setText(desc)
        if(isDark == True):
            errorNoti.applyPreset(ToastPreset.SUCCESS_DARK)
        else:
            errorNoti.applyPreset(ToastPreset.SUCCESS)
        errorNoti.setDuration(duration)
        errorNoti.setTitleFont(font)
        errorNoti.setTextFont(font)
        errorNoti.show()