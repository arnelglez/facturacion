from datetime import datetime
import sys
from typing import List
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from numpy import real
from modelo.modCobroFactura import mCobroFactura
from modelo.modFecha import mFecha
from vista.consultas.Ui_CargarFacturaCobro import *
from modelo.modCliente import mCliente
from modelo.modFactura import mFactura
from modelo.modCobro import mCobro
from funciones.generales import FuncionesGenerales
from funciones.reportes import Reporte


class VentanaCargarFacturaCobro(QtWidgets.QMainWindow, Ui_VentanaCargarFacturaCobro):

    def __init__(self, titulo = "Facturado"):

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaCargarFacturaCobro.__init__(self)

        self.generales = FuncionesGenerales()
        self.mcliente = mCliente()
        self.mfactura = mFactura()
        self.mcobro = mCobro()
        self.titulo = titulo

        self.clientes = list()
        self.reportes = Reporte()
        
        self.setupUi(self)

    # inicializo la ventaa cargando todos los valores en todos los combos
    def inicializarVentana(self, ventana):
        self.llenarComboClientes()
        self.llenarCamposFechas()
        ventana.setWindowTitle(self.titulo)
        icon = QtGui.QIcon()
        if self.titulo == "Facturado":
            icon.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/facturado.jpeg")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.dateDesde.setEnabled(True)
            self.dateHasta.setEnabled(True)
        elif self.titulo == "Cuentas Cobradas":
            icon.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/cobrado.jpeg")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.dateDesde.setEnabled(True)
            self.dateHasta.setEnabled(True)
        else:
            icon.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/cobrar.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.dateDesde.setEnabled(False)
            self.dateHasta.setEnabled(False)
        ventana.setWindowIcon(icon)
        
    # llenado del combo cliente 
    def llenarComboClientes(self):
        self.clientes.clear()
        self.comboCliente.addItem('                     ---   TODOS   --- ')
        for cliente in self.mcliente.cargarDatosClientes():
            if cliente.getActivo() == 1:
                self.clientes.append(cliente)
                self.comboCliente.addItem(str(cliente.getIdCliente()) + ' - ' + cliente.getNombre())

    # funcion para obtener los datos del nombre que coincida con el combo
    def busquedaPorDescripcion(self, lista, parametro):
        for data in lista:
            if data.getDescripcion() == parametro:
                return data


    def llenarCamposFechas(self):
        if self.titulo == "Cuentas Cobradas":
            fecha = self.mcobro.cargarDatosCobro()   
        else:  
            fecha = self.mfactura.cargarDatosFactura() 

        self.dateDesde.setDate(datetime.strptime(fecha[0].getFecha(), '%d/%m/%Y'))
        self.dateHasta.setDate(datetime.strptime(fecha[fecha.__len__()-1].getFecha(), '%d/%m/%Y'))
                
    def obtenerLista(self, lista):
        listaResultado = list()
        for item in lista:
            if datetime.strptime(self.dateDesde.text(), '%d/%m/%Y') <= datetime.strptime(item.getFecha(), '%d/%m/%Y') <= datetime.strptime(self.dateHasta.text(), '%d/%m/%Y'):
                listaResultado.append(item)
        return listaResultado
        

    def imprimirReporte(self):
        
        if self.dateDesde.date() > self.dateHasta.date():
            self.generales.mensageInformacion('error', 'Error de selcción de fechas', 
                                            'La fecha de inicio no puede ser mayor que la fecha final de la busqueda...')
        else:
            clienteSeleccion = self.comboCliente.currentIndex() -1
            
            listaFacturas = self.obtenerLista(self.mfactura.cargarDatosFactura())
            listaCobros = self.obtenerLista(self.mcobro.cargarDatosCobro())
                    
            data = ''
            total = 0

            if clienteSeleccion >= 0:   
                    
                if self.titulo == "Cuentas Cobradas":
                    titulo = "Cuentas Cobradas de {} desde {} hasta {}".format(self.clientes[clienteSeleccion].getNombre(), self.dateDesde.text(), self.dateHasta.text()) 
                    plantilla = "lista_cobrado.html"
                    formatoTotal = "<tr><td></td><td></td><td></td><td></td><td align='center'><b>{}: {}</b></td></tr>"
                    for cobro in listaCobros:                        
                        if self.clientes[clienteSeleccion].getIdCliente() == cobro.getCliente() and cobro.getEstado() == 2:                             
                            for cobroDesglosado in mCobroFactura().cargarDatosCobroFactura():
                                if cobroDesglosado.getCobro() == cobro.getIdCobro():                    
                                    factura = self.mfactura.obtenerFacturaEspecifico(cobroDesglosado.getFactura())
                                    data += "<tr><td>{}</td><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td></tr>".format(factura.getNoFactura(), factura.getFecha(), cobro.getNoCobro(), cobro.getFecha(), cobroDesglosado.getMonto() )                               
                                    total += float(cobroDesglosado.getMonto())
                            
                else:                    
                    for fac in listaFacturas: 
                        if self.titulo == "Facturado":
                            consulta = fac.getEstado() == 2 or fac.getEstado() == 3 # confirmadas o pagadas
                            titulo = "Facturado a {} desde {} hasta {}".format(self.clientes[clienteSeleccion].getNombre(), self.dateDesde.text(), self.dateHasta.text())
                            plantilla = "lista_facturado.html"
                            formatoTotal = "<tr><td></td><td></td><td align='center'><b>{}: {}</b></td></tr>"
                            
                        else:
                            consulta = fac.getEstado() == 2 # solo confirmadas
                            titulo = "Cuentas por Cobrar de {} desde {} hasta {}".format(self.clientes[clienteSeleccion].getNombre(), self.dateDesde.text(), self.dateHasta.text()) 
                            plantilla = "lista_cobrar.html"
                            formatoTotal = "<tr><td></td><td></td><td></td><td></td><td align='center'><b>{}: {}</b></tr>"
                            
                        if self.clientes[clienteSeleccion].getIdCliente() == fac.getCliente() and consulta:  
                            if self.titulo == "Facturado":                               
                                data += "<tr><td>{}</td><td align='center'>{}</td><td align='center'>{}</td></tr>".format(fac.getNoFactura(), fac.getFecha(), fac.getTotalFactura()) 
                            else:
                                treinta = treintaSesenta = sesentaNoventa = noventa = ""
                                complemento = (datetime.strptime(mFecha().cargarValorFecha().getFechaProcesamiento(), '%d/%m/%Y') - datetime.strptime(fac.getFecha(), '%d/%m/%Y')).days
                            
                                if complemento <= 30:
                                    treinta = fac.getTotalFactura()
                                elif 30 < complemento <= 60:
                                    treintaSesenta = fac.getTotalFactura()
                                elif 60 < complemento <= 90:
                                    sesentaNoventa = fac.getTotalFactura()
                                else:
                                    noventa = fac.getTotalFactura()
                                data += "<tr><td>{}</td><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td></tr>".format(fac.getNoFactura(), treinta, treintaSesenta, sesentaNoventa, noventa)
                            
                            total += float(fac.getTotalFactura())

            else:       
                for cliente in self.clientes:    # recorro la lista de clietes para agrupar las facturas por cada uno de ellos
                    clienteUsado = False  
                    subTotal = 0   
                    
                    
                    if self.titulo == "Cuentas Cobradas":     
                        titulo ="Cuentas Cobradas desde {} hasta {}".format(self.dateDesde.text(), self.dateHasta.text()) 
                        plantilla = "lista_cobrado.html"
                        formatoTotal = "<tr><td></td><td></td><td></td><td></td><td align='center'><b>{}: {}</b></td></tr>"
                        
                        for cobro in listaCobros:                        
                            if cliente.getIdCliente() == cobro.getCliente() and cobro.getEstado() == 2:                             
                                for cobroDesglosado in mCobroFactura().cargarDatosCobroFactura():
                                    if cobroDesglosado.getCobro() == cobro.getIdCobro():                   
                                        if clienteUsado == False: # pequeño aarreglo para poner el nombre del cliente antes de sus facturas 
                                            data += "<tr><td colspan='5'><b>Cliente:    </b>{}</td></tr>".format(cliente.getNombre())
                                            clienteUsado = True   
                                            
                                        factura = self.mfactura.obtenerFacturaEspecifico(cobroDesglosado.getFactura())
                                        data += "<tr><td>{}</td><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td></tr>".format(factura.getNoFactura(), factura.getFecha(), cobro.getNoCobro(), cobro.getFecha(), cobroDesglosado.getMonto() )                             
                                        subTotal += float(cobroDesglosado.getMonto())
                                        total += float(cobroDesglosado.getMonto())
                                    
                                    # arrego para mostrar el sub total de clientes    
                            if cobro.getIdCobro() == listaCobros[listaCobros.__len__() -1].getIdCobro() and subTotal > 0:
                                data += formatoTotal.format("Total cliente", str(subTotal))
                        
                        
                    else:                   
                        for fac in listaFacturas: # recorro las facturas almacenadas en la lista                            
                            if self.titulo == "Facturado":
                                consulta = fac.getEstado() == 2 or fac.getEstado() == 3 # confirmadas o pagadas
                                titulo = "Facturado desde {} hasta {}".format(self.dateDesde.text(), self.dateHasta.text()) 
                                plantilla = "lista_facturado.html"                                
                                formatoTotal = "<tr><td></td><td></td><td align='center'><b>{}: {}</b></td></tr>"
                                
                            else:
                                consulta = fac.getEstado() == 2 # solo confirmadas
                                titulo = "Cuentas por Cobrar desde {} hasta {}".format(self.dateDesde.text(), self.dateHasta.text()) 
                                plantilla = "lista_cobrar.html"
                                formatoTotal = "<tr><td></td><td></td><td></td><td></td><td align='center'><b>{}: {}</b></tr>"
                                
                            if cliente.getIdCliente() == fac.getCliente() and consulta:  # compruebo cliente de lista con el de la factura                    
                                if clienteUsado == False: # pequeño aarreglo para poner el nombre del cliente antes de sus facturas 
                                    if self.titulo == "Facturado":                               
                                        data += "<tr><td colspan='3'><b>Cliente:    </b>{}</td></tr>".format(cliente.getNombre()) 
                                    else:
                                        data += "<tr><td colspan='5'><b>Cliente:    </b>{}</td></tr>".format(cliente.getNombre())
                                    clienteUsado = True                                    
                                if self.titulo == "Facturado":                               
                                    data += "<tr><td>{}</td><td align='center'>{}</td><td align='center'>{}</td></tr>".format(fac.getNoFactura(), fac.getFecha(), fac.getTotalFactura()) 
                                else:
                                    treinta = treintaSesenta = sesentaNoventa = noventa = ""
                                    complemento = (datetime.strptime(mFecha().cargarValorFecha().getFechaProcesamiento(), '%d/%m/%Y') - datetime.strptime(fac.getFecha(), '%d/%m/%Y')).days
                                    if complemento <= 30:
                                        treinta = fac.getTotalFactura()
                                    elif 30 < complemento <= 60:
                                        treintaSesenta = fac.getTotalFactura()
                                    elif 60 < complemento <= 90:
                                        sesentaNoventa = fac.getTotalFactura()
                                    else:
                                        noventa = fac.getTotalFactura()
                                    data += "<tr><td>{}</td><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td></tr>".format(fac.getNoFactura(), treinta, treintaSesenta, sesentaNoventa, noventa)
                            
                                subTotal += float(fac.getTotalFactura())
                                total += float(fac.getTotalFactura())
                                    
                            # arrego para mostrar el sub total de clientes    
                            if fac.getIdFactura() == listaFacturas[listaFacturas.__len__() -1].getIdFactura() and subTotal > 0:
                                data += formatoTotal.format("Total cliente", str(subTotal))
            
            data += formatoTotal.format("TOTAL", str(total))
            self.reportes.listasConfiguraciones(plantilla, data , titulo , self)

    # cerrar la ventana
    def cerrarVentana(self, ventana):
        self.generales.cerrarVentana(ventana)
  
     
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaCargarFacturaCobro()
    ventana.show()
    sys.exit(app.exec())
