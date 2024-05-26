import main, inspect
from PyQt6.QtWidgets import QWidget
from src.support.library.ipl_exception import Exceptions

class Host:
    """
    Inject CSS Theme into Main Window.
    :param css: CSS Code for PyQt6
    :param window: QWidget Window
    :return: Updated Theme
    """
    def injectTheme(css: str, window: QWidget):
        try:
            window.setStyleSheet(window, css)
        except:
            raise Exceptions.InvaildCodeInjection
    
    """
    Returing functions from Main Class
    :return: List
    """
    def getModules():
        try:
            returned = inspect.getmembers(main.Main, predicate=inspect.isfunction)
            return returned
        except:
            raise Exceptions.InvaildCodeInjection

    #depra
    def replaceWidget(widget):
        try:
            pass
        except:
            raise Exceptions.InvaildCodeInjection