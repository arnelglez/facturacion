from datetime import datetime
from entidades.entUsuario import eUsuario
import sys
from PyQt6.QtCore import QRegularExpression, QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap, QRegularExpressionValidator

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Cobro import *
from control.buscarcliente import *
from control.buscarfactura import *
from modelo.modDuenno import mDuenno, eDuenno
from modelo.modTaller import mTaller, eTaller
from modelo.modCobro import mCobro, eCobro
from modelo.modCobroFactura import mCobroFactura, eCobroFactura
from modelo.modFactura import mFactura, eFactura
from modelo.modCliente import mCliente, eCliente
from modelo.modTipoPago import mTipoPago, eTipoPago
from funciones.visuales import Tablas
from funciones.reportes import Reporte
from funciones.misObjetos import QComboReturn, QEditClickable

class VentanaCobro(QtWidgets.QMainWindow, Ui_VentanaCobro):

    def __init__(self, ecobro:eCobro , usuario:eUsuario, parent = None):
        super(VentanaCobro, self).__init__()

        self.ecobro = ecobro
        self.usuario = usuario
        self.parent = parent
        self.mcobro = mCobro()
        self.mcobrofactura = mCobroFactura()
        self.mduenno = mDuenno()
        self.mtaller = mTaller()
        self.mfactura = mFactura()
        self.mclient = mCliente()
        self.mtipopago = mTipoPago()
        self.generales = FuncionesGenerales()
        self.reporte = Reporte()
        self.listaPagos = list()
        self.listaeliminados = list()
        self.tablas = Tablas()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaCobro.__init__(self)
        self.setupUi(self)

    def vistaPrevia(self):
        self.reporte.cobroDesglosado(self.ecobro, self.usuario, self)

    def verificarLicencia(self):
        taller = self.mtaller.cargarValorTaller()
        duenno = self.mduenno.cargarDatosDuenno()
        if taller.getLicencia() != "" and self.generales.verificarLicencia(taller, duenno, taller.getLicencia()):
            return True
        else:
            return False
    
    def contexMenuEvent(self, pos):    
        self.tableCobro.clicked
        menuTabla = QtWidgets.QMenu(self)
        menuTabla.addAction(self.actionAdd)
        menuTabla.addAction(self.actionDelete)
        menuTabla.addAction(self.actionSave)
        menuTabla.addAction(self.actionPrint)

        menuTabla.exec(self.tableCobro.mapToGlobal(pos))

    def inicializacionVentana(self, ventana):
        self.tableCobro.setEnabled(False)
        self.actionAdd.setEnabled(False)
        self.actionDelete.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.labelCliente.setVisible(False)
        self.llenadoCombo()
        # aqui verifico si es un cobro nuevo
        if self.ecobro.getIdCobro() == "":
            cobros = self.mcobro.cargarDatosCobro() 
            #generando el numero del documento
            if cobros.__len__() > 0:
                documento = cobros[-1].getNoCobro()
            else:
                documento = ""
            self.actionPrint.setEnabled(False)        
            fecha = self.generales.fechaDocumentos()
            numero = self.generales.numeroDocumento(documento)
            self.dateFechaEmision.setDate(datetime.strptime(self.generales.fechaDocumentos(), '%d/%m/%Y'))
        # aqui editar cobro
        else:
            self.actionPrint.setEnabled(self.verificarLicencia())
            cliente = self.ecobro.getCliente()
            cliente = self.mclient.obtenerDatosClientesEspecifica(cliente)
            self.editCliente.setText(str(cliente.getIdCliente()))
            self.labelCliente.setText(cliente.getNombre()) 
            self.labelCliente.setVisible(True)       
            fecha = self.ecobro.getFecha()
            numero = str(self.ecobro.getNoCobro())
            self.comboTipoPago()          
            self.editNumero.setText(self.ecobro.getDocumento())
            self.editTotalPago.setText(self.generales.floatToStr(self.ecobro.getTotalCobro()))
            self.dateFechaEmision.setDate(datetime.strptime(self.ecobro.getFechaEmision(), '%d/%m/%Y'))
            self.labelTotal.setText(self.generales.floatToStr(self.ecobro.getTotalCobro()))
            self.labelTotal.setVisible(True)
            self.llenadoCobros()
            #aqui es para si esta eliminada o confirmada no editarla
            if self.ecobro.getEstado() == 1:
                self.tableCobro.setEnabled(True)
                self.actionAdd.setEnabled(True)
                self.actionDelete.setEnabled(True)
            else:
                self.tableCobro.setEnabled(False)
                self.editCliente.setEnabled(False)
                self.buttonCliente.setEnabled(False)
                self.comboPago.setEnabled(False)
                self.editNumero.setEnabled(False)
                self.dateFechaEmision.setEnabled(False)
                self.editTotalPago.setEnabled(False)
                self.actionAdd.setEnabled(False)
                self.actionDelete.setEnabled(False)
                self.actionSave.setEnabled(False)

        self.editFecha.setText(fecha)
        self.editCobro.setText(numero)
        ventana.setWindowTitle('Cobro _ ' + numero)
            
    def llenadoCombo(self):
        pagos = self.mtipopago.cargarDatosTipoPago()
        for pago in pagos:
            self.listaPagos.append(pago)
            self.comboPago.addItem(pago.getDescripcion())

    def comboTipoPago(self):
        for lista in self.listaPagos:
            if lista.getIdTipoPago() == self.ecobro.getTipoPago():
                tipo = lista.getDescripcion()
                self.generales.comboTextoAnterior(self.comboPago, tipo)
                break

    def llenadoCobros(self):
        cobrosfacturas = self.mcobrofactura.cargarDatosCobroFactura()
        for cobrofactura in cobrosfacturas:
            if cobrofactura.getCobro() == self.ecobro.getIdCobro():
                self.lineaTablaCobroFatura(cobrofactura)


    def headerTablaCobro(self):        
        self.tablas.headerCobro(0, self.tableCobro)    
        self.tablas.headerCobro(1, self.tableCobro)   
        self.tablas.headerCobro(2, self.tableCobro)   
        self.tablas.headerCobro(3, self.tableCobro)   
        self.tablas.headerCobro(4, self.tableCobro)   


    def verificarCliente(self):
        buscar = self.editCliente.text()
        if buscar != "":
            if buscar.isdigit(): # en estas 2 lineas compruebo si es entero para saber como buscar
                buscar = int(buscar)

            cliente = self.mclient.obtenerDatosClientesEspecifica(buscar)
            if cliente.getIdCliente() != "" and cliente.getActivo() != 0:
                self.clienteSeleccionado(cliente)
            else:
                self.buscarCliente()
        else:
            self.buscarCliente()

    def buscarCliente(self):
        self.ventanaBuscarCliente = QtWidgets.QDialog()
        self.ui = VentanaBuscarCliente(self)
        self.ui.setupUi(self.ventanaBuscarCliente) 
        self.ventanaBuscarCliente.exec()

    def clienteSeleccionado(self, cliente:eCliente):
        self.editCliente.setText(str(cliente.getIdCliente()))
        self.labelCliente.setText(cliente.getNombre())
        self.labelCliente.setVisible(True)
        self.comboPago.setFocus()

    def verificarDatos(self):
        if self.editCliente.text() != "" and self.editNumero.text() != "" and self.editTotalPago.text() != "":
            self.actionAdd.setEnabled(True)

    def iniciarTablaCobro(self):
        self.tableCobro.setEnabled(True)
        self.tableCobro.setFocus()
        cobrofactura = eCobroFactura()
        self.lineaTablaCobroFatura(cobrofactura)
    
    def facturaSeleccionada(self, efactura:eFactura, editFactura, editImporte, fila):
        self.tableCobro.setItem(fila, 4, QTableWidgetItem(str(efactura.getIdFactura())))
        editFactura.setText(str(efactura.getNoFactura()))
        editImporte.setText(self.generales.floatToStr(efactura.getTotalFactura()))
        self.calculoTotal()


    def calculoTotal(self):
        suma = 0
        for fila in range(self.tableCobro.rowCount()):
            valor = self.tableCobro.cellWidget(fila, 3).text()
            if valor == "":
                suma += 0
            else:
                suma += float(valor)

        self.labelTotal.setText(self.generales.floatToStr(suma))
        self.labelTotal.setVisible(True)

    def lineaTablaCobroFatura(self, ecobrofactura:eCobroFactura):
        # creo la fila nueva
        fila = self.generales.insertarFila(self.tableCobro)
        self.actionAdd.setEnabled(False)
        self.actionSave.setEnabled(False)

        def cambioCombo():
            verificarCampos()
            editFactura.clear()
            if comboTipo.currentIndex() == 0: # pago total
                editFactura.setReadOnly(False)
                buttonFactura.setEnabled(True)
                editImporte.setReadOnly(True)
            elif comboTipo.currentIndex() == 1: # pago parcial
                editFactura.setReadOnly(False)
                buttonFactura.setEnabled(True)
                editImporte.setReadOnly(False)
            else:                             #anticipo
                editFactura.setReadOnly(True)
                buttonFactura.setEnabled(False)
                editImporte.setReadOnly(False)
            

        def returnCombo():
            if editFactura.isReadOnly():
                editImporte.setFocus()
                self.tableCobro.setItem(fila, 4, QTableWidgetItem(''))
            else:
                editFactura.setFocus()
        
        def verificarCampos():
            if comboTipo.currentIndex() < 2 and editFactura.text() != "" and editImporte.text() != "":
                self.actionAdd.setEnabled(True)
                self.actionDelete.setEnabled(True)
                self.actionSave.setEnabled(True)
            elif comboTipo.currentIndex() == 2 and editImporte.text() != "":
                self.actionAdd.setEnabled(True)
                self.actionDelete.setEnabled(True)
                self.actionSave.setEnabled(True)
            else:
                self.actionAdd.setEnabled(False)
            self.calculoTotal()
            if editFactura.isReadOnly():
                self.tableCobro.setItem(fila, 4, QTableWidgetItem(''))

        # verifico si se puede crear una linea nueva
        def nuevaLinea():
            if self.actionAdd.isEnabled():
                ecfactura = eCobroFactura()
                self.lineaTablaCobroFatura(ecfactura)

        #verificar el numero de la factura
        def verificarFactura():
            nofactura = editFactura.text()
            buscar = True
            facturas =  self.mfactura.cargarDatosFactura()
            if facturas.__len__() > 0:
                for fac in facturas:
                    if fac.getNoFactura() == nofactura and fac.getCliente == self.editCliente.text() and fac.getEstado == 1:
                        self.tableCobro.setItem(fila, 4, QTableWidgetItem(str(fac.getIdFactura())))
                        buscar = False
                        break

            if buscar == True:
                buscarFactura()

        # abre la ventana de buscar equipos
        def buscarFactura():
            editImporte.setFocus()
            cliente = int(self.editCliente.text())
            self.ventanaBuscarFactura = QtWidgets.QDialog()
            self.ui = VentanaBuscarFactura(cliente, editFactura, editImporte, fila, self)
            self.ui.setupUi(self.ventanaBuscarFactura) 
            self.ventanaBuscarFactura.exec()


        comboTipo = QComboReturn(self.tableCobro)
        editFactura = QEditClickable(self.tableCobro)
        buttonFactura = QtWidgets.QToolButton(editFactura)
        buttonFactura.setGeometry(QtCore.QRect(231, 1, 27, 26))
        buttonFactura.setText('...')
        buttonFactura.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        editImporte = QEditClickable(self.tableCobro)
        editImporte.setValidator(QRegularExpressionValidator(QRegularExpression("^[0-9]*\.?[0-9]{1,2}")))

        comboTipo.addItems(['Total', 'Parcial', 'Anticipado'])

        idcobrofactura = str(ecobrofactura.getIdCobroFactura())
        if idcobrofactura == "": # es nuevo por lo que todo inicia en blanco

            editFactura.setReadOnly(False)
            buttonFactura.setEnabled(True)
            editImporte.setReadOnly(True)
            editImporte.setText('0.00')
        else: # vamos a editar por lo que se cargan los valores anteriores
            comboTipo.setCurrentIndex(int(ecobrofactura.getTipo()))
            factura = ecobrofactura.getFactura()
            factura = self.mfactura.obtenerFacturaEspecifico(factura)
            editFactura.setText(factura.getNoFactura())

            editImporte.setText(self.generales.floatToStr(ecobrofactura.getMonto()))        
            self.tableCobro.setItem(fila, 4, QTableWidgetItem(str(factura.getIdFactura())))

        self.tableCobro.setItem(fila, 0, QTableWidgetItem(idcobrofactura))
        self.tableCobro.setCellWidget(fila, 1, comboTipo)
        self.tableCobro.setCellWidget(fila, 2, editFactura)
        self.tableCobro.setCellWidget(fila, 3, editImporte)


        comboTipo.setFocus()
        comboTipo.currentIndexChanged.connect(cambioCombo)
        editFactura.textChanged.connect(verificarCampos)
        editImporte.textChanged.connect(verificarCampos)
        comboTipo.returnPressed.connect(returnCombo)
        editFactura.returnPressed.connect(buttonFactura.click)
        editImporte.returnPressed.connect(nuevaLinea)
        buttonFactura.clicked.connect(verificarFactura)

        self.headerTablaCobro()

    def guardarCobro(self):
        if float(self.editTotalPago.text()) != float(self.labelTotal.text()):                   
            self.generales.mensageInformacion("error",
                                "Error en el documento",
                                "El Monto del {} no puede ser diferente al total de las facturas asociadas ".format(self.comboPago.currentText()))
        else:
            ecobro = eCobro()
            ecobro.setIdCobro(self.ecobro.getIdCobro())
            ecobro.setCliente((self.editCliente.text()))
            ecobro.setNoCobro(self.editCobro.text())
            ecobro.setDocumento(self.editNumero.text())
            # para el tipo de documento de pago
            pos = self.comboPago.currentIndex()
            ecobro.setTipoPago(self.listaPagos[pos].getIdTipoPago())
            ecobro.setFecha(self.editFecha.text())
            ecobro.setUsuario(self.usuario.getIdUsuario())
            ecobro.setTotalCobro(self.editTotalPago.text())
            ecobro.setEstado(1)
            ecobro.setFechaEmision(self.dateFechaEmision.text())
            if ecobro.getIdCobro() == "":
                self.mcobro.guardarDatosCobro(ecobro)
                aux = self.mcobro.cargarDatosCobro()
                self.ecobro = aux[-1]
            else:
                self.mcobro.editarDatosCobro(ecobro,1)
                self.ecobro = ecobro
            
            #### guardando los documentos seleccionados a confirmar
            for fila in range(self.tableCobro.rowCount()):
                ecobrofactura = eCobroFactura()
                ecobrofactura.setIdCobroFactura(self.tableCobro.item(fila, 0).text())
                ecobrofactura.setCobro(self.ecobro.getIdCobro())
                ecobrofactura.setTipo(self.tableCobro.cellWidget(fila, 1).currentIndex())
                ecobrofactura.setFactura(self.tableCobro.item(fila, 4).text())
                ecobrofactura.setMonto(self.tableCobro.cellWidget(fila, 3).text())
                if ecobrofactura.getIdCobroFactura() == "":
                    self.mcobrofactura.guardarDatosCobroFactura(ecobrofactura)
                    cobrofactura = self.mcobrofactura.cargarDatosCobroFactura()
                    self.tableCobro.setItem(fila, 0, QTableWidgetItem(str(cobrofactura[-1].getIdCobroFactura())))
                else:
                    self.mcobrofactura.editarDatosCobroFactura(ecobrofactura, 1)

        self.actionSave.setEnabled(False)
        self.actionPrint.setEnabled(self.verificarLicencia())
        self.parent.configuracionBotonesMenu(3)
        #elimino columnas retiradas del inventario
        if self.listaeliminados.__len__() > 0:
            for data in self.listaeliminados:
                self.mcobrofactura.eliminarDatosCobroFactura(int(data))

    #eliminar campo del cobro
    def eliminarCobro(self):
        fila = self.tableCobro.currentRow()
        if self.tableCobro.item(fila, 0).text() != "":
            self.listaeliminados.append(self.tableCobro.item(fila, 0).text())
        self.generales.eliminarFila(self.tableCobro)
        
        if self.tableCobro.rowCount() > 0:
            self.actionDelete.setEnabled(True)
            self.actionSave.setEnabled(True)
        else:
            self.actionDelete.setEnabled(False) 
            self.actionSave.setEnabled(False)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaCobro()
    ventana.show()
    sys.exit(app.exec())
