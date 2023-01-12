from datetime import datetime
import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Devolucion import *
from funciones.generales import FuncionesGenerales
from modelo.modUsuario import eUsuario
from modelo.modCliente import mCliente ,eCliente
from modelo.modCobroFactura import mCobroFactura, eCobroFactura
from modelo.modAnticipo import mAnticipo, eAnticipo


class VentanaDevolucion(QtWidgets.QMainWindow, Ui_VentanaDevolucion):

    def __init__(self, anticipo:eAnticipo, usuario:eUsuario, parent = None):
        super(VentanaDevolucion, self).__init__()

        self.generales = FuncionesGenerales()
        self.anticipo = anticipo
        self.usuario = usuario
        self.parent = parent
        self.monto = ""

        self.manticipo = mAnticipo()
        self.mcliente = mCliente()
        self.mcobrofactura = mCobroFactura()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaDevolucion.__init__(self)
        self.setupUi(self)

    def inicializarVentana(self, ventana):
        if self.anticipo.getIdAnticipo() == "":
            anticipos = self.manticipo.cargarDatosAnticipo() 
            #generando el numero del documento
            if anticipos.__len__() > 0:
                documento = anticipos[-1].getNoAnticipo()
            else:
                documento = ""
            fecha = self.generales.fechaDocumentos()
            numero = self.generales.numeroDocumento(documento)
            self.dateFechaEmision.setDate(datetime.strptime(self.generales.fechaDocumentos(), '%d/%m/%Y'))
            aux = self.mcobrofactura.obtenerCobroFacturaEspecifico(self.anticipo.getCobroFactura())
            monto = aux.getMonto()
            documento = ""
        else:
            numero = self.anticipo.getNoAnticipo()
            fecha = self.anticipo.getFecha()
            documento = self.anticipo.getDocumento()
            self.dateFechaEmision.setDate(datetime.strptime(self.anticipo.getFechaEmision(), '%d/%m/%Y'))
            monto = self.anticipo.getMonto()

            if self.anticipo.getEstado() != 1:
                self.editNumero.setEnabled(False)
                self.editMonto.setEnabled(False)
                self.dateFechaEmision.setEnabled(False)
                self.buttonAceptar.setEnabled(False)

        cliente = self.mcliente.obtenerDatosClientesEspecifica(self.anticipo.getCliente())
        self.editFecha.setText(fecha)
        self.editDocumento.setText(numero)
        self.editNumero.setText(documento)
        self.labelCliente.setText(cliente.getNombre())
        self.monto = self.generales.floatToStr(monto) 
        self.editMonto.setText(self.monto)
        ventana.setWindowTitle('Devolución _ ' + numero)

    def guardarDevolucion(self, ventana):
        if float(self.monto) < float(self.editMonto.text()):
            self.generales.mensageInformacion("informacion",
                                "Error en el monto",
                                "El monto de dinero a devolver no puede ser superior al del pago anticipado.      ")
        
        else:
            self.anticipo.setDocumento(self.editNumero.text())
            self.anticipo.setEstado(1)
            self.anticipo.setFactura("")
            self.anticipo.setFecha(self.editFecha.text())
            self.anticipo.setFechaEmision(self.dateFechaEmision.text())
            self.anticipo.setMonto(self.editMonto.text())
            self.anticipo.setNoAnticipo(self.editDocumento.text())
            self.anticipo.setUsuario(self.usuario.getIdUsuario())
            if self.anticipo.getIdAnticipo() == "":
                self.manticipo.guardarDatosAnticipo(self.anticipo)                
            else:
                self.manticipo.editarDatosAnticipo(self.anticipo, 1)
            
            self.parent.configuracionBotonesMenu(4)
            self.cerrarVentana(ventana)

    def cerrarVentana(self, ventana):
        self.generales.cerrarVentana(ventana)
  
     
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaDevolucion()
    ventana.show()
    sys.exit(app.exec())
