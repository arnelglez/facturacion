import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_UnidadMedida import *
from modelo.modUnidadMedida import mUnidadMedida, eUnidadMedida
from funciones.generales import FuncionesGenerales


class VentanaUnidadMedida(QtWidgets.QMainWindow, Ui_VentanaUnidadMedida):

    def __init__(self, unidadmedida:eUnidadMedida , parent = None):
        super(VentanaUnidadMedida, self).__init__()

        self.parent = parent
        self.eunidadmedida = unidadmedida
        self.munidad = mUnidadMedida()
        self.generales = FuncionesGenerales()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaUnidadMedida.__init__(self)
        self.setupUi(self)

    def inicializacionVentana(self, ventana):     
        if self.eunidadmedida.getIdUnidadMedida() == "": # es porque vamos a insertar nueva unidad de medida
            ventana.setWindowTitle("Insertar Unidad de Medida")
        else:
            self.editDescripcion.setText(self.eunidadmedida.getDescripcion())
            self.editSigla.setText(self.eunidadmedida.getSigla())
            ventana.setWindowTitle("Modificar Unidad de Medida")
        
    def verificarCampos(self):
        if self.editDescripcion.text() != "" and self.editSigla.text() != "":
            self.buttonAceptar.setEnabled(True)
        else:
            self.buttonAceptar.setEnabled(False)

    def guardarUnidadMedida(self, ventana):
        eumedida = eUnidadMedida()
        eumedida.setIdUnidadMedida(self.eunidadmedida.getIdUnidadMedida())
        eumedida.setDescripcion(self.editDescripcion.text())
        eumedida.setSigla(self.editSigla.text())
        eumedida.setActivo(1)
        if self.eunidadmedida.getIdUnidadMedida() == "":
            self.munidad.guardarDatosUnidadMedida(eumedida)
        else:
            self.munidad.editarDatosUnidadMedida(eumedida,1)
        lista = self.munidad.cargarDatosUnidadMedida()
        self.parent.llenadoTablaUnidadMedida(lista) 
        self.generales.cerrarVentana(ventana)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaUnidadMedida()
    ventana.show()
    sys.exit(app.exec())