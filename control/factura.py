import sys
import base64
from traceback import print_tb
from PyQt6.QtCore import QRegularExpression, QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap, QRegularExpressionValidator, QTextDocument

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QLineEdit, QTableView, QTableWidget, QTableWidgetItem, QTextEdit
from numpy import number
from vista.Ui_Factura import *
from control.buscarcliente import *
from control.buscarinventario import *
from control.notafactura import *
from funciones.visuales import Tablas
from modelo.modFactura import mFactura, eFactura
from modelo.modEquipo import mEquipo, eEquipo
from modelo.modUsuario import mUsuario, eUsuario
from modelo.modCliente import mCliente, eCliente
from modelo.modFichaCliente import mFichaCliente, eFichaCliente
from modelo.modInventario import mInventario, eInventario
from modelo.modFacturaDesglose import mFacturaDesglose, eFacturaDesglose
from modelo.modServicio import mServicio, eServicio
from modelo.modRecepcion import mRecepcion, eRecepcion
from modelo.modDuenno import mDuenno, eDuenno
from modelo.modTaller import mTaller, eTaller
from modelo.modCargo import mCargo, eCargo
from modelo.modUnidadMedida import mUnidadMedida, eUnidadMedida
from funciones.generales import FuncionesGenerales
from funciones.misObjetos import QComboReturn, QEditClickable
from funciones.reportes import Reporte
 
