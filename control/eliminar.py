
import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Eliminar import *
from funciones.generales import FuncionesGenerales


class VentanaEliminar(QtWidgets.QMainWindow, Ui_VentanaEliminar):

    def __init__(self, texto, parent = None):
        super(VentanaEliminar, self).__init__()

        self.parent = parent
        self.labelTexto = texto
        self.generales = FuncionesGenerales()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaEliminar.__init__(self)
        self.setupUi(self)

    def respuestaVentana(self, boton ,ventana):
        self.parent.eliminando(boton)
        self.generales.cerrarVentana(ventana)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaEliminar()
    ventana.show()
    sys.exit(app.exec())