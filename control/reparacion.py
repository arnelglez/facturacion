from operator import truediv
from funciones.generales import FuncionesGenerales
import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Reparacion import *
from modelo.modEquipo import eEquipo, mEquipo


class VentanaReparacion(QtWidgets.QMainWindow, Ui_VentanaReparacion):

    def __init__(self, equipo ,parent = None):
        super(VentanaReparacion, self).__init__()

        self.parent = parent
        self.equipo = equipo
        self.mequipo = mEquipo()
        self.generales = FuncionesGenerales()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaReparacion.__init__(self)
        self.setupUi(self)

    def inicializacionVentana(self, ventana):     
        if self.equipo.getIdEquipo() == "": # es porque vamos a insertar nuevo tipo de equipo
            ventana.setWindowTitle("Insertar Equipo")
        else:
            self.editDescripcion.setText(self.equipo.getDescripcion())
            if self.equipo.getMultiple() == 1:
                marcado = True
            else:
                marcado = False

            self.checkBox.setChecked(marcado)
            ventana.setWindowTitle("Modificar Equipo")
    

        
    def verificarCampos(self):
        if self.editDescripcion.text() != "":
            self.buttonAceptar.setEnabled(True)
        else:
            self.buttonAceptar.setEnabled(False)

    def guardarEquipo(self, ventana):
        eumedida = eEquipo()
        eumedida.setIdEquipo(self.equipo.getIdEquipo())
        eumedida.setDescripcion(self.editDescripcion.text())            
        if self.checkBox.isChecked():
            marcado = True
        else:
            marcado = False
        eumedida.setMultiple(marcado)
        eumedida.setActivo(1)
        if self.equipo.getIdEquipo() == "":
            self.mequipo.guardarDatosEquipo(eumedida)
        else:
            self.mequipo.editarDatosEquipo(eumedida,1)
        lista = self.mequipo.cargarDatosEquipo()
        self.parent.llenadoTablaEquipo(lista) 
        self.generales.cerrarVentana(ventana)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaReparacion()
    ventana.show()
    sys.exit(app.exec())