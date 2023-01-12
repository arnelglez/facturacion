
import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_BuscarCliente import *
from funciones.generales import FuncionesGenerales
from funciones.visuales import Tablas
from modelo.modCliente import eCliente, mCliente


class VentanaBuscarCliente(QtWidgets.QMainWindow, Ui_VentanaBuscarCliente):

    def __init__(self, parent = None):
        super(VentanaBuscarCliente, self).__init__()

        self.parent = parent
        self.generales = FuncionesGenerales()
        self.mclient = mCliente()
        self.tablas = Tablas()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaBuscarCliente.__init__(self)
        self.setupUi(self)

    def llenadoTabla(self):
        lista = list()
        busqueda = self.editCliente.text()
        lista = self.mclient.busquedaClientes(busqueda)

        self.tableCliente.clear()
        self.tableCliente.setRowCount(0)
        for fila, data in enumerate(lista):
            self.tableCliente.insertRow(fila)   
            self.tableCliente.setItem(fila, 0,QTableWidgetItem(str(data.getIdCliente())))    
            self.tablas.headerBuscarCliente(0, self.tableCliente)
            self.tableCliente.setItem(fila, 1,QTableWidgetItem(data.getNombre()))    
            self.tablas.headerBuscarCliente(1, self.tableCliente)
            if data.getActivo() == 0:
                self.tableCliente.setRowHidden(fila, True)

    def habilitarBoton(self):
        self.buttonAceptar.setEnabled(True)

    def clienteSeleccionado(self, ventana):
        eclient = eCliente()
        fila = self.tableCliente.currentRow()
        idcliente = self.tableCliente.item(fila, 0).text()
        cliente = self.mclient.obtenerDatosClientesEspecifica(int(idcliente))
        self.parent.clienteSeleccionado(cliente)
        self.generales.cerrarVentana(ventana)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaBuscarCliente()
    ventana.show()
    sys.exit(app.exec())