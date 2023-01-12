import sys
from typing import List
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from modelo.modRecepcion import mRecepcion
from vista.consultas.Ui_CargarInventario import *
from modelo.modCliente import mCliente
from modelo.modEquipo import mEquipo
from modelo.modMarca import mMarca
from modelo.modModelo import mModelo
from modelo.modInventario import mInventario
from funciones.generales import FuncionesGenerales
from funciones.reportes import Reporte


class VentanaCargarInventario(QtWidgets.QMainWindow, Ui_VentanaCargarInventario):

    def __init__(self):

        self.generales = FuncionesGenerales()
        self.mcliente = mCliente()
        self.mequipo = mEquipo()
        self.mmarca = mMarca()
        self.mmodelo = mModelo()

        self.clientes = list()
        self.equipos = list()
        self.modelos = list()
        self.marcas = list()
        self.reportes = Reporte()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaCargarInventario.__init__(self)
        self.setupUi(self)

    # inicializo la ventaa cargando todos los valores en todos los combos
    def inicializarVentana(self):
        self.llenarComboClientes()
        self.llenarComboEquipos()
        self.llenarComboMarca('*')
        self.llenarComboModelo('*', '*')
        
    # llenado del combo cliente 
    def llenarComboClientes(self):
        self.clientes.clear()
        self.comboCliente.addItem('                        ---   TODOS   --- ')
        for cliente in self.mcliente.cargarDatosClientes():
            if cliente.getActivo() == 1:
                self.clientes.append(cliente)
                self.comboCliente.addItem(str(cliente.getIdCliente()) + ' - ' + cliente.getNombre())

    # funcion para obtener los datos del nombre que coincida con el combo
    def busquedaPorDescripcion(self, lista, parametro):
        for data in lista:
            if data.getDescripcion() == parametro:
                return data

    #funcion para obtener el id del equipo seleccionado en el combo
    def seleccionEquipo(self):
        if self.comboEquipo.currentIndex() < 1:
            equipo = '*'
        else:
            equipo = self.busquedaPorDescripcion(self.equipos, self.comboEquipo.currentText())
            equipo = equipo.getIdEquipo()

        return equipo

    #funcion para obtener el id de la marca seleccionado en el combo
    def seleccionMarca(self):
        if self.comboMarca.currentIndex() < 1:
            marca = '*'
        else:
            marca = self.busquedaPorDescripcion(self.marcas, self.comboMarca.currentText())
            marca = marca.getIdMarca()

        return marca

    # funcion para filtrar los modelos y marcas dependiendo de los equipos 
    def equipoSeleccionado(self):
        equipo = self.seleccionEquipo()
        marca = self.seleccionMarca()
        self.llenarComboMarca(equipo)
        self.llenarComboModelo(equipo, marca)

    # funcion para filtrar las marcas dependiendo de los modelos selecciones 
    def marcaSeleccionada(self):
        equipo = self.seleccionEquipo()
        marca = self.seleccionMarca()
        self.llenarComboModelo(equipo, marca)

    # funcion para llenar el combo de los equipos
    def llenarComboEquipos(self):
        self.comboEquipo.clear()
        self.equipos.clear()
        self.comboEquipo.addItem('                        ---   TODOS   --- ')
        for equipo in self.mequipo.cargarDatosEquipo():
            if equipo.getActivo() == 1:
                self.equipos.append(equipo)
                self.comboEquipo.addItem(equipo.getDescripcion())

    # funcion para llenar las marcas
    def llenarComboMarca(self, equipo):
        self.comboMarca.clear()
        self.marcas.clear()        
        self.comboMarca.addItem('                        ---   TODOS   --- ')
        for marca in self.mmarca.cargarDatosMarca():
            if marca.getEquipo() == equipo or equipo == '*': 
                self.marcas.append(marca)
                self.comboMarca.addItem(marca.getDescripcion())

    # funcion para llear el combo de los modelos
    def llenarComboModelo(self, equipo, marca):
        self.comboModelo.clear()
        self.modelos.clear()
        self.comboModelo.addItem('                        ---   TODOS   --- ')
        for modelo in self.mmodelo.cargarDatosModelo():
            if (modelo.getEquipo() == equipo or equipo == '*') and (modelo.getMarca() == marca or marca == '*'): 
                self.modelos.append(modelo)
                self.comboModelo.addItem(modelo.getDescripcion())

    def imprimirInventario(self):
        clienteSeleccion = self.comboCliente.currentIndex() -1
        equipoSeleccion = self.comboEquipo.currentIndex() - 1
        marcaSeleccion = self.comboMarca.currentIndex() - 1
        modeloSeleccion = self.comboModelo.currentIndex() -1
            
        if equipoSeleccion >= 0:
            equipo = self.equipos[equipoSeleccion].getIdEquipo()
        else:
            equipo = '*'
            
        if marcaSeleccion >= 0:
            marca = self.marcas[marcaSeleccion].getIdMarca()
        else:
            marca = '*'
            
        if modeloSeleccion >= 0:
            modelo = self.modelos[modeloSeleccion].getIdModelo()
        else:
            modelo = '*'
            
        
        inventarios = mInventario().busquedaListaInventarios(equipo, marca, modelo)
        data = ''
        
        if clienteSeleccion >= 0:    
            if inventarios:                    
                for inv in inventarios:
                    invRecepcion = mRecepcion().obtenerRecepcionEspecifico(inv.getRecepcion())
                    invEquipo = mEquipo().obtenerEquipoEspecifico(inv.getEquipo()).getDescripcion()
                    invMarca = mMarca().obtenerMarcaEspecifico(inv.getMarca()).getDescripcion()
                    invModelo = mModelo().obtenerModeloEspecifico(inv.getModelo()).getDescripcion()
                    
                    if invRecepcion.getEstado() == 2:
                        if invRecepcion.getCliente() == self.clientes[clienteSeleccion].getIdCliente():
                            data += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(inv.getNoInventario(), invEquipo, invMarca, invModelo, inv.getActivo()) 
                    
            self.reportes.listasConfiguraciones('lista_inventario.html', data , 'Inventarios ' +  self.clientes[clienteSeleccion].getNombre() , self)

        else:         
            if inventarios:   
                for cliente in self.clientes:    
                    clienteUsado = False               
                    for inv in inventarios:
                        invRecepcion = mRecepcion().obtenerRecepcionEspecifico(inv.getRecepcion())
                        invEquipo = mEquipo().obtenerEquipoEspecifico(inv.getEquipo()).getDescripcion()
                        invMarca = mMarca().obtenerMarcaEspecifico(inv.getMarca()).getDescripcion()
                        invModelo = mModelo().obtenerModeloEspecifico(inv.getModelo()).getDescripcion()
                        
                        if invRecepcion.getEstado() == 2:
                            if cliente.getIdCliente() == invRecepcion.getCliente(): 
                                if clienteUsado == False:
                                    data += "<tr><td colspan='5'><b>Cliente:    </b>{}</td></tr>".format(cliente.getNombre())
                                    clienteUsado = True
                                    
                                data += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(inv.getNoInventario(), invEquipo, invMarca, invModelo, inv.getActivo()) 
            
              
            self.reportes.listasConfiguraciones('lista_inventario.html', data , 'Inventarios' , self)

    # cerrar la ventana
    def cerrarVentana(self, ventana):
        self.generales.cerrarVentana(ventana)
  
     
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaCargarInventario()
    ventana.show()
    sys.exit(app.exec())
