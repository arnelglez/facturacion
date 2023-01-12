
from statistics import mode
import sys
import datetime
import io
import os
from datetime import date
from PyQt6.QtCore import QSaveFile
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon
from unidecode import unidecode
import ntpath

from PyQt6.QtWidgets import QDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Principal import *
from control.configuracion import *
from control.administracionusuario import *
from control.recepcion import *
from control.factura import *
from control.cobro import *
from control.rangofechas import *
from control.anticipo import *
from control.devolucion import *
from control.acerca import *
from control.fecha import *
from control.consultas.cargarinventario import *
from control.consultas.cargarfacturacobro import *
from modelo.modTaller import mTaller, eTaller
from modelo.modDuenno import mDuenno, eDuenno
from modelo.modRecepcion import mRecepcion, eRecepcion
from modelo.modFactura import mFactura, eFactura
from modelo.modCobro import mCobro, eCobro
from modelo.modUsuario import mUsuario, eUsuario
from modelo.modCliente import mCliente, eCliente
from modelo.modInventario import mInventario, eInventario
from modelo.modCobroFactura import mCobroFactura, eCobroFactura
from modelo.modAnticipo import mAnticipo, eAnticipo
from modelo.modTipoPago import mTipoPago, eTipoPago
from funciones.generales import FuncionesGenerales, Criptografia
from funciones.visuales import Tablas
from funciones.reportes import Reporte
from funciones.tallerDB import BaseTaller

