from PyQt6.QtCore import QEvent, pyqtSignal, QObject
from PyQt6.QtGui import QMouseEvent

def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()
        
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseReleaseEvent:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False
    
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked