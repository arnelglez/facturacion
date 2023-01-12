
import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_BuscarFactura import *
from funciones.generales import FuncionesGenerales
from funciones.visuales import Tablas
from modelo.modFactura import eFactura, mFactura
from modelo.modCobroFactura import eCobroFactura, mCobroFactura
from modelo.modAnticipo import mAnticipo


class VentanaBuscarFactura(QtWidgets.QMainWindow, Ui_VentanaBuscarFactura):

    def __init__(self, cliente, editFactura = None, editImporte = None, fila = None, parent = None):
        super(VentanaBuscarFactura, self).__init__()

        self.cliente = cliente
        self.fila = fila
        self.editfactura = editFactura
        self.editimporte = editImporte
        self.parent = parent
        self.generales = FuncionesGenerales()
        self.mfactura = mFactura()
        self.mcobrofact = mCobroFactura()
        self.manticipo = mAnticipo()
        self.tablas = Tablas()


        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaBuscarFactura.__init__(self)
        self.setupUi(self)

    def llenadoTabla(self):
        lista = list()
        busqueda = self.editFactura.text()
        lista = self.mfactura.busquedaFactura(busqueda, self.cliente)

        self.tableFactura.clear()
        self.tableFactura.setRowCount(0)
        for fila, data in enumerate(lista):
            self.tableFactura.insertRow(fila)   
            self.tableFactura.setItem(fila, 0,QTableWidgetItem(str(data.getIdFactura())))    
            self.tablas.headerBuscarFactura(0, self.tableFactura)
            self.tableFactura.setItem(fila, 1,QTableWidgetItem(data.getNoFactura()))    
            self.tablas.headerBuscarFactura(1, self.tableFactura)
            self.tableFactura.setItem(fila, 2,QTableWidgetItem(self.generales.floatToStr(data.getTotalFactura())))    
            self.tablas.headerBuscarFactura(2, self.tableFactura)

            faltante = self.pagoFaltante(data.getIdFactura(), data.getTotalFactura())
            if data.getEstado() == 2 and not self.enUso(data.getIdFactura()):
                self.tableFactura.setRowHidden(fila, False)
            elif data.getEstado() == 4 and faltante != 0: 
                self.tableFactura.setRowHidden(fila, False)
                self.tableFactura.setItem(fila, 2,QTableWidgetItem(self.generales.floatToStr(faltante)))  
            else:
                self.tableFactura.setRowHidden(fila, True)

    def enUso(self, idFactura):
        result = False
        for cobro in self.mcobrofact.cargarDatosCobroFactura():
            if cobro.getFactura() == idFactura:
                result = True

        return result

    def pagoFaltante(self, idfactura, total):
        cobros = self.mcobrofact.cargarDatosCobroFactura()
        anticipos = self.manticipo.cargarDatosAnticipo()
        for cobro in cobros:
            if cobro.getFactura() == idfactura:
                total -= cobro.getMonto()

        for anticipo in anticipos:
            if anticipo.getFactura() == idfactura and anticipo.getEstado() != 0:
                total -= anticipo.getMonto()

        return total
        

    def habilitarBoton(self):
        self.buttonAceptar.setEnabled(True)

    def facturaSeleccionada(self, ventana):
        fila = self.tableFactura.currentRow()
        idfactura = self.tableFactura.item(fila, 0).text()
        efactura = eFactura()
        factura = self.mfactura.obtenerFacturaEspecifico(int(idfactura))

        efactura.setIdFactura(factura.getIdFactura())
        efactura.setNoFactura(factura.getNoFactura())
        efactura.setCliente(factura.getCliente())
        efactura.setFichaCliente(factura.getFichaCliente())
        efactura.setUsuario(factura.getUsuario())
        efactura.setFecha(factura.getFecha())
        efactura.setEstado(factura.getEstado())
        if self.tableFactura.item(fila, 2).text() != self.generales.floatToStr(factura.getTotalFactura()):
            efactura.setTotalFactura(self.tableFactura.item(fila, 2).text())
        else:
            efactura.setTotalFactura(factura.getTotalFactura())

        if self.editfactura == None:
            self.parent.facturaSeleccionada(efactura)
        else:
            self.parent.facturaSeleccionada(efactura, self.editfactura, self.editimporte, self.fila)
        self.generales.cerrarVentana(ventana)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaBuscarFactura()
    ventana.show()
    sys.exit(app.exec())
