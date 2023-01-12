import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Cliente import *
from control.fichacliente import *
from modelo.modCliente import mCliente, eCliente
from modelo.modFichaCliente import mFichaCliente, eFichaCliente
from modelo.modCargo import mCargo, eCargo
from funciones.visuales import Tablas


class VentanaCliente(QtWidgets.QMainWindow, Ui_VentanaCliente):

    def __init__(self, eclient:eCliente ,parent= None):
        super(VentanaCliente, self).__init__(parent)

        self.parent = parent
        self.eclient = eclient
        self.tablas = Tablas()
        self.mcliente = mCliente()
        self.mfcliente = mFichaCliente()
        self.generales = FuncionesGenerales()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaCliente.__init__(self)
        self.setupUi(self)

    #mostrar ventana dependiendo si es edicion o nuevo
    def inicializarVentana(self, ventana):
        if self.eclient.getIdCliente() == "": # es porque vamos a insertar nuevo cliente
            self.actionAdd.setEnabled(False)
            self.actionDelete.setEnabled(False)
            self.actionEdit.setEnabled(False)
            self.actionSave.setEnabled(False)
            ventana.setWindowTitle("Insertar Cliente")
        else:
            self.actionAdd.setEnabled(True)
            self.actionDelete.setEnabled(False)
            self.actionEdit.setEnabled(False)
            self.actionSave.setEnabled(False)
            self.editCliente.setText(self.eclient.getNombre())
            self.editContrato.setText(self.eclient.getContrato())
            self.editCuenta.setText(self.eclient.getCuenta())
            self.editDireccion.setText(self.eclient.getDireccion())
            self.inicializacionFichaCliente()
            ventana.setWindowTitle("Modificar Cliente")

    #inicializando los datos para la tabla ficha de clientes
    def inicializacionFichaCliente(self):
        listaFichaClientes = self.mfcliente.cargarDatosFichaCliente()
        if listaFichaClientes.__len__() > 0:
            self.llenadoTablaFichaCliente(listaFichaClientes)

    
    #llenando tabla de los pertenecientes a la ficha de cliente
    def llenadoTablaFichaCliente(self, lista):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        for fila, data in enumerate(lista):
            self.tableWidget.insertRow(fila)   
            self.tableWidget.setItem(fila, 0,QTableWidgetItem(str(data.getIdFichaCliente())))    
            self.tablas.headerFichaClientes(0, self.tableWidget)
            nombre = data.getNombre()
            apellido = data.getApellidos()
            self.tableWidget.setItem(fila, 1,QTableWidgetItem(nombre + ' ' + apellido ))    
            self.tablas.headerFichaClientes(1, self.tableWidget)
            self.tableWidget.setItem(fila, 2,QTableWidgetItem(data.getCarnet()))    
            self.tablas.headerFichaClientes(2, self.tableWidget)
            cargo = self.obtenerCargos(data.getCargo())
            self.tableWidget.setItem(fila, 3,QTableWidgetItem(cargo))    
            self.tablas.headerFichaClientes(3, self.tableWidget)
            self.tableWidget.setItem(fila, 4,QTableWidgetItem(str(data.getCliente())))    
            self.tablas.headerFichaClientes(4, self.tableWidget)
            self.tableWidget.setItem(fila, 5,QTableWidgetItem(str(data.getNombre())))    
            self.tablas.headerFichaClientes(5, self.tableWidget)
            self.tableWidget.setItem(fila, 6,QTableWidgetItem(str(data.getApellidos())))    
            self.tablas.headerFichaClientes(6, self.tableWidget)
            self.tableWidget.setItem(fila, 7,QTableWidgetItem(str(data.getActivo())))    
            self.tablas.headerFichaClientes(7, self.tableWidget)
            if data.getActivo() == 0 or int(data.getCliente()) !=  int(self.eclient.getIdCliente()):
                self.tableWidget.setRowHidden(fila, True)

    #obtener los nombres de los cargos para mostrarlos en la tabla
    def obtenerCargos(self, idcargo):
        mcargo = mCargo()
        cargo = mcargo.obtenerCargoEspecifico(idcargo)
        return cargo.getDescripcion()

    #verificar que los campos estan llenos para habilitar el boton de guardar
    def verificarCampos(self):
        if self.editCliente.text() != "" and self.editContrato.text() != "" and self.editDireccion.text() != "" and len(self.editCuenta.text()) == 16:
            self.actionSave.setEnabled(True)
        else:
            self.actionSave.setEnabled(False)

    #habilitando los botones de editar y eliminar
    def fichaClienteSeleccionada(self):
        self.actionDelete.setEnabled(True)
        self.actionEdit.setEnabled(True)

    #funcion para mofificar o guardar los clientes
    def guardarCliente(self):
        cliente = eCliente()
        cliente.setIdCliente(self.eclient.getIdCliente())
        cliente.setNombre(self.editCliente.text())
        cliente.setContrato(self.editContrato.text())
        cliente.setDireccion(self.editDireccion.text())
        cliente.setCuenta(self.editCuenta.text())
        cliente.setActivo(1)
        if self.eclient.getIdCliente() == "":
            self.mcliente.guardarDatosCliente(cliente)
        else:
            self.mcliente.editarDatosCliente(cliente,1)        
        listaCliente = self.mcliente.cargarDatosClientes()
        self.parent.llenadoTablaCliente(listaCliente)
        idcliente = listaCliente[-1].getIdCliente()
        self.eclient.setIdCliente(idcliente)
        self.actionAdd.setEnabled(True)
        self.actionSave.setEnabled(False)

    ###funcion para abrir la ventana de ficha cliente
    def nuevaFichaCliente(self):
        fcliente = eFichaCliente()
        fcliente.setCliente(self.eclient.getIdCliente())
        self.ventanaFichaCliente = QtWidgets.QDialog()
        self.ui = VentanaFichaCliente(fcliente, self)
        self.ui.setupUi(self.ventanaFichaCliente) 
        self.ventanaFichaCliente.exec()

    ###funcion para abrir la ventana de ficha cliente
    def editarFichaCliente(self):
        fila = self.tableWidget.currentRow()
        idfcliente = self.tableWidget.item(fila,0).text()
        fcliente = self.mfcliente.obtenerFichaClienteEspecifico(int(idfcliente))
        self.ventanaFichaCliente = QtWidgets.QDialog()
        self.ui = VentanaFichaCliente(fcliente, self)
        self.ui.setupUi(self.ventanaFichaCliente) 
        self.ventanaFichaCliente.exec()

    # eliminae ficha de cliente
    def eliminarFichaCliente(self):
        fila = self.tableWidget.currentRow()
        idfcliente = self.tableWidget.item(fila,0).text()
        fcliente = self.mfcliente.obtenerFichaClienteEspecifico(int(idfcliente))
        self.mfcliente.editarDatosFichaCliente(fcliente, 0)
        self.generales.eliminarFila(self.tableWidget)

     
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaCliente()
    ventana.show()
    sys.exit(app.exec())
