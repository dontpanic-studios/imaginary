from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit, QFileDialog, QCheckBox, QComboBox, QRadioButton
from PyQt6.QtGui import QIcon
from PyQt6 import QtCore
from PyQt6.QtCore import QSize
from src.gui.label import whynotclick
import os, sys, logging, json, subprocess, traceback
from dotenv import load_dotenv
from src.language.lang import LanguageList
from src.language.lang import Language

log = logging
logFilePath = './log/debug-log.log'
load_dotenv('./data/setting.env')

class VMControl(QWidget):
    def __init__(self):
        try:
            super().__init__()

            self.width = 400
            self.height = 300

            self.setWindowTitle(Language.getLanguageByEnum(LanguageList.VMCONTROL_TITLE))
            self.setStyleSheet("background-color: #262626; Color : white;")
            self.setWindowIcon(QIcon('src/png/icons/128.png'))