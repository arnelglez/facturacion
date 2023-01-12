import sys
from typing import List
from PyQt6.QtCore import QBuffer, QByteArray, QCoreApplication, QIODevice, QLibraryInfo, QLocale, QSize, QStringListModel, QTranslator
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QMessageBox, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Configuracion import *
from control.cliente import *
from control.unidadmedida import *
from control.reparacion import *
from control.servicio import *
from control.tipopago import *
from funciones.visuales import Tablas
from funciones.reportes import Reporte
from modelo.modTaller import mTaller, eTaller
from modelo.modDuenno import mDuenno, eDuenno
from modelo.modCliente import mCliente, eCliente
from modelo.modEquipo import mEquipo, eEquipo
from modelo.modUnidadMedida import mUnidadMedida, eUnidadMedida
from modelo.modServicio import mServicio, eServicio
from modelo.modTipoPago import mTipoPago, eTipoPago


class VentanaConfiguracion(QtWidgets.QMainWindow, Ui_ventanaConfiguracion):


    def __init__(self , parent = None):
        QtWidgets.QMainWindow.__init__(self)
        Ui_ventanaConfiguracion.__init__(self)
        self.mtaller = mTaller()
        self.duenno = mDuenno()
        self.mclient = mCliente()
        self.munidadmedida = mUnidadMedida()
        self.mequipo = mEquipo()
        self.mservicio = mServicio()
        self.mtpago = mTipoPago()
        self.idtaller = ''
        self.idduenno = ''
        self.tablas = Tablas()
        self.generales = FuncionesGenerales()
        self.lista = list()
        self.reporte = Reporte()
        self.setupUi(self)
        self.logo = ""
        self.tituloVentana = ""
        self.parent = parent

    
    def contexMenuCliente(self, pos):  
        self.seleccionCliente()
        menuTabla = QtWidgets.QMenu(self)
        menuTabla.addAction(self.actionAddCliente)
        menuTabla.addAction(self.actionDeleteCliente)
        menuTabla.addAction(self.actionActivarCliente)
        menuTabla.addAction(self.actionEditCliente)
        menuTabla.addAction(self.actionPrintCliente)
        menuTabla.addAction(self.actionVerCliente)
        menuTabla.exec(self.tableCliente.mapToGlobal(pos))
    
    def contexMenuUM(self, pos):   
        self.seleccionUnidadMedida()
        menuTabla = QtWidgets.QMenu(self)
        menuTabla.addAction(self.actionAddUM)
        menuTabla.addAction(self.actionDeleteUM)
        menuTabla.addAction(self.actionActivarUM)
        menuTabla.addAction(self.actionEditUM)
        menuTabla.addAction(self.actionPrintUM)
        menuTabla.addAction(self.actionVerUM)
        menuTabla.exec(self.tableUM.mapToGlobal(pos))

    def contexMenuReparacion(self, pos):   
        self.seleccionReparacion()
        menuTabla = QtWidgets.QMenu(self)
        menuTabla.addAction(self.actionAddReparacion)
        menuTabla.addAction(self.actionDeleteReparacion)
        menuTabla.addAction(self.actionActivarReparacion)
        menuTabla.addAction(self.actionEditReparacion)
        menuTabla.addAction(self.actionPrintReparacion)
        menuTabla.addAction(self.actionVerReparacion)
        menuTabla.exec(self.tableReparacion.mapToGlobal(pos))
    
    def contexMenuServicio(self, pos):   
        self.seleccionServicio()
        menuTabla = QtWidgets.QMenu(self)
        menuTabla.addAction(self.actionAddServicio)
        menuTabla.addAction(self.actionDeleteServicio)
        menuTabla.addAction(self.actionActivarServicio)
        menuTabla.addAction(self.actionEditServicio)
        menuTabla.addAction(self.actionPrintServicio)
        menuTabla.addAction(self.actionVerServicio)
        menuTabla.exec(self.tableServicio.mapToGlobal(pos))
    
    def contexMenuPago(self, pos):   
        self.seleccionTipoPago()
        menuTabla = QtWidgets.QMenu(self)
        menuTabla.addAction(self.actionAddPago)
        menuTabla.addAction(self.actionDeletePago)
        menuTabla.addAction(self.actionActivarPago)
        menuTabla.addAction(self.actionEditPago)
        menuTabla.addAction(self.actionPrintPago)
        menuTabla.addAction(self.actionVerPago)
        menuTabla.exec(self.tablePago.mapToGlobal(pos))
    
    
    #Inicializacion de la ventana
    def inicializacionVentana(self):
        self.inicializacionPestannaTaller()
        self.inicializacionPestannaDuenno()
        self.inicializacionPestannaCliente()
        self.inicializacionPestannaUM()
        self.inicializacionPestannaEquipo()
        self.inicializacionPestannaServicio()
        self.inicializacionPestannaTipoPago()

    #metodo para vista preliminar de las listas
    def vistaPrevia(self):
        self.reporte.listasConfiguraciones(self.lista[0], self.lista[1], self.lista[2], self)

    #metodo para recargar la tabla dependiendo de la pestaña
    def tabSeleccionado(self):
        if self.tabConfiguracion.currentIndex() == 0:
            self.inicializacionPestannaTaller()                       
        
        elif self.tabConfiguracion.currentIndex() == 1:
            self.inicializacionPestannaDuenno()
        
        elif self.tabConfiguracion.currentIndex() == 2:
            if self.actionVerCliente.isChecked():
                self.actionDeleteCliente.setVisible(False)
                self.actionActivarCliente.setVisible(True)
                self.actionVerCliente.setText('Mostrar Clientes Activos')
            else:
                self.actionDeleteCliente.setVisible(True)
                self.actionActivarCliente.setVisible(False)
                self.actionVerCliente.setText('Mostrar Clientes Inactivos')
            self.inicializacionPestannaCliente() 
            self.tituloVentana = 'Lista de Clientes'
       
        elif self.tabConfiguracion.currentIndex() == 3:
            if self.actionVerUM.isChecked():
                self.actionDeleteUM.setVisible(False)
                self.actionActivarUM.setVisible(True)
                self.actionVerCliente.setText('Mostrar Unidades de Medidas Activos')
            else:
                self.actionDeleteUM.setVisible(True)
                self.actionActivarUM.setVisible(False)
                self.actionVerCliente.setText('Mostrar Unidades de Medidas Inactivos')
            self.inicializacionPestannaUM() 
            self.tituloVentana = 'Lista de Unidades de Medida'
        
        elif self.tabConfiguracion.currentIndex() == 4:
            if self.actionVerReparacion.isChecked():
                self.actionDeleteReparacion.setVisible(False)
                self.actionActivarReparacion.setVisible(True)
                self.actionVerCliente.setText('Mostrar Equipos Activos')
            else:
                self.actionDeleteReparacion.setVisible(True)
                self.actionActivarReparacion.setVisible(False)
                self.actionVerCliente.setText('Mostrar Equipos Inactivos')
            self.inicializacionPestannaEquipo() 
            self.tituloVentana = 'Lista de Equipos'
        
        elif self.tabConfiguracion.currentIndex() == 5:
            if self.actionVerServicio.isChecked():
                self.actionDeleteServicio.setVisible(False)
                self.actionActivarServicio.setVisible(True)
                self.actionVerCliente.setText('Mostrar Servicios Activos')
            else:
                self.actionDeleteServicio.setVisible(True)
                self.actionActivarServicio.setVisible(False)
                self.actionVerCliente.setText('Mostrar Servicios Inactivos')
            self.inicializacionPestannaServicio() 
            self.tituloVentana = 'Lista de Servicios'
        
        elif self.tabConfiguracion.currentIndex() == 6:
            if self.actionVerPago.isChecked():
                self.actionDeletePago.setVisible(False)
                self.actionActivarPago.setVisible(True)
                self.actionVerCliente.setText('Mostrar Tipos de Pagos Activos')
            else:
                self.actionDeletePago.setVisible(True)
                self.actionActivarPago.setVisible(False)
                self.actionVerCliente.setText('Mostrar Tipos de Pagos Inactivos')
            self.inicializacionPestannaTipoPago() 
            self.tituloVentana = 'Lista de Formas de Pagos'

    #Inicializacion de la pestaña taller
    def inicializacionPestannaTaller(self):
        taller = self.mtaller.cargarValorTaller()
        self.idtaller = taller.getIdTaller()
        self.editNombre.setText(taller.getNombre())
        self.editDireccion.setText(taller.getDireccion())
        self.editCuenta.setText(taller.getCuenta())
        self.editCuentaMLC.setText(taller.getCuentaMLC())
        self.editSucursal.setText(taller.getSucursal())
        if taller.getLogo() != "../img/Taller.jpeg":
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(taller.getLogo(), 'png')
            self.logo = pixmap
        else: 
            self.logo = QtGui.QPixmap(self.generales.resource_path(taller.getLogo()))
        scaled = self.logo.scaled(200,200)
        self.labelLogo.setPixmap(scaled)
        
    #inicializamos la pestaña del dueno
    def inicializacionPestannaDuenno(self):
        dueno = self.duenno.cargarDatosDuenno()
        self.idduenno = dueno.getIdDuenno()
        self.editNombreDuenno.setText(dueno.getNombre())
        self.editApellidos.setText(dueno.getApellidos())
        self.editCarnet.setText(dueno.getCarnet())
        self.editTelefono.setText(dueno.getTelefono())
        self.editLicencia.setText(str(dueno.getLicencia())) 

    #inicializamos la pestaña de los cliente
    def inicializacionPestannaCliente(self):
        listaClientes = self.mclient.cargarDatosClientes()
        self.actionPrintCliente.setEnabled(False)
        if listaClientes.__len__() > 0:
            self.llenadoTablaCliente(listaClientes)
        self.actionDeleteCliente.setEnabled(False)
        self.actionActivarCliente.setEnabled(False)
        self.actionEditCliente.setEnabled(False)


    # llenamos la tabla perteneciente a la funcion anterior
    def llenadoTablaCliente(self, lista):  
        self.tableCliente.clear()
        self.tableCliente.setRowCount(0)
        clientes = ""
        for fila, data in enumerate(lista):
            self.tableCliente.insertRow(fila)   
            self.tableCliente.setItem(fila, 0,QTableWidgetItem(str(data.getIdCliente())))   
            self.tablas.headerClientes(0, self.tableCliente)
            self.tableCliente.setItem(fila, 1,QTableWidgetItem(data.getNombre()))    
            self.tablas.headerClientes(1, self.tableCliente)
            self.tableCliente.setItem(fila, 2,QTableWidgetItem(data.getContrato()))    
            self.tablas.headerClientes(2, self.tableCliente)
            self.tableCliente.setItem(fila, 3,QTableWidgetItem(data.getDireccion()))    
            self.tablas.headerClientes(3, self.tableCliente)
            self.tableCliente.setItem(fila, 4,QTableWidgetItem(data.getCuenta()))    
            self.tablas.headerClientes(4, self.tableCliente)
            self.tableCliente.setItem(fila, 5,QTableWidgetItem(str(data.getActivo())))    
            self.tablas.headerClientes(5, self.tableCliente)
            if self.actionVerCliente.isChecked() == data.getActivo():
                self.tableCliente.setRowHidden(fila, True)
            else:
                clientes += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(data.getNombre(), data.getContrato(), data.getDireccion(), data.getDireccion()) 

        if clientes != "":
            self.lista.clear()
            self.lista.append('lista_clientes.html')
            self.lista.append(clientes)
            self.lista.append('Lista de Clientes')
            self.actionPrintCliente.setEnabled(True)


    #inicializamos la tabla delas unidades de medida
    def inicializacionPestannaUM(self):
        listaUM = self.munidadmedida.cargarDatosUnidadMedida()
        self.actionPrintUM.setEnabled(False)
        if listaUM.__len__() > 0:
            self.llenadoTablaUnidadMedida(listaUM)
        self.actionDeleteUM.setEnabled(False)
        self.actionActivarUM.setEnabled(False)
        self.actionEditUM.setEnabled(False)

    # llenamos la tabla perteneciente a la funcion anterior
    def llenadoTablaUnidadMedida(self, lista):  
        self.tableUM.clear()
        self.tableUM.setRowCount(0)
        umedidas = ''
        for fila, data in enumerate(lista):
            self.tableUM.insertRow(fila)   
            self.tableUM.setItem(fila, 0,QTableWidgetItem(str(data.getIdUnidadMedida())))    
            self.tablas.headerUM(0, self.tableUM)
            self.tableUM.setItem(fila, 1,QTableWidgetItem(data.getDescripcion()))    
            self.tablas.headerUM(1, self.tableUM)
            self.tableUM.setItem(fila, 2,QTableWidgetItem(data.getSigla()))    
            self.tablas.headerUM(2, self.tableUM)
            self.tableUM.setItem(fila, 3,QTableWidgetItem(str(data.getActivo())))    
            self.tablas.headerUM(3, self.tableUM)
            if self.actionVerUM.isChecked() == data.getActivo():
                self.tableUM.setRowHidden(fila, True)
            else:
                umedidas += "<tr><td>{}</td><td>{}</td></tr>".format(data.getDescripcion(), data.getSigla()) 

        if umedidas != "":
            self.lista.clear()
            self.lista.append('lista_umedidas.html')
            self.lista.append(umedidas)
            self.lista.append('Lista de Unidades de Medidas')
            self.actionPrintUM.setEnabled(True)

    
    #inicializamos la pestaña de los tipos de equipos
    def inicializacionPestannaEquipo(self):
        listaReparacion = self.mequipo.cargarDatosEquipo()
        self.actionPrintReparacion.setEnabled(False)
        if listaReparacion.__len__() > 0:
            self.llenadoTablaEquipo(listaReparacion)
        self.actionDeleteReparacion.setEnabled(False)
        self.actionActivarReparacion.setEnabled(False)
        self.actionEditReparacion.setEnabled(False)

    # llenamos la tabla perteneciente a la funcion anterior
    def llenadoTablaEquipo(self, lista):    
        self.tableReparacion.clear()
        self.tableReparacion.setRowCount(0)
        equipos = ""
        for fila, data in enumerate(lista):
            self.tableReparacion.insertRow(fila)   
            self.tableReparacion.setItem(fila, 0,QTableWidgetItem(str(data.getIdEquipo())))    
            self.tablas.headerEquipos(0, self.tableReparacion)

            item = QTableWidgetItem()
            if data.getMultiple() == 1:
                imagen = "../img/check.png"
            else:
                imagen = "../img/nocheck.png"
        
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(self.generales.resource_path(imagen)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            item.setIcon(icon)
            item.setText(str(data.getDescripcion()))
                            
            self.tableReparacion.setItem(fila, 1,item)    
            self.tablas.headerEquipos(1, self.tableReparacion)
            self.tableReparacion.setItem(fila, 2,QTableWidgetItem(data.getDescripcion()))  
            self.tablas.headerEquipos(2, self.tableReparacion)
            self.tableReparacion.setItem(fila, 3,QTableWidgetItem(str(data.getActivo())))    
            self.tablas.headerEquipos(3, self.tableReparacion)
            if self.actionVerReparacion.isChecked() == data.getActivo():
                self.tableReparacion.setRowHidden(fila, True)
            else:
                equipos += "<tr><td>{}</td></tr>".format(data.getDescripcion()) 

        if equipos != "":
            self.lista.clear()
            self.lista.append('lista_equipos.html')
            self.lista.append(equipos)
            self.lista.append('Lista de Equipos')
            self.actionPrintReparacion.setEnabled(True)
    
    #inicializamos la pestaña de los servicios
    def inicializacionPestannaServicio(self):
        listaServicio = self.mservicio.cargarDatosServicio()
        self.actionPrintServicio.setEnabled(False)
        if listaServicio.__len__() > 0:
            self.llenadoTablaServicio(listaServicio)
        self.actionDeleteServicio.setEnabled(False)
        self.actionActivarServicio.setEnabled(False)
        self.actionEditServicio.setEnabled(False)
    
    # llenamos la tabla perteneciente a la funcion anterior
    def llenadoTablaServicio(self, lista):      
        self.tableServicio.clear()
        self.tableServicio.setRowCount(0)
        servicios = ""
        for fila, data in enumerate(lista):
            self.tableServicio.insertRow(fila)   
            self.tableServicio.setItem(fila, 0,QTableWidgetItem(str(data.getIdServicio())))    
            self.tablas.headerServicio(0, self.tableServicio)

            equipo = data.getEquipo()
            desc =  data.getDescripcion()
            tipo =  self.mequipo.obtenerEquipoEspecifico(equipo)
            descripcion = desc + ' ' + tipo.getDescripcion()

            self.tableServicio.setItem(fila, 1,QTableWidgetItem(descripcion))    
            self.tablas.headerServicio(1, self.tableServicio)

            umedida = self.generales.optenerUnidadMedidad(data.getUnidadMedida())
            precio = round(data.getPrecio(), 2)

            self.tableServicio.setItem(fila, 2,QTableWidgetItem(umedida.getSigla()))    
            self.tablas.headerServicio(2, self.tableServicio)
            self.tableServicio.setItem(fila, 3,QTableWidgetItem(self.generales.floatToStr(precio)))  
            self.tablas.headerServicio(3, self.tableServicio)
            self.tableServicio.setItem(fila, 4,QTableWidgetItem(str(data.getActivo())))  
            self.tablas.headerServicio(4, self.tableServicio)
            self.tableServicio.setItem(fila, 5,QTableWidgetItem(data.getDescripcion()))  
            self.tablas.headerServicio(5, self.tableServicio)
            self.tableServicio.setItem(fila, 6,QTableWidgetItem(str(data.getEquipo())))  
            self.tablas.headerServicio(6, self.tableServicio)
            if self.actionVerServicio.isChecked() == data.getActivo():
                self.tableServicio.setRowHidden(fila, True)
            else:
                servicios += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(descripcion, umedida.getSigla(), precio) 
 
        if servicios != "":
            self.lista.clear()
            self.lista.append('lista_servicios.html')
            self.lista.append(servicios)
            self.lista.append('Lista de Servicios')
            self.actionPrintServicio.setEnabled(True)
    
    #inicializamos la pestaña de los tipos de pago
    def inicializacionPestannaTipoPago(self):
        listaTpoPago = self.mtpago.cargarDatosTipoPago()
        self.actionPrintPago.setEnabled(False)
        if listaTpoPago.__len__() > 0:
            self.llenadoTablaTipoPago(listaTpoPago)
        self.actionDeletePago.setEnabled(False)
        self.actionActivarPago.setEnabled(False)
        self.actionEditPago.setEnabled(False)

    # llenamos la tabla perteneciente a la funcion anterior
    def llenadoTablaTipoPago(self, lista):                            
        self.tablePago.clear()
        self.tablePago.setRowCount(0)
        tpagos = ""
        for fila, data in enumerate(lista):
            self.tablePago.insertRow(fila)   
            self.tablePago.setItem(fila, 0,QTableWidgetItem(str(data.getIdTipoPago())))    
            self.tablas.headerDosColumnas(0, self.tablePago)
            self.tablePago.setItem(fila, 1,QTableWidgetItem(data.getDescripcion()))    
            self.tablas.headerDosColumnas(1, self.tablePago)
            self.tablePago.setItem(fila, 2,QTableWidgetItem(str(data.getActivo())))    
            self.tablas.headerDosColumnas(2, self.tablePago)
            if self.actionVerPago.isChecked() == data.getActivo():
                self.tablePago.setRowHidden(fila, True)
            else:
                tpagos += "<tr><td>{}</td></tr>".format(data.getDescripcion()) 

        if tpagos != "":
            self.lista.clear()
            self.lista.append('lista_tpagos.html')
            self.lista.append(tpagos)
            self.lista.append('Lista de Formas de Pago')
            self.actionPrintPago.setEnabled(True)



    ##### funcion para obtener el logo
    def cargarLogo(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '', 'Imagenes (*.png *.jpg *.jepg *.bmp)')
        if path != ('', ''):
            imagen = QtGui.QPixmap(path[0])
            scaled = imagen.scaled(200,200)
            self.labelLogo.setPixmap(scaled)
            
    # verificar campos para guardar taller
    def verificarCamposTaller(self):
        if self.editNombre.text() != "" and self.editDireccion.text() != "" and len(self.editCuenta.text()) == 16 and len(self.editCuentaMLC.text()) == 16 and self.editSucursal.text() != "" and len(self.editSucursal.text()) == 4:
            self.buttonGuardarTaller.setEnabled(True)
        else:
            self.buttonGuardarTaller.setEnabled(False)



    # Guardar datos de pestaña Taller
    def guardarDatosTaller(self):
        taller = eTaller()
        taller.setIdTaller(self.idtaller)
        taller.setNombre(self.editNombre.text())
        taller.setDireccion(self.editDireccion.text())
        taller.setCuenta(self.editCuenta.text())
        taller.setCuentaMLC(self.editCuentaMLC.text())
        taller.setSucursal(self.editSucursal.text())
        logo = self.conversionImagen()
        taller.setLogo(logo)
        taller.setLicencia("")
        self.mtaller.guardarDatosTaller(taller)
        # muestro los datos nuevos ne la pantalla inicial
        self.parent.presentacionVentana()
        self.buttonGuardarTaller.setEnabled(False)

    def conversionImagen(self):
        foto = self.labelLogo.pixmap()
        if foto:
            bArray = QByteArray()
            bufer = QBuffer(bArray)
            bufer.open(QIODevice.OpenModeFlag.WriteOnly)
            bufer.close()
            foto.save(bufer, 'PNG')
        else:
            bArray = ""

        return bArray

    def verificarCamposDuenno(self):
        if self.editNombreDuenno.text() == "" or self.editApellidos.text()  == "" or self.editCarnet.text()  == "" or self.editLicencia.text() == "" or self.editTelefono.text() == "" or len(self.editTelefono.text()) < 8:
            self.buttonGuardarDuenno.setEnabled(False)
        else:
            self.buttonGuardarDuenno.setEnabled(True)
            

    def guardarDatosDuenno(self):
        dueno = eDuenno()
        dueno.setIdDuenno(self.idduenno)
        dueno.setNombre(self.editNombreDuenno.text())
        dueno.setApellidos(self.editApellidos.text())
        dueno.setCarnet(self.editCarnet.text())
        dueno.setTelefono(self.editTelefono.text())
        dueno.setLicencia(self.editLicencia.text())
        self.duenno.guardarDatosDuenno(dueno)
        self.buttonGuardarDuenno.setEnabled(False)

    ###funcion para abrir la ventana de nuevo cliente
    def nuevoCliente(self):
        eclient = eCliente()
        self.ventanaCliente = QtWidgets.QDialog()
        self.ui = VentanaCliente(eclient,self)
        self.ui.setupUi(self.ventanaCliente) 
        self.ventanaCliente.exec()

    # Habilitar boton de eliminar y modificar
    def seleccionCliente(self):
        fila = self.tableCliente.currentRow()
        if fila != -1:
            if int(self.tableCliente.item(fila, 5).text()) == 1:
                self.actionDeleteCliente.setEnabled(True)
                self.actionActivarCliente.setEnabled(False)
                self.actionEditCliente.setEnabled(True)
            else:
                self.actionDeleteCliente.setEnabled(False)
                self.actionActivarCliente.setEnabled(True)

    # funcion para editar el cliente
    def editarCliente(self):
        fila = self.tableCliente.currentRow()
        idcliente = self.tableCliente.item(fila,0).text()
        eclient = self.mclient.obtenerDatosClientesEspecifica(int(idcliente))
        self.ventanaCliente = QtWidgets.QDialog()
        self.ui = VentanaCliente(eclient, self)
        self.ui.setupUi(self.ventanaCliente) 
        self.ventanaCliente.exec()

    #Activar Cliente
    def activarCliente(self):
        fila = self.tableCliente.currentRow()
        idcliente = self.tableCliente.item(fila,0).text()
        eclient = self.mclient.obtenerDatosClientesEspecifica(int(idcliente))
        resp = self.generales.mensageSiNo("Activar Cliente", "El cliente {} va a ser activado en la base de datos!".format(eclient.getNombre()),
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mclient.editarDatosCliente(eclient, 1)
            self.generales.eliminarFila(self.tableCliente)

    #Eliminar Cliente
    def eliminarCliente(self):
        fila = self.tableCliente.currentRow()
        idcliente = self.tableCliente.item(fila,0).text()
        eclient = self.mclient.obtenerDatosClientesEspecifica(int(idcliente))
        resp = self.generales.mensageSiNo("Eliminar Cliente", "El cliente {} va a ser eliminado de la base de datos!".format(eclient.getNombre()),
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mclient.editarDatosCliente(eclient, 0)
            self.generales.eliminarFila(self.tableCliente)


    ###funcion para abrir la ventana unidad de medida
    def nuevoUnidadMedida(self):
        eumedida = eUnidadMedida()
        self.ventanaUnidadMedida = QtWidgets.QDialog()
        self.ui = VentanaUnidadMedida(eumedida, self)
        self.ui.setupUi(self.ventanaUnidadMedida) 
        self.ventanaUnidadMedida.exec()

    # Habilitar boton de eliminar y modificar
    def seleccionUnidadMedida(self):
        fila = self.tableUM.currentRow()
        if fila != -1:
            if int(self.tableUM.item(fila, 3).text()) == 1:
                self.actionDeleteUM.setEnabled(True)    
                self.actionEditUM.setEnabled(True)
                self.actionActivarUM.setEnabled(False)
            else:
                self.actionDeleteUM.setEnabled(False)
                self.actionActivarUM.setEnabled(True)

    # funcion para editar Unidad de Medida
    def editarUnidadMedida(self):
        fila = self.tableUM.currentRow()
        idum = self.tableUM.item(fila,0).text()
        eumedida = self.munidadmedida.obtenerUnaUnidadMedidaEspecifica(int(idum))
        self.ventanaUnidadMedida = QtWidgets.QDialog()
        self.ui = VentanaUnidadMedida(eumedida, self)
        self.ui.setupUi(self.ventanaUnidadMedida) 
        self.ventanaUnidadMedida.exec()

    #Activar Unidad de Medida
    def activarUnidadMedida(self):
        fila = self.tableUM.currentRow()
        idum = self.tableUM.item(fila,0).text()
        eumedida = self.munidadmedida.obtenerUnaUnidadMedidaEspecifica(int(idum))
        resp = self.generales.mensageSiNo("Activar Unidad de Medida", "La unidad de medida ({}) va a ser activada en la base de datos!".format(eumedida.getDescripcion()),
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.munidadmedida.editarDatosUnidadMedida(eumedida, 1)
            self.generales.eliminarFila(self.tableUM)

    #Eliminar Unidad de Medida
    def eliminarUnidadMedida(self):
        fila = self.tableUM.currentRow()
        idum = self.tableUM.item(fila,0).text()
        eumedida = self.munidadmedida.obtenerUnaUnidadMedidaEspecifica(int(idum))
        resp = self.generales.mensageSiNo("Eliminar Unidad de Medida", "La unidad de medida ({}) va a ser eliminado de la base de datos!".format(eumedida.getDescripcion()),
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.munidadmedida.editarDatosUnidadMedida(eumedida, 0)
            self.generales.eliminarFila(self.tableUM)

    ### funcion para abrir la ventana de reparaciones
    def nuevaReparacion(self):
        equipo = eEquipo()
        self.ventanaReparacion = QtWidgets.QDialog()
        self.ui = VentanaReparacion(equipo, self)
        self.ui.setupUi(self.ventanaReparacion) 
        self.ventanaReparacion.exec()

    # Habilitar boton de eliminar y modificar
    def seleccionReparacion(self):
        fila = self.tableReparacion.currentRow()
        if fila != -1:
            if int(self.tableReparacion.item(fila, 3).text()) == 1:
                self.actionDeleteReparacion.setEnabled(True)    
                self.actionEditReparacion.setEnabled(True)
                self.actionActivarReparacion.setEnabled(False)
            else:
                self.actionDeleteReparacion.setEnabled(False)
                self.actionActivarReparacion.setEnabled(True)

    # funcion para editar Tipo de Equipo
    def editarReparacion(self):
        fila = self.tableReparacion.currentRow()
        idequipo = self.tableReparacion.item(fila,0).text()
        equipo = self.mequipo.obtenerEquipoEspecifico(int(idequipo))
        self.ventanaReparacion = QtWidgets.QDialog()
        self.ui = VentanaReparacion(equipo, self)
        self.ui.setupUi(self.ventanaReparacion) 
        self.ventanaReparacion.exec()

    #Activar Tipo de Equipo
    def activarReparacion(self):
        fila = self.tableReparacion.currentRow()
        idequipo = self.tableReparacion.item(fila,0).text()
        equipo = self.mequipo.obtenerEquipoEspecifico(idequipo)
        resp = self.generales.mensageSiNo("Activar Equipo", "El equipo ({}) va a ser activado en la base de datos!".format(equipo.getDescripcion()),
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mequipo.editarDatosEquipo(equipo, 1)
            self.generales.eliminarFila(self.tableReparacion)

    #Eliminar Tipo de Equipo
    def eliminarReparacion(self):
        fila = self.tableReparacion.currentRow()
        idequipo = self.tableReparacion.item(fila,0).text()
        equipo = self.mequipo.obtenerEquipoEspecifico(idequipo)
        resp = self.generales.mensageSiNo("Eliminar Equipo", "El equipo ({}) va a ser eliminado de la base de datos!".format(equipo.getDescripcion()),
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mequipo.editarDatosEquipo(equipo, 0)
            self.generales.eliminarFila(self.tableReparacion)
    
    ### funcion para abrir la ventana de servicio
    def nuevoServicio(self):
        eservicio = eServicio()
        self.ventanaServicio = QtWidgets.QDialog()
        self.ui = VentanaServicio(eservicio, self)
        self.ui.setupUi(self.ventanaServicio) 
        self.ventanaServicio.exec()

    # Habilitar boton de eliminar y modificar
    def seleccionServicio(self):
        fila = self.tableServicio.currentRow()
        if fila != -1:
            if int(self.tableServicio.item(fila, 4).text()) == 1:
                self.actionDeleteServicio.setEnabled(True)    
                self.actionEditServicio.setEnabled(True)
                self.actionActivarServicio.setEnabled(False)
            else:
                self.actionDeleteServicio.setEnabled(False)
                self.actionActivarServicio.setEnabled(True)

    # funcion para editar Servicio
    def editarServicio(self):
        fila = self.tableServicio.currentRow()
        idservicio = self.tableServicio.item(fila, 0).text()
        eservicio = self.mservicio.obtenerServicioEspecifico(idservicio)
        self.ventanaServicio = QtWidgets.QDialog()
        self.ui = VentanaServicio(eservicio, self)
        self.ui.setupUi(self.ventanaServicio) 
        self.ventanaServicio.exec()

    #Activar Servicio
    def activarServicio(self):
        fila = self.tableServicio.currentRow()
        idservicio = self.tableServicio.item(fila, 0).text()
        eservicio = self.mservicio.obtenerServicioEspecifico(idservicio)
        tipo =  self.mequipo.obtenerEquipoEspecifico(eservicio.getEquipo())
        resp = self.generales.mensageSiNo("Activar Servicio", "El servicio {}  {} va a ser activado en la base de datos!".format(eservicio.getDescripcion(), tipo.getDescripcion()),
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mservicio.editarDatosServicio(eservicio, 1)
            self.generales.eliminarFila(self.tableServicio)

    #Eliminar Servicio
    def eliminarServicio(self):
        fila = self.tableServicio.currentRow()
        idservicio = self.tableServicio.item(fila, 0).text()
        eservicio = self.mservicio.obtenerServicioEspecifico(idservicio)
        tipo =  self.mequipo.obtenerEquipoEspecifico(eservicio.getEquipo())
        resp = self.generales.mensageSiNo("Eliminar Servicio", "El servicio {}  {} va a ser eliminado de la base de datos!".format(eservicio.getDescripcion(), tipo.getDescripcion()),
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mservicio.editarDatosServicio(eservicio, 0)
            self.generales.eliminarFila(self.tableServicio)
    

    ### funcion para abrir la ventana de tipo de pagos
    def nuevoTipoPago(self):
        etpago = eTipoPago()
        self.ventanaTipoPago = QtWidgets.QDialog()
        self.ui = VentanaTipoPago(etpago, self)
        self.ui.setupUi(self.ventanaTipoPago) 
        self.ventanaTipoPago.exec()

    # Habilitar boton de eliminar y modificar
    def seleccionTipoPago(self):
        fila = self.tablePago.currentRow()
        if fila != -1:
            if int(self.tablePago.item(fila, 2).text()) == 1:
                self.actionDeletePago.setEnabled(True)    
                self.actionEditPago.setEnabled(True)
                self.actionActivarPago.setEnabled(False)
            else:
                self.actionDeletePago.setEnabled(False)
                self.actionActivarPago.setEnabled(True)

    # funcion para editar Tipo de Pago
    def editarTipoPago(self):
        fila = self.tablePago.currentRow()
        idttpago = self.tablePago.item(fila,0).text()
        etpago = self.mtpago.obtenerTipoPagoEspecifico(int(idttpago))
        self.ventanaTipoPago = QtWidgets.QDialog()
        self.ui = VentanaTipoPago(etpago, self)
        self.ui.setupUi(self.ventanaTipoPago) 
        self.ventanaTipoPago.exec()

    #Activar Tipo de Pago
    def activarTipoPago(self):
        fila = self.tablePago.currentRow()
        idttpago = self.tablePago.item(fila,0).text()
        etpago = self.mtpago.obtenerTipoPagoEspecifico(int(idttpago))
        resp = self.generales.mensageSiNo("Activar Forma de Pago", "La forma de pago {} va a ser activado en la base de datos!".format(etpago.getDescripcion()),
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mtpago.editarDatosTipoPago(etpago, 1)
            self.generales.eliminarFila(self.tablePago)


    #Eliminar Tipo de Pago
    def eliminarTipoPago(self):
        fila = self.tablePago.currentRow()
        idttpago = self.tablePago.item(fila,0).text()
        etpago = self.mtpago.obtenerTipoPagoEspecifico(int(idttpago))
        resp = self.generales.mensageSiNo("Eliminar Forma de Pago", "La forma de pago {} va a ser eliminado de la base de datos!".format(etpago.getDescripcion()),
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mtpago.editarDatosTipoPago(etpago, 0)
            self.generales.eliminarFila(self.tablePago)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    locale = QLocale.system().name()
    qtTanslator = QTranslator()
    if qtTanslator.load("tq_" + locale):
        app.installTranslator(qtTanslator)

    ventana = VentanaConfiguracion()
    ventana.show()
    sys.exit(app.exec())
