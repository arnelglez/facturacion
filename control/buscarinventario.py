
import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_BuscarInventario import *
from funciones.generales import FuncionesGenerales
from funciones.visuales import Tablas
from modelo.modInventario import eInventario, mInventario
from modelo.modRecepcion import mRecepcion, eRecepcion
from modelo.modMarca import mMarca, eMarca
from modelo.modModelo import mModelo, eModelo
from modelo.modFacturaDesglose import eFacturaDesglose
from modelo.modEquipo import mEquipo



class VentanaBuscarInventario(QtWidgets.QMainWindow, Ui_VentanaBuscarInventario):

    def __init__(self, cliente, equipo, edit, fila = None, parent = None):
        super(VentanaBuscarInventario, self).__init__()

        self.parent = parent
        self.cliente = cliente
        self.equipo = equipo
        self.edit = edit
        self.fila = fila
        self.generales = FuncionesGenerales()
        self.mclient = mInventario()
        self.tablas = Tablas()
        self.mrecepcion = mRecepcion()
        self.minventario = mInventario()
        self.mmarca = mMarca()
        self.mmodelo = mModelo()
        self.mequipo = mEquipo()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaBuscarInventario.__init__(self)
        self.setupUi(self)

    def buscarInventarios(self):
        inventarios = self.minventario.cargarDatosInventario()
        recepciones = self.mrecepcion.cargarDatosRecepcion()
        lista = list()
        for recepcion in recepciones:
            if recepcion.getEstado() == 2 and recepcion.getCliente() == self.cliente:
                for inventario in inventarios:
                    if inventario.getActivo() != 0 and inventario.getRecepcion() == recepcion.getIdRecepcion() and inventario.getEquipo() == self.equipo:
                        lista.append(inventario)
        return lista

    def llenadoTabla(self):
        self.editInventario.setFocus()
        self.tableInventario.clear()
        self.tableInventario.setRowCount(0)
        listainventario = self.buscarInventarios()            
        self.tablas.headerBuscarInventario(0, self.tableInventario)
        self.tablas.headerBuscarInventario(1, self.tableInventario)
        self.tablas.headerBuscarInventario(2, self.tableInventario)
        for fila, inventario in enumerate(listainventario):
            self.tableInventario.insertRow(fila)
            noinventario = inventario.getNoInventario()
            equipo = self.mequipo.obtenerEquipoEspecifico(inventario.getEquipo())
            marca = self.mmarca.obtenerMarcaEspecifico(inventario.getMarca())
            modelo = self.mmodelo.obtenerModeloEspecifico(inventario.getModelo())
            
            medio = equipo.getDescripcion() 
            if marca.getDescripcion() != '':
                medio = medio + ' ' + marca.getDescripcion()
            if modelo.getDescripcion() != '':
                medio = medio + ' ' + modelo.getDescripcion()

            self.tableInventario.setItem(fila, 0, QTableWidgetItem(str(inventario.getIdInventario())))
            self.tableInventario.setItem(fila, 1, QTableWidgetItem(noinventario))
            self.tableInventario.setItem(fila, 2, QTableWidgetItem(medio))

    def filtroFilasTabla(self):
        if self.editInventario.text()== "":
            for fila in range(self.tableInventario.rowCount()):
                self.tableInventario.setRowHidden(fila, False)            
        else:
            for fila in range(self.tableInventario.rowCount()):
                noinventario = str(self.tableInventario.item(fila, 1).text())
                noinventario = noinventario.lower()
                equipo = str(self.tableInventario.item(fila, 2).text())
                equipo = equipo.lower()
                busqueda = str(self.editInventario.text())
                busqueda = busqueda.lower()
                if noinventario.find(busqueda) != -1 or equipo.find(busqueda) != -1:
                    self.tableInventario.setRowHidden(fila, False)
                else:
                    self.tableInventario.setRowHidden(fila, True)


    def habilitarBoton(self):
        self.buttonAceptar.setEnabled(True)

    def clienteSeleccionado(self, ventana):
        fila = self.tableInventario.currentRow()
        idinventario = self.tableInventario.item(fila, 0).text()
        inventario = self.minventario.obtenerInventarioEspecifico(int(idinventario))
        self.parent.insertarEquipo(inventario, self.edit, self.fila)
        self.generales.cerrarVentana(ventana)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaBuscarInventario()
    ventana.show()
    sys.exit(app.exec())