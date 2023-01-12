import enum
import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Anticipo import *
from control.devolucion import *
from control.liquidacion import *
from modelo.modUsuario import mUsuario, eUsuario
from modelo.modCobro import mCobro, eCobro
from modelo.modCobroFactura import mCobroFactura, eCobroFactura
from modelo.modCliente import mCliente, eCliente
from modelo.modAnticipo import mAnticipo, eAnticipo
from funciones.generales import FuncionesGenerales
from funciones.visuales import Tablas

class VentanaAnticipo(QtWidgets.QMainWindow, Ui_VentanaAnticipo):

    def __init__(self, usuario:eUsuario, parent = None):
        super(VentanaAnticipo, self).__init__()

        self.generales = FuncionesGenerales()
        self.tablas = Tablas()
        self.usuario = usuario
        self.parent = parent
        self.mcobro = mCobro()
        self.mcobrofactura = mCobroFactura()
        self.mcliente = mCliente()
        self.manticipo = mAnticipo()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaAnticipo.__init__(self)
        self.setupUi(self)
    
    #menu clic derecho en la tabla
    def contexMenuEvent(self, pos):   
        self.filaSeleccionada()
        menuTabla = QtWidgets.QMenu(self)
        menuTabla.addAction(self.actionLiquidar)
        menuTabla.addAction(self.actionDevolver)

        menuTabla.exec(self.tableAnticipo.mapToGlobal(pos))

    # inicializo la ventana
    def inicializarVentana(self):
        self.actionDevolver.setEnabled(False)
        self.actionLiquidar.setEnabled(False)

        anticipos = self.cargarAnticiposCobros()

        self.llenarTabla(anticipos)


    # obtengo todos los campos de anticipos
    def cargarAnticiposCobros(self):    
        facturacobro = self.mcobrofactura.cargarDatosCobroFactura()
        listAnticipos = list()

        for fact in facturacobro:
            if fact.getTipo() == 2:
                cobro = self.mcobro.obtenerCobroEspecifico(fact.getCobro())
                if cobro.getEstado() == 2: # verifico que este confirmada
                    listAnticipos.append(fact)
        
        return listAnticipos
    
    # dejo solo los anticipos pendientes
    def anticipoActivo(self, anticipo:eCobroFactura):
        result = anticipo.getMonto()
        for data in self.manticipo.cargarDatosAnticipo():
            if data.getCobroFactura() == anticipo.getIdCobroFactura() and data.getEstado() != 0: #verifico el cobrofactura y el estado
                result -= data.getMonto()
                
        return result

    def llenarTabla(self, anticipos):
        self.headerAnticipo()

        for fila, data in enumerate(anticipos):
            self.tableAnticipo.insertRow(fila)

            cobro = self.mcobro.obtenerCobroEspecifico(data.getCobro())
            cliente = self.mcliente.obtenerDatosClientesEspecifica(cobro.getCliente())

            monto = self.anticipoActivo(data)

            self.tableAnticipo.setItem(fila, 0, QTableWidgetItem(str(data.getIdCobroFactura())))
            self.tableAnticipo.setItem(fila, 1, QTableWidgetItem(str(cliente.getNombre())))
            self.tableAnticipo.setItem(fila, 2, QTableWidgetItem(str(cobro.getFecha())))
            self.tableAnticipo.setItem(fila, 3, QTableWidgetItem(self.generales.floatToStr(monto)))
            self.tableAnticipo.setItem(fila, 4, QTableWidgetItem(str(cliente.getIdCliente())))
            if monto == 0:
                self.tableAnticipo.setRowHidden(fila, True)
            else:
                self.tableAnticipo.setRowHidden(fila, False)
            
    # encabezado de tabla
    def headerAnticipo(self):
        self.tableAnticipo.clear()
        self.tableAnticipo.setRowCount(0)
        self.tableAnticipo.setColumnCount(5)

        #ancho de las columnas
        self.tableAnticipo.setColumnWidth(0,0)
        self.tableAnticipo.setColumnWidth(1,500)
        self.tableAnticipo.setColumnWidth(2,98)
        self.tableAnticipo.setColumnWidth(3,98)
        self.tableAnticipo.setColumnWidth(4,0)

        self.tableAnticipo.setColumnHidden(0,True)
        self.tableAnticipo.setColumnHidden(4,True)
        #cabecera de la tabla

        self.tablas.headerAnticipos(0, self.tableAnticipo)    
        self.tablas.headerAnticipos(1, self.tableAnticipo)    
        self.tablas.headerAnticipos(2, self.tableAnticipo)    
        self.tablas.headerAnticipos(3, self.tableAnticipo)     
        self.tablas.headerAnticipos(4, self.tableAnticipo)     
            
    
    def filaSeleccionada(self):
        fila = self.tableAnticipo.currentRow()
        if fila != -1:
            self.actionLiquidar.setEnabled(True)
            self.actionDevolver.setEnabled(True)

    def devolucionAnticipo(self, ventana):
        eanticipo = eAnticipo()
        fila = self.tableAnticipo.currentRow()
        eanticipo.setCobroFactura(self.tableAnticipo.item(fila, 0).text())
        eanticipo.setCliente(self.tableAnticipo.item(fila, 4).text())

        self.ventanaDevolucion = QtWidgets.QDialog()
        self.ui = VentanaDevolucion(eanticipo, self.usuario, self.parent)
        self.ui.setupUi(self.ventanaDevolucion) 
        self.generales.cerrarVentana(ventana)
        self.ventanaDevolucion.exec()

    def liquidacionAnticipo(self, ventana):
        eanticipo = eAnticipo()
        fila = self.tableAnticipo.currentRow()
        eanticipo.setCobroFactura(self.tableAnticipo.item(fila, 0).text())
        eanticipo.setCliente(self.tableAnticipo.item(fila, 4).text())

        self.ventanaLiquidacion = QtWidgets.QDialog()
        self.ui = VentanaLiquidacion(eanticipo, self.usuario, self.parent)
        self.ui.setupUi(self.ventanaLiquidacion) 
        self.generales.cerrarVentana(ventana)
        self.ventanaLiquidacion.exec()


     
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaAnticipo()
    ventana.show()
    sys.exit(app.exec())