class VentanaPrincipal(QtWidgets.QMainWindow, Ui_MainWindow):


    def __init__(self, usuario:eUsuario):
        QtWidgets.QMainWindow.__init__(self)

        self.mrececpcion = mRecepcion()
        self.musuario = mUsuario()
        self.mcliente = mCliente()
        self.mcargo = mCargo()
        self.mfichaClinete = mFichaCliente()
        self.mumedida = mUnidadMedida() 
        self.mequipo = mEquipo()
        self.mservicio = mServicio()
        self.mtipoPago = mTipoPago()
        self.minventario = mInventario()
        self.mfactura = mFactura()
        self.mcobro = mCobro()
        self.mfacturadesglose = mFacturaDesglose()
        self.mcobrofactura = mCobroFactura()
        self.manticipo = mAnticipo()
        self.mtaller = mTaller()
        self.mduenno = mDuenno()
        self.generales = FuncionesGenerales()
        self.cripto = Criptografia()
        self.tablas = Tablas()
        self.usuario = usuario
        self.reporte = Reporte()
        self.baseTaller = BaseTaller()

        self.confAtiva = ""
        self.fecha_inicio = ""
        self.fecha_fin = ""

        Ui_MainWindow.__init__(self)
        self.setupUi(self)

    #menu clic derecho en la tabla
    def contexMenuEvent(self, pos):   
        self.filaSeleccionada()
        menuTabla = QtWidgets.QMenu(self)
        menuTabla.addAction(self.actionNueva)
        menuTabla.addAction(self.actionAbrir)
        menuTabla.addAction(self.actionConfirmar)
        menuTabla.addAction(self.actionEliminar)
        menuTabla.addAction(self.actionCancelar)
        menuTabla.addAction(self.actionImprimir)
        menuTabla.addAction(self.actionMostrar)
        menuTabla.addAction(self.actionOcultar)
        menuTabla.addAction(self.actionConformidad)

        menuTabla.exec(self.tableWidget.mapToGlobal(pos))


    def verificarLicencia(self):
        taller = self.mtaller.cargarValorTaller()
        duenno = self.mduenno.cargarDatosDuenno()
        if taller.getLicencia() != "" and self.generales.verificarLicencia(taller, duenno, taller.getLicencia()):
            self.menuLicencia.setEnabled(False)
            self.menu_Consultas.setEnabled(True)
            return True
        elif taller.getLicencia() != "" and self.generales.verificarLicencia(taller, duenno, taller.getLicencia()) == False:
            taller.setLicencia('')
            self.menuLicencia.setEnabled(True)
            self.menu_Consultas.setEnabled(False)
            return False
        else:
            self.menuLicencia.setEnabled(True)
            self.menu_Consultas.setEnabled(False)
            return False

    #configuracion 0 por defecto muestro imagen y nombre
    #configuracion 1 menu y tabla para factura
    #configuracion 2 menu y tabla para recepcion
    #configuracion 3 menu y tabla para cobros
    def configuracionVentana(self, configuracion):   
        self.presentacionVentana()
        self.configuracionBotonesMenu(configuracion)
        self.permisosUsuarios()
        self.progressBar.setVisible(False)
        if configuracion == 0:
            self.labelImagen.setVisible(True)
            self.labelTaller.setVisible(True)
            self.toolBar_3.setVisible(False)
            self.tableWidget.setVisible(False)
        else:
            self.labelImagen.setVisible(False)
            self.labelTaller.setVisible(False)
            self.toolBar_3.setVisible(True)
            self.tableWidget.setVisible(True)

    def permisosUsuarios(self):         
        clientes = self.mcliente.cargarDatosClientes()
        cargos = self.mcargo.cargarDatosCargo()
        fichaCliente = self.mfichaClinete.cargarDatosFichaCliente()
        umedida = self.mumedida.cargarDatosUnidadMedida()
        equipos = self.mequipo.cargarDatosEquipo()
        servicios = self.mservicio.cargarDatosServicio()
        pagos = self.mtipoPago.cargarDatosTipoPago()
        
        if self.generales.fechaDocumentos() == '//':
            self.actionRecepcion.setEnabled(False)
            self.actionPago.setEnabled(False)
            self.actionFactura.setEnabled(False) 
            self.actionAnticipos.setEnabled(False)
            self.menu_Operaciones.setEnabled(False)
            self.actioncambioFecha.setEnabled(True)
            if clientes.__len__() == 0 and fichaCliente.__len__() == 0 and servicios.__len__()  == 0 and  umedida.__len__() == 0 and cargos.__len__() == 4 and equipos.__len__() == 9 and pagos.__len__() == 3:
                self.actionImportar.setVisible(True)
                self.actionExportar.setEnabled(False)
            else:
                self.actionImportar.setEnabled(False)
                self.actionExportar.setVisible(True)
            
        elif self.usuario.getIdUsuario() == 1:
            self.actionRecepcion.setEnabled(False)
            self.actionPago.setEnabled(False)
            self.actionFactura.setEnabled(False) 
            self.actionAnticipos.setEnabled(False)
            self.menu_Operaciones.setEnabled(False)
            self.actioncambioFecha.setEnabled(False)
            if clientes.__len__() == 0 and fichaCliente.__len__() == 0 and servicios.__len__()  == 0 and  umedida.__len__() == 0 and cargos.__len__() == 4 and equipos.__len__() == 9 and pagos.__len__() == 3:
                self.actionImportar.setVisible(True)
                self.actionExportar.setEnabled(False)
            else:
                self.actionImportar.setEnabled(False)
                self.actionExportar.setVisible(True)
        else:
            self.actionRecepcion.setEnabled(True)
            self.actionPago.setEnabled(True)
            self.actionFactura.setEnabled(True)
            self.actionAnticipos.setEnabled(True)
            self.menu_Operaciones.setEnabled(True)
            self.actioncambioFecha.setEnabled(True)
            self.actionExportar.setVisible(False)
            self.actionImportar.setVisible(False)
            
    def cambioFecha(self):
        self.ventanaFechaProcesamiento = QtWidgets.QDialog()
        self.ui = VentanaFechaProcesamiento(self)
        self.ui.setupUi(self.ventanaFechaProcesamiento) 
        self.ventanaFechaProcesamiento.exec()
        

    def presentacionVentana(self):
        etaller = mTaller()
        taller = etaller.cargarValorTaller()   
        
        self.labelTaller.setText(taller.getNombre())

        if taller.getLogo() != "../img/Taller.jpeg":
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(taller.getLogo(), 'png')
            logo = pixmap
        else: 
            logo = QtGui.QPixmap(self.generales.resource_path(taller.getLogo()))

        self.labelImagen.setPixmap(logo)
    
    # cambio de botones marcados 
    def botonHChecked(self):
        self.actionHoy.setChecked(True)
        self.actionTodas_las_Fechas.setChecked(False)
        self.actionRango_de_Fechas.setChecked(False)
        self.buttonChecked()

    def botonTChecked(self):
        self.actionHoy.setChecked(False)
        self.actionRango_de_Fechas.setChecked(False)
        self.actionTodas_las_Fechas.setChecked(True)
        self.buttonChecked()

    def botonRChecked(self):
        self.ventanaRangoFechas = QtWidgets.QDialog()
        self.ui = VentanaRangoFechas(self)
        self.ui.setupUi(self.ventanaRangoFechas) 
        self.ventanaRangoFechas.exec()

    def rangoCancelado(self):
        self.actionRango_de_Fechas.setChecked(False)

    def rangoFechas(self, fecha_inicio, fecha_fin):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.actionHoy.setChecked(False)
        self.actionRango_de_Fechas.setChecked(True)
        self.actionTodas_las_Fechas.setChecked(False)
        self.buttonChecked()

    def acercaDe(self):
        self.ventanaAcerca = QtWidgets.QDialog()
        self.ui = VentanaAcerca()
        self.ui.setupUi(self.ventanaAcerca) 
        self.ventanaAcerca.exec()
        
    # cambio de boton de mostrar a ocultar
    def mostrarCanceladas(self):
        self.actionMostrar.setVisible(False)
        self.actionOcultar.setVisible(True)
        self.buttonChecked()
        
    # cambio de boton de ocultar a mostrar
    def ocultarCanceladas(self):
        self.actionMostrar.setVisible(True)
        self.actionOcultar.setVisible(False)
        self.buttonChecked()

    # oculto o muestro filas dependiendo de la seleccion de fechas yel estado de las facturas
    def buttonChecked(self):
        hoy = self.generales.fechaDocumentos()
        for fila in range(self.tableWidget.rowCount()):
            if self.actionNueva.text() == 'Nueva Recepción':
                fecha = self.tableWidget.item(fila, 4).text()
            else:
                fecha = self.tableWidget.item(fila, 5).text()
                
            estado = int(self.tableWidget.item(fila,1).text())

            if self.actionRango_de_Fechas.isChecked() and not self.comparacionFecha(fecha) or ( self.actionMostrar.isVisible() and estado == 0):
                self.tableWidget.setRowHidden(fila, True)
            elif self.actionHoy.isChecked() and hoy != fecha or ( self.actionMostrar.isVisible() and estado == 0):
                self.tableWidget.setRowHidden(fila, True)
            elif self.actionTodas_las_Fechas.isChecked() or ( self.actionMostrar.isVisible() and estado == 0):
                self.tableWidget.setRowHidden(fila, False)
            else:
                self.tableWidget.setRowHidden(fila, False)
    

    def comparacionFecha(self, fecha):        
        ahora = datetime.strptime(fecha, '%d/%m/%Y')

        if self.fecha_inicio <= ahora <= self.fecha_fin:
            result = True
        else:
            result = False
        return result

    # configuracion de los nombres de los botones 
    def configuracionBotonesMenu(self, configuracion):
        self.actionEliminar.setEnabled(False)
        self.actionAbrir.setEnabled(False)
        self.actionCancelar.setEnabled(False)
        self.actionConfirmar.setEnabled(False)
        self.actionImprimir.setEnabled(False)
        self.actionConformidad.setEnabled(False)

        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)

        if configuracion == 1:
            self.actionNueva.setText('Nueva Recepción')
            self.actionAbrir.setText('Abrir Recepción')
            self.actionEliminar.setText('Eliminar Recepción')
            self.actionConfirmar.setText('Confirmar Recepción')
            self.actionCancelar.setText('Cancelar Recepción')
            self.actionImprimir.setText('Imprimir Recepción')
            self.actionMostrar.setText('Mostrar Recepciones Canceladas')
            self.actionOcultar.setText('Ocultar Recepciones Canceladas')
            self.actionConformidad.setVisible(False)
            self.actionOcultar.setVisible(False)
            self.llenadoTablaRecepcion()

        if configuracion == 2:
            self.actionNueva.setText('Nueva Factura')
            self.actionAbrir.setText('Abrir Factura')
            self.actionEliminar.setText('Eliminar Factura')
            self.actionConfirmar.setText('Confirmar Factura')
            self.actionCancelar.setText('Cancelar Factura')
            self.actionImprimir.setText('Imprimir Factura')
            self.actionMostrar.setText('Mostrar Facturas Canceladas')
            self.actionOcultar.setText('Ocultar Facturas Canceladas')
            self.actionConformidad.setVisible(True)
            self.actionOcultar.setVisible(False)
            self.llenadoTablaFactura()

        if configuracion == 3:
            self.actionNueva.setText('Nuevo Cobro')
            self.actionAbrir.setText('Abrir Cobro')
            self.actionEliminar.setText('Eliminar Cobro')
            self.actionConfirmar.setText('Confirmar Cobro')
            self.actionCancelar.setText('Cancelar Cobro')
            self.actionImprimir.setText('Imprimir Cobro')
            self.actionMostrar.setText('Mostrar Cobros Cancelados')
            self.actionOcultar.setText('Ocultar Cobros Cancelados')
            self.actionConformidad.setVisible(False)
            self.actionOcultar.setVisible(False)
            self.llenadoTablaCobro()

        if configuracion == 4:
            self.actionNueva.setText('Nueva Operación de Anticipo')
            self.actionAbrir.setText('Abrir Operación de Anticipo')
            self.actionEliminar.setText('Eliminar Operación de Anticipo')
            self.actionConfirmar.setText('Confirmar Operación de Anticipo')
            self.actionCancelar.setText('Cancelar Operación de Anticipo')
            self.actionImprimir.setText('Imprimir Operación de Anticipo')
            self.actionMostrar.setText('Mostrar Anticipos Cancelados')
            self.actionOcultar.setText('Ocultar Anticipos Cancelados')
            self.actionConformidad.setVisible(False)
            self.actionOcultar.setVisible(False)
            self.llenadoTablaAnticipo()
        
        if configuracion != self.confAtiva:
            self.actionHoy.setChecked(True)
            self.actionTodas_las_Fechas.setChecked(False)
            self.actionRango_de_Fechas.setChecked(False)
        self.confAtiva = configuracion

        self.verificarLicencia()
        self.buttonChecked()

    # nueva  principal
    def nuevaVentana(self):        
        if self.actionNueva.text() == 'Nueva Recepción':
            self.nuevaRecepcion()
        if self.actionNueva.text() == 'Nueva Factura':
            servicios = mServicio().cargarDatosServicio()
            if servicios.__len__() != 0:
                self.nuevaFactura()
            else:                
                self.generales.mensageInformacion("informacion",
                                    "Error de factura",
                                    "No se pueden generar Facturas si no tiene servicios en el sistema.                ")
        if self.actionNueva.text() == 'Nuevo Cobro': 
            self.nuevoCobro()
        if self.actionNueva.text() == 'Nueva Operación de Anticipo': 
            self.nuevoAnticipo() 

    #abrir principal
    def abrirVentana(self):
        if self.actionAbrir.isEnabled:
            if self.actionAbrir.text() == 'Abrir Recepción':
                self.abrirRecepcion()
            elif self.actionAbrir.text() == 'Abrir Factura':
                self.abrirFactura()
            elif self.actionAbrir.text() == 'Abrir Cobro': 
                self.abrirCobro()
            elif self.actionAbrir.text() == 'Abrir Operación de Anticipo': 
                self.abrirAnticipo()


    #confirmar principal
    def confirmarVentana(self):
        if self.actionConfirmar.isEnabled:
            if self.actionConfirmar.text() == 'Confirmar Recepción':
                self.confirmarRecepcion()
            elif self.actionConfirmar.text() == 'Confirmar Factura':
                self.confirmarFactura()
            elif self.actionConfirmar.text() == 'Confirmar Cobro': 
                self.confirmarCobro()
            elif self.actionConfirmar.text() == 'Confirmar Operación de Anticipo': 
                self.confirmarAnticipo()

    #cancelar principal
    def cancelarVentana(self):
        if self.actionCancelar.isEnabled:
            if self.actionCancelar.text() == 'Cancelar Recepción':
                self.cancelarRecepcion()
            elif self.actionCancelar.text() == 'Cancelar Factura':
                self.cancelarFactura()
            elif self.actionCancelar.text() == 'Cancelar Cobro': 
                self.cancelarCobro()
            elif self.actionCancelar.text() == 'Cancelar Operación de Anticipo': 
                self.cancelarAnticipo()

    #eliminar principal
    def eliminarVentana(self):
        if self.actionEliminar.isEnabled:
            if self.actionEliminar.text() == 'Eliminar Recepción':
                self.eliminarRecepcion()
            elif self.actionEliminar.text() == 'Eliminar Factura':
                self.eliminarFactura()
            elif self.actionEliminar.text() == 'Eliminar Cobro': 
                self.eliminarCobro()
            elif self.actionEliminar.text() == 'Eliminar Operación de Anticipo': 
                self.eliminarAnticipo()                

    # impresion de documentos
    def imprimirDocumento(self):        
        fila = self.tableWidget.currentRow()
        seleccion = self.tableWidget.item(fila,0).text()
        if self.actionImprimir.isEnabled:
            if self.actionImprimir.text() == 'Imprimir Recepción':
                erecepcion = self.mrececpcion.obtenerRecepcionEspecifico(seleccion)
                self.reporte.recepcionDesglosada(erecepcion, self.usuario, self)
            elif self.actionImprimir.text() == 'Imprimir Factura':
                efactura = self.mfactura.obtenerFacturaEspecifico(seleccion)
                self.reporte.facturaDesglosada(efactura, self.usuario, self)
            elif self.actionImprimir.text() == 'Imprimir Cobro': 
                ecobro = self.mcobro.obtenerCobroEspecifico(seleccion)
                self.reporte.cobroDesglosado(ecobro, self.usuario, self)
            elif self.actionImprimir.text() == 'Imprimir Operación de Anticipo': 
                eanticipo = self.manticipo.obtenerAnticipoEspecifico(seleccion)
                self.reporte.anticipoDesglosado(eanticipo, self.usuario, self)
    
    # impresion de certifico de conformidad      
    def imprimirConformidad(self):
        fila = self.tableWidget.currentRow()
        seleccion = self.tableWidget.item(fila,0).text()
        efactura = self.mfactura.obtenerFacturaEspecifico(seleccion)
        self.reporte.certificoConformidad(efactura, self.usuario, self)

    # fila seleccionada ne la tabla
    def filaSeleccionada(self):
        fila = self.tableWidget.currentRow()
        if fila != -1:             
            self.actionImprimir.setEnabled(self.verificarLicencia())
            if int(self.tableWidget.item(fila, 1).text()) == 0:  
                self.actionConfirmar.setEnabled(False)
                self.actionAbrir.setEnabled(True)
                self.actionEliminar.setEnabled(False)
                self.actionCancelar.setEnabled(False)
                self.actionConformidad.setEnabled(False)
            
            elif int(self.tableWidget.item(fila, 1).text()) == 1:
                self.actionConfirmar.setEnabled(True)
                self.actionAbrir.setEnabled(True)
                self.actionEliminar.setEnabled(True)
                self.actionCancelar.setEnabled(False)
                self.actionConformidad.setEnabled(False)
            
            else:
                self.actionConfirmar.setEnabled(False)
                self.actionAbrir.setEnabled(True)
                self.actionEliminar.setEnabled(False)
                self.actionCancelar.setEnabled(True)
                self.actionConformidad.setEnabled(True)
            

    # llenado para recepción
    def llenadoTablaRecepcion(self):
        self.tablaRecepcion()
        for fila, data in enumerate(self.mrececpcion.cargarDatosRecepcion()):
            self.tableWidget.insertRow(fila)

            usuario = self.musuario.obtenerUsuarioEspecifico(data.getUsuario())
            cliente = self.mcliente.obtenerDatosClientesEspecifica(data.getCliente())
            self.utilizacionIconos(fila, data.getEstado(), data.getNoRecepcion())

            self.tableWidget.setItem(fila, 0, QTableWidgetItem(str(data.getIdRecepcion())))
            self.tableWidget.setItem(fila, 1, QTableWidgetItem(str(data.getEstado())))
            self.tableWidget.setItem(fila, 3, QTableWidgetItem(str(cliente.getNombre())))
            self.tableWidget.setItem(fila, 4, QTableWidgetItem(str(data.getFecha())))
            self.tableWidget.setItem(fila, 5, QTableWidgetItem(str(usuario.getUsername())))
        #self.buttonChecked()

    # llenado para factura
    def llenadoTablaFactura(self):
        self.tablaFactura()
        for fila, data in enumerate(self.mfactura.cargarDatosFactura()):
            self.tableWidget.insertRow(fila)

            usuario = self.musuario.obtenerUsuarioEspecifico(data.getUsuario())
            cliente = self.mcliente.obtenerDatosClientesEspecifica(data.getCliente())
            self.utilizacionIconos(fila, data.getEstado(), data.getNoFactura())

            self.tableWidget.setItem(fila, 0, QTableWidgetItem(str(data.getIdFactura())))
            self.tableWidget.setItem(fila, 1, QTableWidgetItem(str(data.getEstado())))
            self.tableWidget.setItem(fila, 3, QTableWidgetItem(str(cliente.getNombre())))
            self.tableWidget.setItem(fila, 4, QTableWidgetItem(self.generales.floatToStr(data.getTotalFactura())))
            self.tableWidget.setItem(fila, 5, QTableWidgetItem(str(data.getFecha())))
            self.tableWidget.setItem(fila, 6, QTableWidgetItem(str(usuario.getUsername()))) 
        #self.buttonChecked()   

    # llenado para cobro
    def llenadoTablaCobro(self):
        self.tablaCobro()
        for fila, data in enumerate(self.mcobro.cargarDatosCobro()):
            self.tableWidget.insertRow(fila)

            usuario = self.musuario.obtenerUsuarioEspecifico(data.getUsuario())
            cliente = self.mcliente.obtenerDatosClientesEspecifica(data.getCliente())
            self.utilizacionIconos(fila, data.getEstado(), data.getNoCobro())

            self.tableWidget.setItem(fila, 0, QTableWidgetItem(str(data.getIdCobro())))
            self.tableWidget.setItem(fila, 1, QTableWidgetItem(str(data.getEstado())))
            self.tableWidget.setItem(fila, 3, QTableWidgetItem(str(cliente.getNombre())))
            self.tableWidget.setItem(fila, 4, QTableWidgetItem(self.generales.floatToStr(data.getTotalCobro())))
            self.tableWidget.setItem(fila, 5, QTableWidgetItem(str(data.getFecha())))
            self.tableWidget.setItem(fila, 6, QTableWidgetItem(str(usuario.getUsername())))
        #self.buttonChecked()

    #iconos dependiendo del estado
    def utilizacionIconos(self, fila, estado, documento):
        item = QTableWidgetItem()

        if estado == 0: #cancelada
            imagen = "../img/TextCancelado.png"
            item.setToolTip('Cancelado')
        elif estado == 1: #en uso
            imagen = "../img/Text.png"
            item.setToolTip('En Edición')
        elif estado == 2: # confirmada
            imagen = "../img/TextConfirmado.png"
            item.setToolTip('Confirmado')
        elif estado == 3: #pagado
            imagen = "../img/TextPagado.png" #cambiar icono
            item.setToolTip('Pagada')
        else: #pago paricial
            imagen = "../img/Ok.ico" #cambiar icono
            item.setToolTip('Pago Parcial')
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.generales.resource_path(imagen)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        item.setIcon(icon)
        item.setText(str(documento))

        self.tableWidget.setItem(fila, 2, item)

    def llenadoTablaAnticipo(self):
        self.tablaAnticipo()
        for fila, data in enumerate(self.manticipo.cargarDatosAnticipo()):
            self.tableWidget.insertRow(fila)

            usuario = self.musuario.obtenerUsuarioEspecifico(data.getUsuario())
            cliente = self.mcliente.obtenerDatosClientesEspecifica(data.getCliente())
            self.iconosAnticipos(fila, data.getEstado(), data.getNoAnticipo(), data.getFactura())

            self.tableWidget.setItem(fila, 0, QTableWidgetItem(str(data.getIdAnticipo())))
            self.tableWidget.setItem(fila, 1, QTableWidgetItem(str(data.getEstado())))
            self.tableWidget.setItem(fila, 3, QTableWidgetItem(str(cliente.getNombre())))
            self.tableWidget.setItem(fila, 4, QTableWidgetItem(self.generales.floatToStr(data.getMonto())))
            self.tableWidget.setItem(fila, 5, QTableWidgetItem(str(data.getFecha())))
            self.tableWidget.setItem(fila, 6, QTableWidgetItem(str(usuario.getUsername())))
        #self.buttonChecked()


    def iconosAnticipos(self, fila, estado, documento, factura):
        item = QTableWidgetItem()

        if estado == 0 and factura == "": # cancelada
            imagen = "../img/TextCancelado.png"
            item.setToolTip('Devolución Cancelada')
        elif estado == 1 and factura == "": #en uso
            imagen = "../img/Text.png"
            item.setToolTip('Devolución en Edición')
        elif estado == 2 and factura == "": # confirmada
            imagen = "../img/TextConfirmado.png"
            item.setToolTip('Devolución Confirmada')
        elif estado == 0 and factura != "": # cancelada
            imagen = "../img/TextCancelado.png"
            item.setToolTip('Liquidación Cancelada')
        elif estado == 1 and factura != "": #en uso
            imagen = "../img/Text.png"
            item.setToolTip('Liquidación en Edición')
        else:
            imagen = "../img/TextConfirmado.png"
            item.setToolTip('Liquidación Confirmada')
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.generales.resource_path(imagen)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        item.setIcon(icon)
        item.setText(str(documento))

        self.tableWidget.setItem(fila, 2, item)
    
    # encabezado de tabla recepcion
    def tablaRecepcion(self):
        self.tableWidget.setColumnCount(6)

        #ancho de las columnas
        self.tableWidget.setColumnWidth(0,0)
        self.tableWidget.setColumnWidth(1,20)
        self.tableWidget.setColumnWidth(2,140)
        self.tableWidget.setColumnWidth(3,400)
        self.tableWidget.setColumnWidth(4,150)
        self.tableWidget.setColumnWidth(5,150)

        self.tableWidget.setColumnHidden(0,True)
        self.tableWidget.setColumnHidden(1,True)
        #cabecera de la tabla

        self.tablas.headerListaRecepciones(0, self.tableWidget)    
        self.tablas.headerListaRecepciones(1, self.tableWidget)    
        self.tablas.headerListaRecepciones(2, self.tableWidget)    
        self.tablas.headerListaRecepciones(3, self.tableWidget)   
        self.tablas.headerListaRecepciones(4, self.tableWidget)  
        self.tablas.headerListaRecepciones(5, self.tableWidget)  

    # encabezado de tabla factura
    def tablaFactura(self):
        self.tableWidget.setColumnCount(7)

        #ancho de las columnas
        self.tableWidget.setColumnWidth(0,0)
        self.tableWidget.setColumnWidth(1,20)
        self.tableWidget.setColumnWidth(2,140)
        self.tableWidget.setColumnWidth(3,400)
        self.tableWidget.setColumnWidth(4,100)
        self.tableWidget.setColumnWidth(5,100)
        self.tableWidget.setColumnWidth(6,100)

        self.tableWidget.setColumnHidden(0,True)
        self.tableWidget.setColumnHidden(1,True)
        #cabecera de la tabla

        self.tablas.headerListaFacturas(0, self.tableWidget)    
        self.tablas.headerListaFacturas(1, self.tableWidget)    
        self.tablas.headerListaFacturas(2, self.tableWidget)    
        self.tablas.headerListaFacturas(3, self.tableWidget)   
        self.tablas.headerListaFacturas(4, self.tableWidget)  
        self.tablas.headerListaFacturas(5, self.tableWidget)  
        self.tablas.headerListaFacturas(6, self.tableWidget)     

    # encabezado de tabla cobro
    def tablaCobro(self):
        self.tableWidget.setColumnCount(7)

        #ancho de las columnas
        self.tableWidget.setColumnWidth(0,50)
        self.tableWidget.setColumnWidth(1,20)
        self.tableWidget.setColumnWidth(2,140)
        self.tableWidget.setColumnWidth(3,400)
        self.tableWidget.setColumnWidth(4,100)
        self.tableWidget.setColumnWidth(5,100)
        self.tableWidget.setColumnWidth(6,100)

        self.tableWidget.setColumnHidden(0,True)
        self.tableWidget.setColumnHidden(1,True)
        #cabecera de la tabla

        self.tablas.headerListaCobros(0, self.tableWidget)    
        self.tablas.headerListaCobros(1, self.tableWidget)    
        self.tablas.headerListaCobros(2, self.tableWidget)    
        self.tablas.headerListaCobros(3, self.tableWidget)   
        self.tablas.headerListaCobros(4, self.tableWidget)  
        self.tablas.headerListaCobros(5, self.tableWidget)  
        self.tablas.headerListaCobros(6, self.tableWidget)   

    # encabezado de tabla anticipos
    def tablaAnticipo(self):
        self.tableWidget.setColumnCount(7)

        #ancho de las columnas
        self.tableWidget.setColumnWidth(0,50)
        self.tableWidget.setColumnWidth(1,20)
        self.tableWidget.setColumnWidth(2,140)
        self.tableWidget.setColumnWidth(3,400)
        self.tableWidget.setColumnWidth(4,100)
        self.tableWidget.setColumnWidth(5,100)
        self.tableWidget.setColumnWidth(6,100)

        self.tableWidget.setColumnHidden(0,True)
        self.tableWidget.setColumnHidden(1,True)
        #cabecera de la tabla

        self.tablas.headerListaAnticipos(0, self.tableWidget)    
        self.tablas.headerListaAnticipos(1, self.tableWidget)    
        self.tablas.headerListaAnticipos(2, self.tableWidget)    
        self.tablas.headerListaAnticipos(3, self.tableWidget)   
        self.tablas.headerListaAnticipos(4, self.tableWidget)  
        self.tablas.headerListaAnticipos(5, self.tableWidget)  
        self.tablas.headerListaAnticipos(6, self.tableWidget)    


    # Abrir ventana de recepciones
    def nuevaRecepcion(self):
        erecepcion = eRecepcion()
        self.ventanaRecepcion = QtWidgets.QDialog()
        self.ui = VentanaRecepcion(erecepcion, self.usuario, self)
        self.ui.setupUi(self.ventanaRecepcion) 
        self.ventanaRecepcion.exec()

    # editar recepcion
    def abrirRecepcion(self):
        fila = self.tableWidget.currentRow()
        idrececpcion = self.tableWidget.item(fila, 0).text()
        erecepcion = self.mrececpcion.obtenerRecepcionEspecifico(idrececpcion)
        self.ventanaRecepcion = QtWidgets.QDialog()
        self.ui = VentanaRecepcion(erecepcion, self.usuario, self)
        self.ui.setupUi(self.ventanaRecepcion) 
        self.ventanaRecepcion.exec()

    #confirmar recepcion
    def confirmarRecepcion(self):
        fila = self.tableWidget.currentRow()
        idrececpcion = self.tableWidget.item(fila, 0).text()
        erecepcion = self.mrececpcion.obtenerRecepcionEspecifico(idrececpcion)
        resp = self.generales.mensageSiNo("Confirmar recepción", "La recepción va a ser confirmada!                    ",
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mrececpcion.editarDatosRecepcion(erecepcion,2)
            self.configuracionBotonesMenu(1)

    #cancelar recepcion
    def cancelarRecepcion(self):
        fila = self.tableWidget.currentRow()
        idrececpcion = self.tableWidget.item(fila, 0).text()
        erecepcion = self.mrececpcion.obtenerRecepcionEspecifico(idrececpcion)
        resp = self.generales.mensageSiNo("Cancelar recepción", "La recepción va a ser cancelada!                    ",
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mrececpcion.editarDatosRecepcion(erecepcion,0)
            self.configuracionBotonesMenu(1)

    #elimianr recepcion
    def eliminarRecepcion(self):
        fila = self.tableWidget.currentRow()
        idrececpcion = self.tableWidget.item(fila, 0).text()
        erecepcion = self.mrececpcion.obtenerRecepcionEspecifico(idrececpcion)
        resp = self.generales.mensageSiNo("Eliminar recepción", "La recepción va a ser eliminada!                    ",
                                                "Desea continuar con el proceso?")
        if resp == 1:
            inventarios = self.minventario.cargarDatosInventario()
            for inventario in inventarios:
                if inventario.getRecepcion() == erecepcion.getIdRecepcion():
                    self.minventario.eliminarDatosInventario(inventario.getIdInventario())

            self.mrececpcion.eliminarRecepcion(erecepcion.getIdRecepcion())
            self.configuracionBotonesMenu(1)

    # Abrir ventana de factura
    def nuevaFactura(self):
        efactura = eFactura()
        self.ventanaFactura = QtWidgets.QDialog()
        self.ui = VentanaFactura(efactura ,self.usuario, self)
        self.ui.setupUi(self.ventanaFactura) 
        self.ventanaFactura.exec()

    #editar factura
    def abrirFactura(self):
        fila = self.tableWidget.currentRow()
        idfactura = self.tableWidget.item(fila, 0).text()
        efactura = self.mfactura.obtenerFacturaEspecifico(idfactura)
        self.ventanaFactura = QtWidgets.QDialog()
        self.ui = VentanaFactura(efactura, self.usuario, self)
        self.ui.setupUi(self.ventanaFactura) 
        self.ventanaFactura.exec()

    #confirmar factura
    def confirmarFactura(self):
        fila = self.tableWidget.currentRow()
        idfactura = self.tableWidget.item(fila, 0).text()
        efactura = self.mfactura.obtenerFacturaEspecifico(idfactura)
        resp = self.generales.mensageSiNo("Confirmar factura", "La factura va a ser confirmada!                    ",
                                                "Desea continuar con el proceso?")
        if resp == 1:            
            facturas = self.mfactura.cargarDatosFacturaConNumero() 
            #generando el numero del documento
            if facturas.__len__() > 0:
                documento = facturas[-1].getNoFactura()
            else:
                documento = ""
            efactura.setNoFactura(self.generales.numeroDocumento(documento))
            efactura.setFecha(self.generales.fechaDocumentos())
            self.mfactura.editarDatosFactura(efactura,2)
            self.actualizarInventario(idfactura, 0)
            self.configuracionBotonesMenu(2)

    #cancelar factura
    def cancelarFactura(self):
        fila = self.tableWidget.currentRow()
        idfactura = self.tableWidget.item(fila, 0).text()
        efactura = self.mfactura.obtenerFacturaEspecifico(idfactura)

        resp = self.generales.mensageSiNo("Confirmar Factura", "La factura va a ser cancelada!                    ",
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mfactura.editarDatosFactura(efactura,0)
            self.actualizarInventario(idfactura, 1)
            self.configuracionBotonesMenu(2)

    #eliminar factura
    def eliminarFactura(self):
        fila = self.tableWidget.currentRow()
        idfactura = self.tableWidget.item(fila, 0).text()
        efactura = self.mfactura.obtenerFacturaEspecifico(idfactura)
        facdesglose = self.mfacturadesglose.cargarDatosFacturaDesglose()
        resp = self.generales.mensageSiNo("eliminar Factura", "La factura va a ser eliminada!                    ",
                                                "Desea continuar con el proceso?")
        if resp == 1:
            for data in facdesglose:
                if data.getFactura() == efactura.getIdFactura():
                    self.mfacturadesglose.eliminarDatosFacturaDesglose(data.getIdFacturaDesglose())

            self.mfactura.eliminarFactura(efactura.getIdFactura())
            self.configuracionBotonesMenu(2)
    
    #actualizar factura
    def actualizarInventario(self, idfactura, modo):
        factdesglose = self.mfacturadesglose.cargarDatosFacturaDesglose()
        for data in factdesglose:
            if int(data.getFactura()) == int(idfactura):
                inventario = self.minventario.obtenerInventarioEspecifico(data.getInventario())
                cantidad =float(data.getCantidad())
                inv =inventario.getActivo()
                cantInv = inventario.getCantidad()
                if inv != "":
                    if modo == 1:
                        if (int(inv) + int(round(cantidad,0))) > int(cantInv):
                            activo = cantInv
                        else:
                            activo = int(inv) + int(round(cantidad,0))
                    else:
                        if inv != 0:
                            activo = int(inv) - int(round(cantidad,0))
                    self.minventario.editarDatosInventario(inventario, activo)

    # Abrir ventana de Cobros
    def nuevoCobro(self):
        ecobro = eCobro()
        self.ventanaCobro = QtWidgets.QDialog()
        self.ui = VentanaCobro(ecobro, self.usuario, self)
        self.ui.setupUi(self.ventanaCobro) 
        self.ventanaCobro.exec()

    #editar cobro
    def abrirCobro(self):
        fila = self.tableWidget.currentRow()
        idcobro = self.tableWidget.item(fila, 0).text()
        ecobro = self.mcobro.obtenerCobroEspecifico(idcobro)
        self.ventanaCobro = QtWidgets.QDialog()
        self.ui = VentanaCobro(ecobro, self.usuario, self)
        self.ui.setupUi(self.ventanaCobro) 
        self.ventanaCobro.exec()

    #confirmar cobro
    def confirmarCobro(self):
        fila = self.tableWidget.currentRow()
        idcobro = self.tableWidget.item(fila, 0).text()
        ecobro = self.mcobro.obtenerCobroEspecifico(idcobro)
        resp = self.generales.mensageSiNo("Confirmar cobro", "El cobro va a ser confirmado!                    ",
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mcobro.editarDatosCobro(ecobro,2)
            self.actualizarEstadoFactura(idcobro, 3)
            self.configuracionBotonesMenu(3)

    #cancelar cobro
    def cancelarCobro(self):
        fila = self.tableWidget.currentRow()
        idcobro = self.tableWidget.item(fila, 0).text()
        ecobro = self.mcobro.obtenerCobroEspecifico(idcobro)    
        resp = self.generales.mensageSiNo("Cancelar cobro", "El cobro va a ser cancelado!                    ",
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.mcobro.editarDatosCobro(ecobro,0)
            self.actualizarEstadoFactura(idcobro, 2)
            self.configuracionBotonesMenu(3)

    #eliminar cobro
    def eliminarCobro(self):
        fila = self.tableWidget.currentRow()
        idcobro = self.tableWidget.item(fila, 0).text()
        ecobro = self.mcobro.obtenerCobroEspecifico(idcobro)
        ecobrofactura = self.mcobrofactura.cargarDatosCobroFactura()
        resp = self.generales.mensageSiNo("Eliminar cobro", "El cobro va a ser eliminado!                    ",
                                                "Desea continuar con el proceso?")
        if resp == 1:
            for data in ecobrofactura:
                if data.getCobro() == ecobro.getIdCobro():
                    self.mcobrofactura.eliminarDatosCobroFactura(data.getIdCobroFactura())

            self.mcobro.eliminarCobro(ecobro.getIdCobro())
            self.configuracionBotonesMenu(3)

    # actualizar factura a pagado
    def actualizarEstadoFactura(self, idcobro, modo):
        cobrofactura = self.mcobrofactura.cargarDatosCobroFactura()
        for data in cobrofactura:
            if int(data.getCobro()) == int(idcobro):
                factura = self.mfactura.obtenerFacturaEspecifico(data.getFactura())
                if factura.getIdFactura() != "":
                    if modo == 3 and data.getTipo() == 1: 
                        self.mfactura.editarDatosFactura(factura, 4)
                    else:
                        self.mfactura.editarDatosFactura(factura, modo)

    #funcion para liquidar los anticipos 
    def nuevoAnticipo(self):
        self.ventanaAnticipo = QtWidgets.QDialog()
        self.ui = VentanaAnticipo(self.usuario, self)
        self.ui.setupUi(self.ventanaAnticipo) 
        self.ventanaAnticipo.exec()

    #editar anticipo
    def abrirAnticipo(self):
        fila = self.tableWidget.currentRow()
        idanticipo = self.tableWidget.item(fila, 0).text()
        eanticipo = self.manticipo.obtenerAnticipoEspecifico(idanticipo)

        if eanticipo.getFactura() == "":
            self.ventanaDevolucion = QtWidgets.QDialog()
            self.ui = VentanaDevolucion(eanticipo, self.usuario, self)
            self.ui.setupUi(self.ventanaDevolucion) 
            self.ventanaDevolucion.exec()
        else:
            self.ventanaLiquidacion = QtWidgets.QDialog()
            self.ui = VentanaLiquidacion(eanticipo, self.usuario, self)
            self.ui.setupUi(self.ventanaLiquidacion) 
            self.ventanaLiquidacion.exec()

    #confirmar anticipo
    def confirmarAnticipo(self):
        fila = self.tableWidget.currentRow()
        idanticipo = self.tableWidget.item(fila, 0).text()
        eanticipo = self.manticipo.obtenerAnticipoEspecifico(idanticipo)
        if eanticipo.getFactura() == "":
            aux = 'devolución'
        else:
            aux = 'liquidación de la factura'
        resp = self.generales.mensageSiNo("Confirmar " + aux , "La " + aux + " va a ser confirmada!                    ",
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.manticipo.editarDatosAnticipo(eanticipo, 2)
            if eanticipo.getFactura() != "":
                factura = self.mfactura.obtenerFacturaEspecifico(eanticipo.getFactura())
                if eanticipo.getMonto() == factura.getTotalFactura():
                    self.mfactura.editarDatosFactura(factura,3)
                else:
                    self.mfactura.editarDatosFactura(factura,4)
            self.configuracionBotonesMenu(4)

    #cancelar anticipo
    def cancelarAnticipo(self):
        fila = self.tableWidget.currentRow()
        idanticipo = self.tableWidget.item(fila, 0).text()
        eanticipo = self.manticipo.obtenerAnticipoEspecifico(idanticipo)
        if eanticipo.getFactura() == "":
            aux = 'devolución'
        else:
            aux = 'liquidación de la factura'   
        resp = self.generales.mensageSiNo("Cancelar " + aux , "La " + aux + " va a ser cancelada!                    ",
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.manticipo.editarDatosAnticipo(eanticipo, 0)
            if eanticipo.getFactura() != "":
                factura = self.mfactura.obtenerFacturaEspecifico(eanticipo.getFactura())
                self.mfactura.editarDatosFactura(factura,2)
            self.configuracionBotonesMenu(4)

    # eliminar anticipo en edicion
    def eliminarAnticipo(self):
        fila = self.tableWidget.currentRow()
        idanticipo = self.tableWidget.item(fila, 0).text()
        eanticipo = self.manticipo.obtenerAnticipoEspecifico(idanticipo)
        if eanticipo.getFactura() == "":
            aux = 'devolución'
        else:
            aux = 'liquidación de la factura'
        resp = self.generales.mensageSiNo("Eliminar " + aux, 'La ' + aux + " va a ser eliminada!                    ",
                                                "Desea continuar con el proceso?")
        if resp == 1:
            self.manticipo.eliminarDatosAnticipo(eanticipo.getIdAnticipo())
            self.configuracionBotonesMenu(4)

    # carga el fichero de licencia 
    def iniciarLicencia(self):
        taller = self.mtaller.cargarValorTaller()
        duenno = self.mduenno.cargarDatosDuenno()
        nombreArchivo, _ = QtWidgets.QFileDialog.getOpenFileName(self,  'Cargar fichero KEY', 
                                                            self.generales.resource_path("../"),
                                                           "Archivos KEY (*.key)")

        if nombreArchivo:
            fichero = ""
        
            with open(nombreArchivo, 'r') as f:
                fichero += f.read()
              
            if self.generales.verificarLicencia(taller, duenno, fichero):
                taller.setLicencia(fichero)
                self.mtaller.guardarDatosTaller(taller)
                self.menuLicencia.setEnabled(False)
                self.menu_Consultas.setEnabled(True)
            else:
                self.generales.mensageInformacion("error",
                                    "Licencia Inválida",
                                    "La licencia suministrada no se corresponde con la semilla.                ")


    #genera un fichero para la licencia
    def generarSemilla(self):
        taller = self.mtaller.cargarValorTaller()
        duenno = self.mduenno.cargarDatosDuenno()
        nombreArchivo, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Guardar llave", 
                                                            self.generales.resource_path("../" + duenno.getNombre() + duenno.getApellidos() + '.agr'),
                                                           "Archivos AGR (*.agr)")

        if nombreArchivo:
            fichero = unidecode(taller.getNombre()) + '\n' + unidecode(taller.getDireccion()) + '\n' + unidecode(duenno.getNombre())  + '\n' + unidecode(duenno.getApellidos())  + '\n' + duenno.getCarnet()
            
            with open(nombreArchivo, 'w') as f:
                f.write(fichero)

    # ventana para generar reporte de inventarios 
    def cargarInventario(self):
        self.ventanaCargarInventario = QtWidgets.QDialog()
        self.ui = VentanaCargarInventario()
        self.ui.setupUi(self.ventanaCargarInventario) 
        self.ventanaCargarInventario.exec()

    # ventana para generar reportes de facturacion cuentas cobradas y por cobrar
    def cargarFacturaCobros(self, opcion):
        facturas = self.mfactura.cargarDatosFactura()
        cobros = self.mcobro.cargarDatosCobro()
        
        if (opcion == "Cuentas Cobradas" and cobros.__len__() > 0) or (opcion != "Cuentas Cobradas" and facturas.__len__() > 0) : 
            self.ventanaCargarFacturaCobro = QtWidgets.QDialog()
            self.ui = VentanaCargarFacturaCobro(opcion)
            self.ui.setupUi(self.ventanaCargarFacturaCobro) 
            self.ventanaCargarFacturaCobro.exec()        
        else:            
            if opcion == "Cuentas Cobradas":
                operacion = "Operaciones de Cobros"
            else:
                operacion = "Facturas"
                
            self.generales.mensageInformacion('error', 'Error de reporte', 
                                            'No existen {} registradas en la base de datos. Registre operaciones para poder acceder a este reporte.'.format(operacion))

    # Abrir la ventana de configuraciones
    def invocarConfiguraciones(self):
        self.ventanaConfiguracion = QtWidgets.QDialog()
        self.ui = VentanaConfiguracion(self)
        self.ui.setupUi(self.ventanaConfiguracion) 
        self.ventanaConfiguracion.exec()

    # Abrir la ventana de Administracion de Usuarios
    def invocarAdministracionUsuario(self):
        self.ventanaAdministracionUsuario = QtWidgets.QDialog()
        self.ui = VentanaAdministracionUsuario()
        self.ui.setupUi(self.ventanaAdministracionUsuario) 
        self.ventanaAdministracionUsuario.exec()

    # Genero fichero a exportar
    def salvaConfiguraciones(self):
        clientes = self.mcliente.cargarDatosClientes()
        cargos = self.mcargo.cargarDatosCargo()
        fichaCliente = self.mfichaClinete.cargarDatosFichaCliente()
        umedida = self.mumedida.cargarDatosUnidadMedida()
        equipos = self.mequipo.cargarDatosEquipo()
        servicios = self.mservicio.cargarDatosServicio()
        pagos = self.mtipoPago.cargarDatosTipoPago()
        
        fichero = "###FICHERO DE CONFIGURACIONES###\n"
        
        for cliente in clientes:
            fichero +=  "CLIEN" + '|' + str(cliente.getIdCliente()) + '|' + cliente.getNombre() + '|' + cliente.getContrato() + '|' + cliente.getDireccion() + '|' + cliente.getCuenta() + '|' + str(cliente.getActivo()) + '\n'
                
        for cargo in cargos:
            fichero += "CARGO" + '|' + str(cargo.getIdCargo()) + '|' + cargo.getDescripcion() + '\n'
            
        for ficha in fichaCliente:
            fichero += "FICHA" + '|' + str(ficha.getIdFichaCliente()) + '|' + ficha.getNombre() + '|' + ficha.getApellidos() + '|' + ficha.getCarnet() + '|' + str(ficha.getCargo()) + '|' + str(ficha.getCliente()) + '|' + str(ficha.getActivo()) + '\n'
        
        for um in umedida:
            fichero += "UNIDA" + '|' + str(um.getIdUnidadMedida()) + '|' + um.getDescripcion() + '|' + um.getSigla()+ '|' + str(um.getActivo()) + '\n'
        
        for equipo in equipos:
            fichero += "EQUIP" + '|' + str(equipo.getIdEquipo()) + '|' + equipo.getDescripcion() + '|' + str(equipo.getActivo()) + '|' +  str(equipo.getMultiple()) + '\n'
       
        for serv in servicios:
            fichero += "SERVI" + '|' + str(serv.getIdServicio()) + '|' + serv.getDescripcion() + '|' + str(serv.getPrecio()) + '|' + str(serv.getUnidadMedida()) + '|' + str(serv.getEquipo()) + '|' + str(serv.getActivo()) + '\n'
                
        for pago in pagos:
            fichero += "PAGOS" + '|' + str(pago.getIdTipoPago()) + '|' + pago.getDescripcion() + '|' + str(pago.getActivo()) + '\n'
             
               
        return fichero

    # Exportar fichero de exportacion de configuraciones
    def exportarConfiguraciones(self):
        nombreArchivo, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Exportar Configuraciones", 
                                                            self.generales.resource_path("../configuraciones.agr"),
                                                           "Archivos AGR (*.agr)")

        if nombreArchivo:
            fichero = self.salvaConfiguraciones()
            
            with open(nombreArchivo, 'w') as f:
                f.write(fichero)
    
    # Importar fichero de exportacion de configuraciones
    def importarConfiguraciones(self):
        config = False 
        
        nombreArchivo, _ = QtWidgets.QFileDialog.getOpenFileName(self,  'Importar Carga Inicial', 
                                                            self.generales.resource_path("../"),
                                                           "Archivos AGR (*.agr)")

        if not nombreArchivo:              
            pass
        else:
            with open(nombreArchivo, 'r') as f:
                for linea in f:
                    if linea == "###FICHERO DE CONFIGURACIONES###\n":
                        config = True
                        break
                        
                    else:
                        self.generales.mensageInformacion('error', 'Error de carga inicial', 
                                        'El fichero {} no es un fichero de carga inicial.'.format(ntpath.basename(nombreArchivo)))
                        
                        break
                
                if config == True:                
                    for linea in f:
                        aux = linea.split('|')
                        
                        if aux[0] == "CLIEN":
                            ecliente = eCliente()
                            ecliente.setNombre(aux[2])
                            ecliente.setContrato(aux[3])
                            ecliente.setDireccion(aux[4])
                            ecliente.setCuenta(aux[5])
                            ecliente.setActivo(aux[6])            
                            self.mcliente.guardarDatosCliente(ecliente)      
                            
                        elif aux[0] == "CARGO":
                            ecargo = eCargo()
                            ecargo.setIdCargo(aux[1])
                            ecargo.setDescripcion(aux[2])
                            if not str(self.mcargo.obtenerCargoEspecifico(aux[1]).getIdCargo()).isnumeric():
                                self.mcargo.guardarDatosCargo(ecargo)    
                                    
                        elif aux[0] == "FICHA":
                            eficha = eFichaCliente()
                            eficha.setNombre(aux[2])
                            eficha.setApellidos(aux[3])
                            eficha.setCarnet(aux[4])
                            eficha.setCargo(aux[5])
                            eficha.setCliente(aux[6])
                            eficha.setActivo(aux[7])
                            self.mfichaClinete.guardarDatosFichaCliente(eficha)
                        
                        elif aux[0] == "UNIDA":
                            eum = eUnidadMedida()
                            eum.setIdUnidadMedida(aux[1])
                            eum.setDescripcion(aux[2])
                            eum.setSigla(aux[3])
                            eum.setActivo(aux[4])
                            self.mumedida.guardarDatosUnidadMedida(eum)
                            
                        elif aux[0] == "EQUIP":
                            eequipo = eEquipo()
                            eequipo.setIdEquipo(aux[1])
                            eequipo.setDescripcion(aux[2])
                            eequipo.setActivo(aux[3])
                            eequipo.setMultiple(aux[4])
                            if not str(self.mequipo.obtenerEquipoEspecifico(aux[1]).getIdEquipo()).isnumeric():
                                self.mequipo.guardarDatosEquipo(eequipo)
                            else:
                                self.mequipo.editarDatosEquipo(eequipo, eequipo.getActivo())
                                                    
                        elif aux[0] == "SERVI":
                            eserv = eServicio()
                            eserv.setDescripcion(aux[2])
                            eserv.setPrecio(aux[3])
                            eserv.setUnidadMedida(aux[4])
                            eserv.setEquipo(aux[5])
                            eserv.setActivo(aux[6])
                            self.mservicio.guardarDatosServicio(eserv)
                                
                        elif aux[0] == "PAGOS":    
                            epago = eTipoPago()         
                            epago.setIdTipoPago(aux[1])
                            epago.setDescripcion(aux[2])
                            epago.setActivo(aux[3])
                            if not str(self.mtipoPago.obtenerTipoPagoEspecifico(aux[2]).getIdTipoPago()).isnumeric():
                                self.mtipoPago.guardarDatosTipoPago(epago)
                            else:
                                self.mtipoPago.editarDatosTipoPago(epago, aux[3])
                
                f.close()
                
                self.generales.mensageInformacion('informacion', 'Importación exitosa', 
                                'La importación de la configuracón a concluido con éxito')
                        
                self.actionImportar.setEnabled(False)
                self.actionExportar.setEnabled(True)
                

    # backup de la base de datos
    def backupDataBase(self):
        nombreArchivo, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Salvar Base de Datos", 
                                                            self.generales.resource_path("../backupdatabase_dump.sql"),
                                                           "Archivos SQL (*.sql)")

        if nombreArchivo:            
            conn = self.baseTaller.abrir()
            with io.open(nombreArchivo , 'w') as p:
                for line in conn.iterdump():
                    p.write('%s\n' % line)
            
            self.generales.mensageInformacion('informacion', 'Salva exitosa', 
                            'La Salva de la base de datos a concluido con éxito')
            
    # Restaurar la base de tatos 
    def uploadDataBase(self):
        config = False 
        
        nombreArchivo, _ = QtWidgets.QFileDialog.getOpenFileName(self,  'Restaurar Base de Datos', 
                                                            self.generales.resource_path("../"),
                                                           "Archivos SQL (*.sql)")

        if not nombreArchivo:              
            pass
        else:
            with open(nombreArchivo, 'r') as f:
                sql = f.read()
            
            os.remove('taller.db')    
            file = open('taller.db', 'w')
            file.close()
                
            conn = self.baseTaller.abrir()
            conn.executescript(sql)
            conn.close()
            self.generales.mensageInformacion('informacion', 'Restaura exitosa', 
                            'La Restaura de la base de datos a concluido con éxito')
             

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
