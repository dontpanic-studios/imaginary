from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6 import QtCore
import os

class FallBackUI(QWidget):
    def __init__(self, errstr):
        super().__init__()

        self.width = 1280
        self.height = 720
        self.setWindowTitle("Imaginary - FallBack")
        self.setStyleSheet("background-color: #262626; Color : white;") 
        self.setFixedSize(self.width, self.height)
        self.setWindowFlags(QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint)

        self.frownface = QLabel(':(', self)
        self.err_desc = QLabel('알수 없는 오류가 발생하여 FallBack UI가 작동했어요, 안타깝게도 여기선 아무것도 할수 없어요.\nAs Unknown error has been appeared, FallBack UI has been occurred.\nUn-fortuantly you cannot do anything on this screen.')
        self.err_full = QLabel(errstr, self)

        self.font_normal = self.frownface.font()
        self.font_normal.setBold(True)
        self.font_normal.setPointSize(15)
        self.font_normal.setFamily(os.environ.get('Font'))

        self.frownface.setFont(self.font_normal)
        self.err_desc.setFont(self.font_normal)