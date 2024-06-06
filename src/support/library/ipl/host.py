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

    """
    Replace Widget to different location
    :param widget: QWidgets
    :param x: x loc
    :param y: y loc
    """
    def relocateWidget(widget, x: int, y: int):
        try:
            widget.move(x, y)
        except:
            raise Exceptions.InvaildCodeInjection
    
    """
    Returing methods from Main Class
    :return: List
    """
    def getWidgets():
        try:
            returned = inspect.getmembers(main.Main, predicate=inspect.ismethod)
            return returned
        except:
            raise Exceptions.InvaildCodeInjection
    
    def accessMainModule():
        try:
            from main import Main
            return Main
        except:
            raise Exceptions.InvaildCodeInjection
    