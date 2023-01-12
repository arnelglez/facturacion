from os import close
from PyQt6 import QtCore, QtGui
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import  QAbstractButton, QComboBox, QLabel, QLineEdit, QMessageBox, QPushButton, QWidget


class QLabelClickable(QLabel):
 
    clicked = pyqtSignal()
    
    def __init__(self, *args):
        QLabel.__init__(self, *args)
   
    def mouseReleaseEvent(self, event):
        self.clicked.emit()

class QEditClickable(QLineEdit):

    clicked = pyqtSignal()
    
    def __init__(self, *args):
        QLineEdit.__init__(self, *args)
   
    def mouseReleaseEvent(self, event):
        self.clicked.emit()

class QComboReturn(QComboBox):

    returnPressed = pyqtSignal()
    clicked = pyqtSignal()
    textChanged = pyqtSignal()

    def  __init__(self, *args):
        QComboBox.__init__(self, *args)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key(16777220) or  event.key() == QtCore.Qt.Key(16777221):
            self.returnPressed.emit()
        else:
            super().keyPressEvent(event)
   
    def mouseReleaseEvent(self, event):
        self.clicked.emit()