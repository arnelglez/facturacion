import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Acerca import *
from funciones.generales import FuncionesGenerales


class VentanaAcerca(QtWidgets.QMainWindow, Ui_VentanaAcerca):

    def __init__(self):

        self.generales = FuncionesGenerales()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaAcerca.__init__(self)
        self.setupUi(self)

    def cerrarVentana(self, ventana):
        self.generales.cerrarVentana(ventana)
  
     
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaAcerca()
    ventana.show()
    sys.exit(app.exec())
