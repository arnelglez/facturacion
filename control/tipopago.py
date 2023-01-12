from funciones.generales import FuncionesGenerales
import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_TipoPago import *
from modelo.modTipoPago import eTipoPago, mTipoPago


class VentanaTipoPago(QtWidgets.QMainWindow, Ui_VentanaTipoPago):

    def __init__(self, etipopago ,parent = None):
        super(VentanaTipoPago, self).__init__()

        self.parent = parent
        self.etipopago = etipopago
        self.mtipopago = mTipoPago()
        self.generales = FuncionesGenerales()
        

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaTipoPago.__init__(self)
        self.setupUi(self)

    def inicializacionVentana(self, ventana):     
        if self.etipopago.getIdTipoPago() == "": # es porque vamos a insertar nuevo tipo de pago
            ventana.setWindowTitle("Insertar Tipo de Pago")
        else:
            self.editDescripcion.setText(self.etipopago.getDescripcion())
            ventana.setWindowTitle("Modificar Tipo de Pago")
        
    def verificarCampos(self):
        if self.editDescripcion.text() != "":
            self.buttonAceptar.setEnabled(True)
        else:
            self.buttonAceptar.setEnabled(False)

    def guardarTipoPago(self, ventana):
        eumedida = eTipoPago()
        eumedida.setIdTipoPago(self.etipopago.getIdTipoPago())
        eumedida.setDescripcion(self.editDescripcion.text())
        eumedida.setActivo(1)
        if self.etipopago.getIdTipoPago() == "":
            self.mtipopago.guardarDatosTipoPago(eumedida)
        else:
            self.mtipopago.editarDatosTipoPago(eumedida, 1)
        lista = self.mtipopago.cargarDatosTipoPago()
        self.parent.llenadoTablaTipoPago(lista) 
        self.generales.cerrarVentana(ventana)