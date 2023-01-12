from datetime import datetime
import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Liquidacion import *
from control.buscarfactura import *
from funciones.generales import FuncionesGenerales
from modelo.modUsuario import eUsuario
from modelo.modCliente import mCliente ,eCliente
from modelo.modCobroFactura import mCobroFactura, eCobroFactura
from modelo.modFactura import mFactura, eFactura
from modelo.modAnticipo import mAnticipo, eAnticipo


class VentanaLiquidacion(QtWidgets.QMainWindow, Ui_VentanaLiquidacion):

    def __init__(self, anticipo:eAnticipo, usuario:eUsuario, parent = None):
        super(VentanaLiquidacion, self).__init__()

        self.generales = FuncionesGenerales()
        self.anticipo = anticipo
        self.usuario = usuario
        self.parent = parent
        self.monto = ""
        self.factura = ""

        self.manticipo = mAnticipo()
        self.mcliente = mCliente()
        self.mcobrofactura = mCobroFactura()
        self.mfactura = mFactura()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaLiquidacion.__init__(self)
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
            aux = self.mcobrofactura.obtenerCobroFacturaEspecifico(self.anticipo.getCobroFactura())
            monto = aux.getMonto()
            factura = ""
            self.buttonAceptar.setEnabled(False)
        else:
            numero = self.anticipo.getNoAnticipo()
            fecha = self.anticipo.getFecha()
            documento = self.anticipo.getDocumento()
            monto = self.anticipo.getMonto()
            factura = mFactura().obtenerFacturaEspecifico(int(self.anticipo.getFactura())).getNoFactura()

            if self.anticipo.getEstado() != 1:
                self.editMonto.setEnabled(False)
                self.buttonAceptar.setEnabled(False)
                self.editFactura.setEnabled(False)
                self.buttonFactura.setEnabled(False)

        cliente = self.mcliente.obtenerDatosClientesEspecifica(self.anticipo.getCliente())
        self.editFecha.setText(fecha)
        self.editDocumento.setText(numero)
        self.editFactura.setText(factura)
        self.labelCliente.setText(cliente.getNombre())
        self.monto = self.generales.floatToStr(monto) 
        self.editMonto.setText(self.monto)
        ventana.setWindowTitle('Liquidación _ ' + numero)

    def verificarFactura(self):
        nofactura = self.editFactura.text()
        buscar = True
        facturas =  self.mfactura.cargarDatosFactura()
        if facturas.__len__() > 0:
            for fac in facturas:
                if fac.getNoFactura() == nofactura and fac.getCliente() == self.anticipo.getCliente() and fac.getEstado == 1:
                    self.facturaSeleccionada(fac)
                    buscar = False
                    break

        if buscar == True:
            self.buscarFactura()

    # abre la ventana de buscar equipos
    def buscarFactura(self):        
        self.ventanaBuscarFactura = QtWidgets.QDialog()
        self.ui = VentanaBuscarFactura(cliente=int(self.anticipo.getCliente()), parent=self)
        self.ui.setupUi(self.ventanaBuscarFactura) 
        self.ventanaBuscarFactura.exec()

    def facturaSeleccionada(self, efactura:eFactura):
        self.factura = efactura
        self.editFactura.setText(self.factura.getNoFactura())
        fact = self.generales.floatToStr(self.factura.getTotalFactura())
        self.buttonAceptar.setEnabled(True)
        if float(self.factura.getTotalFactura()) < float(self.monto):
            self.editMonto.setText(fact)
        else:
            self.editMonto.setText(self.monto)


    def guardarLiquidacion(self, ventana):
        if float(self.monto) < float(self.editMonto.text()):
            self.generales.mensageInformacion("informacion",
                                "Error en el monto",
                                "El monto de dinero a liquidar no puede ser superior al del pago anticipado.      ")
        
        else:
            self.anticipo.setEstado(1)
            self.anticipo.setFactura(self.factura.getIdFactura())
            self.anticipo.setFecha(self.editFecha.text())
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
    ventana = VentanaLiquidacion()
    ventana.show()
    sys.exit(app.exec())