class VentanaFactura(QtWidgets.QMainWindow, Ui_VentanaFactura):

    def __init__(self, efactura:eFactura, usuario:eUsuario, parent = None):
        super(VentanaFactura, self).__init__()

        self.efactura = efactura
        self.usuario = usuario
        self.parent = parent 
        self.tablas = Tablas()
        self.mfactura = mFactura()
        self.mequipo = mEquipo()
        self.mservicio = mServicio()
        self.mcliente = mCliente()
        self.minventario = mInventario()
        self.mfichacliente = mFichaCliente()
        self.mfacturadesglose = mFacturaDesglose()
        self.mrecepcion =mRecepcion()
        self.mduenno = mDuenno()
        self.mtaller = mTaller()
        self.mcargo = mCargo()
        self.mumedida = mUnidadMedida()
        self.generales = FuncionesGenerales()
        self.reporte = Reporte()
        self.servicios = list()
        self.listaeliminados = list()
        self.fichacliente = list()
        self.moneda = 0
        self.sigla = ' CUP'

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaFactura.__init__(self)
        self.setupUi(self)

    def contexMenuEvent(self, pos):    
        self.tableFactura.clicked
        menuTabla = QtWidgets.QMenu(self)
        menuTabla.addAction(self.actionAdd)
        menuTabla.addAction(self.actionDelete)
        menuTabla.addAction(self.actionSave)
        menuTabla.addAction(self.actionPrint)
        menuTabla.addAction(self.actionNota)

        menuTabla.exec(self.tableFactura.mapToGlobal(pos))

    def verificarLicencia(self):
        taller = self.mtaller.cargarValorTaller()
        duenno = self.mduenno.cargarDatosDuenno()
        if taller.getLicencia() != "" and self.generales.verificarLicencia(taller, duenno, taller.getLicencia()):
            return True
        else:
            return False

    def inicializarVentana(self, ventana):
        self.tableFactura.setEnabled(False)
        self.actionMoneda.setEnabled(False)
        self.actionAdd.setEnabled(False)
        self.actionDelete.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.actionPrint.setEnabled(False)
        self.actionNota.setEnabled(False)
        self.actionNota.setToolTip("Comentarios:")
        self.listaServicios()
        # aqui verifico si es una factura nueva
        if self.efactura.getIdFactura() == "":
            self.actionPrint.setEnabled(False)        
            fecha = self.generales.fechaDocumentos()
            numero = 'S/N'
        # aqui editar factura
        else:
            self.actionPrint.setEnabled(self.verificarLicencia())
            cliente = self.efactura.getCliente()
            cliente = self.mcliente.obtenerDatosClientesEspecifica(cliente)
            self.editCliente.setText(str(cliente.getIdCliente()))
            self.labelCliente.setText(cliente.getNombre()) 
            self.labelCliente.setVisible(True)       
            self.llenarCombo(cliente.getIdCliente())
            fichaclienteaux = self.efactura.getFichaCliente()
            fichacliente = self.mfichacliente.obtenerFichaClienteEspecifico(fichaclienteaux)
            textofcliente = fichacliente.getNombre() + ' ' + fichacliente.getApellidos()
            self.generales.comboTextoAnterior(self.comboFichaCliente, textofcliente)
            fecha = self.efactura.getFecha()
            self.moneda = int(self.efactura.getMoneda())
            numero = 'S/N'
            if self.efactura.getNota() != "":
                self.actionNota.setToolTip("Comentarios:\n {}".format(self.efactura.getNota()))
            self.llenadoFacturas()
            #aqui es para si esta eliminada o confirmada no editarla
            if self.efactura.getEstado() == 1:
                self.tableFactura.setEnabled(True)
                self.actionMoneda.setEnabled(True)
                self.actionAdd.setEnabled(True)
                self.actionDelete.setEnabled(True)
                self.actionNota.setEnabled(True)
            else:
                self.tableFactura.setEnabled(False)
                self.editCliente.setEnabled(False)
                self.buttonCliente.setEnabled(False)
                self.comboFichaCliente.setEnabled(False)
        self.iconoMoneda()
        self.editFecha.setText(fecha)
        self.editFactura.setText(numero)
        ventana.setWindowTitle('Factura _ ' + numero)

    # cambio de icono de moneda
    def iconoMoneda(self):
        if self.moneda == 1:
            self.actionMoneda.setIcon(self.icon7)
            self.sigla = ' MLC'            
        else:
            self.actionMoneda.setIcon(self.icon6)
            self.sigla = ' CUP'
                        
    
    #cambio el tipo de moneda al uso
    def cambioMoneda(self):
        if self.moneda == 0:
            self.actionMoneda.setText("Cambiar a CUP")
            self.moneda = 1
        else:
            self.actionMoneda.setText("Cambiar a MLC")
            self.moneda = 0
        self.iconoMoneda()
        self.totalFactura()
                
    #lleno la lista de servicios que utilizare abajo en las lineas de factura
    def listaServicios(self):
        self.servicios.clear()
        servicios = self.mservicio.cargarDatosServicio()
        for serv in servicios:
            if serv.getActivo() == 1:
                self.servicios.append(serv)

    #lleno el combo de las fichas de clientes de la empresa seleccionada
    def llenarCombo(self, idcliente):
        fichas = self.mfichacliente.cargarDatosFichaCliente()
        self.fichacliente.clear()
        self.comboFichaCliente.clear()
        for ficha in fichas:
            if ficha.getCliente() == idcliente:
                self.fichacliente.append(ficha)
                texto = ficha.getNombre() + ' ' + ficha.getApellidos()
                self.comboFichaCliente.addItem(texto)


    def vistaPrevia(self):
        self.reporte.facturaDesglosada(self.efactura, self.usuario, self)


    #aqui comienza la magia de la factura
    def llenadoFacturas(self):
        facturasdesgloses = self.mfacturadesglose.cargarDatosFacturaDesglose()
        for facturadesglose in facturasdesgloses:
            if facturadesglose.getFactura() == self.efactura.getIdFactura():
                self.lineaTablaFactura(facturadesglose)

    # encabezados de la tabla de factura
    def headerTablaFactura(self):        
        self.tablas.headerFactura(0, self.tableFactura)    
        self.tablas.headerFactura(1, self.tableFactura)   
        self.tablas.headerFactura(2, self.tableFactura)   
        self.tablas.headerFactura(3, self.tableFactura)   
        self.tablas.headerFactura(4, self.tableFactura)   
        self.tablas.headerFactura(5, self.tableFactura)  
        self.tablas.headerFactura(6, self.tableFactura)  
        self.tablas.headerFactura(7, self.tableFactura)  
        self.tablas.headerFactura(8, self.tableFactura)  
        self.tablas.headerFactura(9, self.tableFactura)  
        self.tablas.headerFactura(10, self.tableFactura)  

    #verifico si el cliente existe en la tabla 
    def verificarCliente(self):
        buscar = self.editCliente.text()
        if buscar != "":
            if buscar.isdigit(): # en estas 2 lineas compruebo si es entero para saber como buscar
                buscar = int(buscar)

            cliente = self.mcliente.obtenerDatosClientesEspecifica(buscar)
            if cliente.getIdCliente() != "" and cliente.getActivo() != 0:
                self.clienteSeleccionado(cliente)
            else:
                self.buscarCliente()
        else:
            self.buscarCliente()

    # abro la ventana buscar cliente
    def buscarCliente(self):
        self.ventanaBuscarCliente = QtWidgets.QDialog()
        self.ui = VentanaBuscarCliente(self)
        self.ui.setupUi(self.ventanaBuscarCliente) 
        self.ventanaBuscarCliente.exec()

    # paso datos del cliente que halla sido seleccionado
    def clienteSeleccionado(self, cliente:eCliente):
        self.editCliente.setText(str(cliente.getIdCliente()))
        self.labelCliente.setText(cliente.getNombre())
        self.labelCliente.setVisible(True)
        self.tableFactura.setEnabled(True)
        self.actionAdd.setEnabled(True)
        self.tableFactura.clear()
        self.tableFactura.setRowCount(0)
        self.llenarCombo(cliente.getIdCliente())
        facturadesglse = eFacturaDesglose()
        self.actionMoneda.setEnabled(True)
        self.actionNota.setEnabled(True)
        self.lineaTablaFactura(facturadesglse)    

    #coloca los datos del equipo en la factura
    def insertarEquipo(self, einventario:eInventario, edit, fila = None):
        edit.setText(str(einventario.getNoInventario()))
        self.tableFactura.setItem(fila, 9, QTableWidgetItem(str(einventario.getIdInventario())))
        cantidad = int(einventario.getActivo())
        servicio = int(self.tableFactura.item(fila,8).text())
        for i in range(fila):
            if int(einventario.getIdInventario()) == int(self.tableFactura.item(i,9).text()) and servicio == int(self.tableFactura.item(i,8).text()):
                enUso = float(self.tableFactura.cellWidget(i, 5).text())
                cantidad = cantidad - int(round(enUso,0))
        
        self.tableFactura.setItem(fila, 10, QTableWidgetItem(str(cantidad)))

    #creo la linea de la factura
    def lineaTablaFactura(self, efacturadesglse:eFacturaDesglose):
        # creo la fila nueva
        fila = self.generales.insertarFila(self.tableFactura)
        self.actionAdd.setEnabled(False)
        self.actionSave.setEnabled(False)

        #verifico los campos antes de crear nueva linea
        def verificarCampos():
            if comboTipo.currentIndex() == 0 and (editCantidad.text() == "" or editEquipo.text() == "" or editImporte.text() == "" or editPrecio.text() == ""):
                self.actionAdd.setEnabled(True)
            elif comboTipo.currentIndex() == 1 and (editCantidad.text() == "0" or editImporte.text() == "0.00" or editPrecio.text() == ""):
                self.actionAdd.setEnabled(True)
            else:
                self.actionAdd.setEnabled(True)
                self.actionDelete.setEnabled(True)
                self.actionSave.setEnabled(True)

        # verifico si se puede crear una linea nueva
        def nuevaLinea():
            if self.actionAdd.isEnabled():
                factura = eFacturaDesglose()
                self.lineaTablaFactura(factura)

        #cambio lo valores de los widgets dependiendo de la fila de factura
        def usoRecepcion():
            if comboTipo.currentIndex() == 0:
                editEquipo.setReadOnly(False)
                buttonEquipo.setEnabled(True)
                editCantidad.setReadOnly(True)
                editCantidad.setText('1')
            else:
                editEquipo.setReadOnly(True)
                buttonEquipo.setEnabled(False)
                editCantidad.setReadOnly(False)
                editCantidad.setText('0')
            editEquipo.clear()
            verificarCampos()
            
        #funcion para determinar el foco despues de servicio dependiendo de si es recepcio o no
        def focusSeleccion(): 
            if comboTipo.currentIndex() == 0:                                 
                cambioFoco(editEquipo)
            else:
                cambioFoco(editCantidad)
                

        # funcion para hacer el cambio de foco de los edit y seleccione el texto completo
        def cambioFoco(widget):
            widget.setFocus()
            widget.selectAll()

        #funcion para buscar el precio del producto
        def precioServicio():
            pos = comboServicio.currentIndex()
            precio = float(self.servicios[pos].getPrecio())
            um = self.servicios[pos].getUnidadMedida()
            um = self.mumedida.obtenerUnaUnidadMedidaEspecifica(um)
            editUM.setText(um.getSigla())
            editPrecio.setText(self.generales.floatToStr(precio))
            self.tableFactura.setItem(fila, 8, QTableWidgetItem(str(self.servicios[pos].getIdServicio())))
            editEquipo.clear()
            calculoImporte()

            equipos = self.mequipo.cargarDatosEquipo()
            if int(self.tableFactura.cellWidget(fila, 1).currentIndex()) == 0:
                for equip in equipos:
                    if equip.getIdEquipo() == self.servicios[pos].getEquipo():
                        if equip.getMultiple() == 1:
                            editCantidad.setReadOnly(False)
                        else:
                            editCantidad.setReadOnly(True)
                        break
            else:
                editCantidad.setReadOnly(False)
                


        #calculo el importe de la fila
        def calculoImporte():            
            aux = editCantidad.text()
            cantidad = 0
            if aux != "":
                cantidad = float(aux)
                           
            aux = editPrecio.text()
            precio = 0
            if aux != "":
                precio = float(aux)         
                
            total = precio * cantidad
            editImporte.setText(self.generales.floatToStr(total))
            self.totalFactura()
            verificarCampos()

        #verificar el inventario del equipo
        def verificarEquipo():
            pos = comboServicio.currentIndex()
            equipo = self.servicios[pos].getEquipo()
            noinventario = editEquipo.text()

            inv =  self.verificarInventarioEquipo(equipo, noinventario)
            if inv != "":
                self.insertarEquipo(inv, editEquipo, self.tableFactura.currentRow())
            else:
                buscarEquipo(equipo)

        # abre la ventana de buscar equipos
        def buscarEquipo(equipo):
            cambioFoco(editPrecio)
            cliente = int(self.editCliente.text())
            self.ventanaBuscarInventario = QtWidgets.QDialog()
            self.ui = VentanaBuscarInventario(cliente, equipo, editEquipo,fila ,self)
            self.ui.setupUi(self.ventanaBuscarInventario) 
            self.ventanaBuscarInventario.exec()

        self.labelTotal.setVisible(True)
        #creo todos los widgets a utilizar
        comboTipo = QComboReturn(self.tableFactura)
        comboServicio = QComboReturn(self.tableFactura)
        editEquipo = QEditClickable(self.tableFactura)
        buttonEquipo = QtWidgets.QToolButton(editEquipo)
        buttonEquipo.setGeometry(QtCore.QRect(121, 1, 27, 26))
        buttonEquipo.setText('...')
        buttonEquipo.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        editUM = QLineEdit(self.tableFactura)
        editUM.setReadOnly(True)
        editCantidad = QLineEdit(self.tableFactura)        
        editPrecio = QLineEdit(self.tableFactura)
        editImporte = QLineEdit(self.tableFactura)
        editImporte.setReadOnly(True)

        #lleno el combo de los tipos y ubico el foco en el 
        comboTipo.addItems(['Recepcionado', 'No Recepcionado'])
        comboTipo.setFocus()

        #lleno el combo de servicios 
        for serv in self.servicios:
            desc = serv.getDescripcion()
            equipo = serv.getEquipo()
            equipo = self.mequipo.obtenerEquipoEspecifico(equipo)
            comboServicio.addItem(desc + ' ' + equipo.getDescripcion())

        #alineo el texto de los edit a la derecha e inicializo algunos campos
        editCantidad.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        editPrecio.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        editImporte.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        editCantidad.setValidator(QRegularExpressionValidator(QRegularExpression("^[0-9]*\.?[0-9]{1,2}")))
        editPrecio.setValidator(QRegularExpressionValidator(QRegularExpression("^[0-9]*\.?[0-9]{1,2}")))
        editCantidad.setReadOnly(True)
        editCantidad.setText('1')
        editPrecio.setText(self.generales.floatToStr(self.servicios[0].getPrecio()))
        editImporte.setText(self.generales.floatToStr(self.servicios[0].getPrecio()))
 
        # si estamos editando...
        fac = efacturadesglse.getIdFacturaDesglose()
        # Carco valores anteriores en caso de ser edición
        if fac != "":
            tipo = efacturadesglse.getTipo()
            servicio = efacturadesglse.getServicio()
            equ = efacturadesglse.getInventario()
            cant = efacturadesglse.getCantidad()
            precio  = efacturadesglse.getPrecio()
            importe = efacturadesglse.getPrecioTotal()

            comboTipo.setCurrentIndex(int(tipo))

            for pos, serv in enumerate(self.servicios):
                if serv.getIdServicio() == servicio:
                    comboServicio.setCurrentIndex(pos)   
                    um = self.mumedida.obtenerUnaUnidadMedidaEspecifica(serv.getUnidadMedida())
                    editUM.setText(um.getSigla())     
            if equ == "":
                equipo = ""
                idequipo = ""
                cantActiva = 0
                editEquipo.setReadOnly(True)
                buttonEquipo.setEnabled(False)
                editCantidad.setReadOnly(False)
            else:
                equipo = self.minventario.obtenerInventarioEspecifico(int(equ))
                idequipo = equipo.getIdInventario()
                cantActiva = equipo.getActivo()
                equipo = equipo.getNoInventario()
                editEquipo.setReadOnly(False)
                buttonEquipo.setEnabled(True)
                equip = self.mequipo.obtenerEquipoEspecifico(equipo)
                if equip.getMultiple() != 1:
                    editCantidad.setReadOnly(False)
                else:
                    editCantidad.setReadOnly(True)
            
            editEquipo.setText(str(equipo))
            editCantidad.setText(str(cant))
            editPrecio.setText(self.generales.floatToStr(precio))
            editImporte.setText(self.generales.floatToStr(importe))
            
            
        else:
            servicio = self.servicios[0].getIdServicio()            
            um = self.servicios[0].getUnidadMedida()
            um = self.mumedida.obtenerUnaUnidadMedidaEspecifica(um)
            idequipo = ""
            cantActiva = 0
            editUM.setText(um.getSigla())

        #coloco lo cada uno de los widgets en la tabla
        self.tableFactura.setItem(fila, 0, QTableWidgetItem(str(fac)))
        self.tableFactura.setCellWidget(fila, 1, comboTipo)
        self.tableFactura.setCellWidget(fila, 2, comboServicio)
        self.tableFactura.setCellWidget(fila, 3, editEquipo)
        self.tableFactura.setCellWidget(fila, 4, editUM)
        self.tableFactura.setCellWidget(fila, 5, editCantidad)
        self.tableFactura.setCellWidget(fila, 6, editPrecio)
        self.tableFactura.setCellWidget(fila, 7, editImporte)
        self.tableFactura.setItem(fila, 8, QTableWidgetItem(str(servicio)))
        self.tableFactura.setItem(fila, 9, QTableWidgetItem(str(idequipo)))
        self.tableFactura.setItem(fila, 10, QTableWidgetItem(str(cantActiva)))

        #eventos de los widgets creados
        comboTipo.currentTextChanged.connect(usoRecepcion)
        comboTipo.returnPressed.connect(comboServicio.setFocus)
        comboServicio.returnPressed.connect(focusSeleccion)
        editEquipo.returnPressed.connect(buttonEquipo.click)
        buttonEquipo.clicked.connect(verificarEquipo)
        editCantidad.returnPressed.connect(lambda:cambioFoco(editPrecio))
        editPrecio.returnPressed.connect(lambda:cambioFoco(editImporte))
        editImporte.returnPressed.connect(nuevaLinea)
        comboServicio.currentTextChanged.connect(precioServicio)
        editCantidad.textChanged.connect(calculoImporte)
        editEquipo.textChanged.connect(verificarCampos)
        editPrecio.textChanged.connect(calculoImporte)
        
        self.totalFactura()
        self.headerTablaFactura()


    def verificarInventarioEquipo(self, equipo, noinventario):
        cliente = int(self.editCliente.text())
        inventarios = self.minventario.cargarDatosInventario()
        for inv in inventarios:
            if inv.getNoInventario() == noinventario and inv.getActivo() != 0 and inv.getEquipo() == equipo:
                recepcion = self.mrecepcion.obtenerRecepcionEspecifico(int(inv.getRecepcion()))
                if recepcion.getEstado() == 2 and recepcion.getCliente() == cliente:
                    return inv
        return ""

    #calcula el valor total de la factura
    def totalFactura(self):
        total = 0
        if self.tableFactura.rowCount() > 0:
            for fila in range(self.tableFactura.rowCount()):
                suma = 0
                aux = self.tableFactura.cellWidget(fila, 7).text()
                if aux != "":
                    suma = float(aux)
                total += suma
        self.labelTotal.setText(self.generales.floatToStr(total)+ self.sigla )

    #guardar factura
    def guardarFactura(self): 
        guardar = ''
        cantidad = 0
        disponible = 0            
        for fila in range(self.tableFactura.rowCount()):   
            cantidad = float(self.tableFactura.cellWidget(fila, 5).text())
            disponible = self.tableFactura.item(fila, 10).text()                  
            if int(round(cantidad,0)) > int(disponible, 10) and int(self.tableFactura.cellWidget(fila, 1).currentIndex()) == 0:
                guardar = int(fila) + 1
                break
            

        if guardar == '':
            efactura = eFactura()
            efactura.setIdFactura(self.efactura.getIdFactura())
            efactura.setNoFactura(self.editFactura.text())
            efactura.setUsuario(self.usuario.getIdUsuario())
            efactura.setCliente(self.editCliente.text())
            pos = self.comboFichaCliente.currentIndex()
            # si ficha de clientes tiene clientes
            if self.fichacliente.__len__() > 0:
                fichacliente = self.fichacliente[pos].getIdFichaCliente()
            # de no haber ficha de cliente guardo vacio
            else:
                fichacliente = ""
            
            efactura.setFichaCliente(fichacliente)
            efactura.setFecha(self.editFecha.text())
            efactura.setTotalFactura(self.labelTotal.text()[:-4])
            efactura.setNota(self.efactura.getNota())
            efactura.setMoneda(self.moneda)
            efactura.setEstado(1)
            
            if efactura.getIdFactura() == "":
                self.mfactura.guardarDatosFactura(efactura)
                aux = self.mfactura.cargarDatosFactura()
                self.efactura = aux[-1]
            else:
                self.mfactura.editarDatosFactura(efactura, 1)
                self.efactura = efactura

            for fila in range(self.tableFactura.rowCount()):
                efacturaDesglose = eFacturaDesglose()
                efacturaDesglose.setIdFacturaDesglose(self.tableFactura.item(fila, 0,).text())
                efacturaDesglose.setFactura(self.efactura.getIdFactura())
                efacturaDesglose.setTipo(int(self.tableFactura.cellWidget(fila, 1).currentIndex()))
                efacturaDesglose.setServicio(self.tableFactura.item(fila, 8).text())
                inventario = self.tableFactura.item(fila, 9).text()
                efacturaDesglose.setInventario(inventario)
                efacturaDesglose.setCantidad(self.tableFactura.cellWidget(fila, 5).text())
                efacturaDesglose.setPrecio(self.tableFactura.cellWidget(fila, 6).text())
                efacturaDesglose.setPrecioTotal(self.tableFactura.cellWidget(fila, 7).text())
                if efacturaDesglose.getIdFacturaDesglose() == "":
                    self.mfacturadesglose.guardarDatosFacturaDesglose(efacturaDesglose)
                    facturadesglose = self.mfacturadesglose.cargarDatosFacturaDesglose()
                    self.tableFactura.setItem(fila, 0, QTableWidgetItem(str(facturadesglose[-1].getIdFacturaDesglose())))
                else:
                    self.mfacturadesglose.editarDatosFacturaDesglose(efacturaDesglose)


            self.actionSave.setEnabled(False)
            self.actionPrint.setEnabled(self.verificarLicencia())
            self.parent.configuracionBotonesMenu(2)
            #elimino columnas retiradas del inventario
            if self.listaeliminados.__len__() > 0:
                for data in self.listaeliminados:
                    self.mfacturadesglose.eliminarDatosFacturaDesglose(int(data))

        else:            
            self.generales.mensageInformacion("informacion", 
                                "Error al guardar la factura",
                                "Está intentando facturar productos sin existencia. En la fila No. {} está facturando {} y solo tiene {} en recepción".format(guardar, cantidad, disponible))

    # agregar nota a la factura
    def notaFactura(self):
        self.ventanaNotaFactura = QtWidgets.QDialog()
        self.ui = VentanaNotaFactura(self.efactura.getNota(), self)
        self.ui.setupUi(self.ventanaNotaFactura) 
        self.ventanaNotaFactura.exec()
        
    # obtener nota de la factura
    def obtenerNotaFactura(self, nota):
        self.efactura.setNota(nota)
        self.actionNota.setToolTip("Comentarios:\n {}".format(nota))

    #eliminar campo de la factura
    def eliminarFactura(self):
        fila = self.tableFactura.currentRow()
        if self.tableFactura.item(fila, 0).text() != "":
            self.listaeliminados.append(self.tableFactura.item(fila, 0).text())
        self.generales.eliminarFila(self.tableFactura)
        self.totalFactura()
        
        if self.tableFactura.rowCount() > 0:
            self.actionDelete.setEnabled(True)
            self.actionSave.setEnabled(True)
            self.actionAdd.setEnabled(True)

        elif self.tableFactura.rowCount() == 0:
            self.actionAdd.setEnabled(True)
            self.actionDelete.setEnabled(False) 
            self.actionSave.setEnabled(False)

        else:
            self.actionDelete.setEnabled(False) 
            self.actionSave.setEnabled(False)
            self.actionAdd.setEnabled(False)

        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaFactura()
    ventana.show()
    sys.exit(app.exec())
