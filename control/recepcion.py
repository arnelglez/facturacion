from entidades.entUsuario import eUsuario
import sys

from PyQt6.QtCore import QRegularExpression, QSize, QStringListModel, Qt
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QKeyEvent, QPixmap, QRegularExpressionValidator

from PyQt6.QtWidgets import QComboBox, QDialog, QFileDialog, QHeaderView, QLabel, QLineEdit, QTableView, QTableWidget, QTableWidgetItem, QTextEdit, QWidget
from vista.Ui_Recepcion import *
from control.buscarcliente import *
from funciones.misObjetos import QComboReturn
from funciones.visuales import Tablas
from funciones.generales import FuncionesGenerales
from modelo.modDuenno import mDuenno, eDuenno
from modelo.modTaller import mTaller, eTaller
from modelo.modCliente import mCliente, eCliente
from modelo.modRecepcion import mRecepcion, eRecepcion
from modelo.modInventario import mInventario, eInventario
from modelo.modEquipo import mEquipo, eEquipo
from modelo.modMarca import mMarca, eMarca
from modelo.modModelo import mModelo, eModelo
from funciones.reportes import Reporte


class VentanaRecepcion(QtWidgets.QMainWindow, Ui_VentanaRecepcion):

    def __init__(self, erecepcion:eRecepcion ,usuario: eUsuario, parent = None):
        super(VentanaRecepcion, self).__init__()

        self.erecepcion = erecepcion
        self.usuario = usuario
        self.parent = parent
        self.generales = FuncionesGenerales()
        self.mduenno = mDuenno()
        self.mtaller = mTaller()
        self.mclient = mCliente()
        self.mrecepcion = mRecepcion()
        self.minventario = mInventario()
        self.mequipo = mEquipo()
        self.mmarca = mMarca()
        self.mmodelo = mModelo()
        self.tablas = Tablas()
        self.reporte = Reporte()
        self.listaeliminados = list()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaRecepcion.__init__(self)
        self.setupUi(self)
    
    def contexMenuEvent(self, pos):    
        self.tableRecepcion.clicked
        menuTabla = QtWidgets.QMenu(self)
        menuTabla.addAction(self.actionAdd)
        menuTabla.addAction(self.actionDelete)
        menuTabla.addAction(self.actionSave)
        menuTabla.addAction(self.actionPrint)

        menuTabla.exec(self.tableRecepcion.mapToGlobal(pos))

    def vistaPrevia(self):
        self.reporte.recepcionDesglosada(self.erecepcion, self.usuario, self)

    def verificarLicencia(self):
        taller = self.mtaller.cargarValorTaller()
        duenno = self.mduenno.cargarDatosDuenno()
        if taller.getLicencia() != "" and self.generales.verificarLicencia(taller, duenno, taller.getLicencia()):
            return True
        else:
            return False

    def inicializacionVentana(self, ventana):
        self.tableRecepcion.setEnabled(False)
        self.actionAdd.setEnabled(False)
        self.actionDelete.setEnabled(False)
        self.actionSave.setEnabled(False)
        # aqui verifico si es una recepcion nueva
        if self.erecepcion.getIdRecepcion() == "":
            recepciones = self.mrecepcion.cargarDatosRecepcion() 
            #generando el numero del documento
            if recepciones.__len__() > 0:
                documento = recepciones[-1].getNoRecepcion()
            else:
                documento = ""
            self.actionPrint.setEnabled(False)        
            fecha = self.generales.fechaDocumentos()
            numero = self.generales.numeroDocumento(documento)
        # aqui editar recepcion
        else:
            self.actionPrint.setEnabled(self.verificarLicencia())
            cliente = self.erecepcion.getCliente()
            cliente = self.mclient.obtenerDatosClientesEspecifica(cliente)
            self.editCliente.setText(str(cliente.getIdCliente()))
            self.labelCliente.setText(cliente.getNombre()) 
            self.labelCliente.setVisible(True)       
            fecha = self.erecepcion.getFecha()
            numero = str(self.erecepcion.getNoRecepcion())
            self.llenadoRecepciones()
            #aqui es para si esta eliminada o confirmada no editarla
            if self.erecepcion.getEstado() == 1:
                self.tableRecepcion.setEnabled(True)
            else:
                self.tableRecepcion.setEnabled(False)
                self.editCliente.setEnabled(False)
                self.buttonCliente.setEnabled(False)
                self.actionAdd.setEnabled(False)
                self.actionDelete.setEnabled(False)
                self.actionSave.setEnabled(False)

        self.editFecha.setText(fecha)
        self.editRecepcion.setText(numero)
        ventana.setWindowTitle('Recepción _ ' + numero)
            

    def llenadoRecepciones(self):
        inventarios = self.minventario.cargarDatosInventario()
        for inventario in inventarios:
            if inventario.getRecepcion() == self.erecepcion.getIdRecepcion():
                self.lineaTablaInventario(inventario)


    def headerTablaRecepcion(self):        
        self.tablas.headerRecepcion(0, self.tableRecepcion)    
        self.tablas.headerRecepcion(1, self.tableRecepcion)   
        self.tablas.headerRecepcion(2, self.tableRecepcion)   
        self.tablas.headerRecepcion(3, self.tableRecepcion)   
        self.tablas.headerRecepcion(4, self.tableRecepcion)   
        self.tablas.headerRecepcion(5, self.tableRecepcion)  
        self.tablas.headerRecepcion(6, self.tableRecepcion)  


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
        self.tableRecepcion.setEnabled(True)
        self.actionAdd.setEnabled(True)
        self.tableRecepcion.clear()
        self.tableRecepcion.setRowCount(0)
        inventario = eInventario()
        self.lineaTablaInventario(inventario)

    # 
    def lineaTablaInventario(self, einventario:eInventario):    

        # creo la fila nueva
        fila = self.generales.insertarFila(self.tableRecepcion)
        self.actionAdd.setEnabled(False)
        self.actionSave.setEnabled(False)

        def verificarCampos():
            if comboEquipo.currentText() != "" and editNoInventario.text() != "" and editCantidad.text() != "":
                self.actionAdd.setEnabled(True)
                self.actionDelete.setEnabled(True)
                self.actionSave.setEnabled(True)
            else:
                self.actionAdd.setEnabled(False)
                self.actionSave.setEnabled(False)       

        # verifico si se puede crear una linea nueva
        def nuevaLinea():
            if self.actionAdd.isEnabled():
                inventario = eInventario()
                self.lineaTablaInventario(inventario)                        
        
        # creo los widgets que voy a ubicar en la tabla
        editNoInventario = QLineEdit(self.tableRecepcion)
        comboEquipo = QComboReturn(self.tableRecepcion)
        comboMarca = QComboReturn(self.tableRecepcion)
        comboModelo = QComboReturn(self.tableRecepcion) 
        editCantidad = QLineEdit(self.tableRecepcion)
        editObservaciones = QLineEdit(self.tableRecepcion)        
        editCantidad.setValidator(QRegularExpressionValidator(QRegularExpression("^[0-9]*\.?[0-9]{1,2}")))
        editCantidad.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)

        #inicializo los combo
        editNoInventario.setFocus()
        
        #### cargar lista de equipos
        self.cargarEquipos(comboEquipo)
        
        #### cargar modelos de equipo
        multiple = False

        def controlEquipo():            
            selec = comboEquipo.currentText()
            equip = self.mequipo.obtenerEquipoEspecifico(selec).getMultiple()            
            editCantidad.setText("1")
            if equip == True:
                editCantidad.setReadOnly(False)
            else:
                editCantidad.setReadOnly(True)

        comboEquipo.currentTextChanged.connect(controlEquipo)
        comboEquipo.currentTextChanged.connect(lambda:self.cargarMarcas(comboMarca,self.seleccionEquipo(comboEquipo)))
        
        comboMarca.clicked.connect(lambda:self.cargarMarcas(comboMarca,self.seleccionEquipo(comboEquipo)))
        
        comboMarca.currentTextChanged.connect(lambda:self.cargarModelos(comboModelo, self.seleccionEquipo(comboEquipo), self.seleccionMarca(comboMarca)))
        comboModelo.clicked.connect(lambda:self.cargarModelos(comboModelo, self.seleccionEquipo(comboEquipo), self.seleccionMarca(comboMarca)))

        # declaro los combobox editables para que me permita agregar nuevos campos
        comboEquipo.setEditable(True)
        comboMarca.setEditable(True)
        comboModelo.setEditable(True)

        editNoInventario.returnPressed.connect(comboEquipo.setFocus)
        comboEquipo.returnPressed.connect(comboMarca.setFocus)
        comboMarca.returnPressed.connect(comboModelo.setFocus)

        def seleccionOpcional():
            if editCantidad.isReadOnly():
                editObservaciones.setFocus()
            else:
                editCantidad.setFocus()
            editCantidad.returnPressed.connect(editObservaciones.setFocus)

        comboModelo.returnPressed.connect(seleccionOpcional)

        editObservaciones.returnPressed.connect(nuevaLinea)

        #verificando campos que esten llenos
        editNoInventario.textChanged.connect(verificarCampos)
        comboEquipo.editTextChanged.connect(verificarCampos)
        comboMarca.editTextChanged.connect(verificarCampos)
        comboModelo.editTextChanged.connect(verificarCampos)
        editCantidad.textChanged.connect(verificarCampos)
        editObservaciones.textChanged.connect(verificarCampos)
        
        inv = einventario.getIdInventario()
        # Carco valores anteriores en caso de ser edición
        if inv != "":
            
            editNoInventario.setText(str(einventario.getNoInventario()))
            editObservaciones.setText(einventario.getObservaciones())

            equ = self.equipoSeleccionado(einventario.getEquipo())
            mar = self.marcaSeleccionada(einventario.getEquipo(), einventario.getMarca())
            mod = self.modeloSeleccionado(einventario.getEquipo(), einventario.getMarca(), einventario.getModelo())

            if equ == "":
                equipo = equ
            else:
                equipo = equ.getDescripcion()
            
            if mar == "":
                marca = mar
            else:
                marca = mar.getDescripcion()

            if mod == "":
                modelo = mod
            else:
                modelo = mod.getDescripcion()

            self.generales.comboTextoAnterior(comboEquipo, equipo)
            self.generales.comboTextoAnterior(comboMarca, marca)
            self.generales.comboTextoAnterior(comboModelo, modelo)
            editCantidad.setText(str(einventario.getCantidad()))


        self.tableRecepcion.setItem(fila, 0,QTableWidgetItem(str(inv))) 
        self.tableRecepcion.setCellWidget(fila, 1, editNoInventario)
        self.tableRecepcion.setCellWidget(fila, 2, comboEquipo)
        self.tableRecepcion.setCellWidget(fila, 3, comboMarca)
        self.tableRecepcion.setCellWidget(fila, 4, comboModelo)
        self.tableRecepcion.setCellWidget(fila, 5, editCantidad)
        self.tableRecepcion.setCellWidget(fila, 6, editObservaciones)

        self.headerTablaRecepcion()

        
    # Funciones de los campos de la tabla 
    # Funcion para cargar equipos
    def cargarEquipos(self, combo):
        equipos = self.mequipo.cargarDatosEquipo()
        combo.clear()
        for dato in equipos:
            combo.addItem(dato.getDescripcion())

        combo.setCurrentIndex(-1)

    # Funcion para cargar marcas por equipos
    def cargarMarcas(self, combo, equipo):
        marcas = self.mmarca.cargarDatosMarca()
        combo.clear()
        for dato in marcas:
            if dato.getEquipo() == equipo:
                combo.addItem(dato.getDescripcion())
            
        combo.setCurrentIndex(-1)

    # Funcion para cargar modelos por marcas y equipos
    def cargarModelos(self, combo, equipo, marca):
        modelos = self.mmodelo.cargarDatosModelo()
        combo.clear()
        for dato in modelos:
            if dato.getEquipo() == equipo and dato.getMarca() == marca:
                combo.addItem(dato.getDescripcion())
            
        combo.setCurrentIndex(-1)


    def seleccionEquipo(self, combo):
        selec = combo.currentText()
        equip = self.mequipo.obtenerEquipoEspecifico(selec)        
        return equip.getIdEquipo()        

    def equipoSeleccionado(self, equipo):
        result = self.mequipo.obtenerEquipoEspecifico(equipo)
        #si el equipo no esta en la tabla lo agrego
        if result.getIdEquipo() == '':
            eequipo = eEquipo()
            eequipo.setIdEquipo(-1)
            eequipo.setDescripcion(equipo)
            self.mequipo.guardarDatosEquipo(eequipo)
            result = self.mequipo.obtenerEquipoEspecifico(equipo)
        
        return result

    def seleccionMarca(self, combo):
        selec = combo.currentText()
        marc = self.mmarca.obtenerMarcaEspecifico(selec)
        return marc.getIdMarca()

    def marcaSeleccionada(self, equipo, marca):
        if marca == '':
            result = marca
        else:
            result = self.mmarca.obtenerMarcaEspecifico(marca)
            #si la marca no esta en la tabla lo agrego
            if result.getIdMarca() == '':
                emarca = eMarca()
                emarca.setIdMarca(-1)
                emarca.setDescripcion(marca)
                emarca.setEquipo(equipo)
                self.mmarca.guardarDatosMarca(emarca)
                result = self.mmarca.obtenerMarcaEspecifico(marca)

        return result
    
    def seleccionModelo(self, combo):
        selec = combo.currentText()
        model = self.mmodelo.obtenerModeloEspecifico(selec)
        return model.getIdModelo()
        
    def modeloSeleccionado(self, equipo, marca, modelo):
        if modelo == '':
            result = modelo
        else:
            result = self.mmodelo.obtenerModeloEspecifico(modelo)
            #si la modelo no esta en la tabla lo agrego
            if result.getIdModelo() == '':
                emodelo = eModelo()
                emodelo.setIdModelo(-1)
                emodelo.setDescripcion(modelo)
                emodelo.setEquipo(equipo)
                emodelo.setMarca(marca)
                self.mmodelo.guardarDatosModelo(emodelo)
                result = self.mmodelo.obtenerModeloEspecifico(modelo)
        
        return result


    def guardarRecepcion(self): 
        erecepcion = eRecepcion()
        erecepcion.setIdRecepcion(self.erecepcion.getIdRecepcion())
        erecepcion.setNoRecepcion(self.editRecepcion.text())
        erecepcion.setFecha(self.editFecha.text())
        erecepcion.setCliente(self.editCliente.text())
        erecepcion.setUsuario(self.usuario.getIdUsuario())
        erecepcion.setEstado(1)
        if erecepcion.getIdRecepcion() == '':
            self.mrecepcion.guardarDatosRecepcion(erecepcion)
            aux = self.mrecepcion.cargarDatosRecepcion()
            self.erecepcion = aux[-1]
        else:
            self.mrecepcion.editarDatosRecepcion(erecepcion,1)
            self.erecepcion = erecepcion

        # en este siclo guardo los inventarios
        for fila in range(self.tableRecepcion.rowCount()):
            einventario = eInventario()
            equipo = self.equipoSeleccionado(self.tableRecepcion.cellWidget(fila, 2).currentText())
            m = self.marcaSeleccionada(equipo.getIdEquipo() , self.tableRecepcion.cellWidget(fila, 3).currentText())
            if m == "":
                marca = m
            else:
                marca = m.getIdMarca()
            m = self.modeloSeleccionado(equipo.getIdEquipo(), marca ,self.tableRecepcion.cellWidget(fila, 4).currentText())
            if m == "":
                modelo = m
            else:
                modelo = m.getIdModelo()
            cantidad = self.tableRecepcion.cellWidget(fila, 5).text()
            observaciones = self.tableRecepcion.cellWidget(fila, 6).text()
            einventario.setIdInventario(self.tableRecepcion.item(fila,0).text())
            einventario.setNoInventario(self.tableRecepcion.cellWidget(fila, 1).text())
            einventario.setEquipo(equipo.getIdEquipo())
            einventario.setMarca(marca)
            einventario.setCantidad(cantidad)
            einventario.setModelo(modelo)
            einventario.setObservaciones(observaciones)
            einventario.setRecepcion(self.erecepcion.getIdRecepcion())
            einventario.setActivo(cantidad)

            if einventario.getIdInventario() == "":
                self.minventario.guardarDatosInventario(einventario)
                inventario = self.minventario.cargarDatosInventario()
                self.tableRecepcion.setItem(fila, 0, QTableWidgetItem(str(inventario[-1].getIdInventario())))
            else:
                self.minventario.editarDatosInventario(einventario, cantidad)            
        
        self.actionSave.setEnabled(False)
        self.actionPrint.setEnabled(self.verificarLicencia())
        self.parent.configuracionBotonesMenu(1)
        #elimino columnas retiradas del inventario
        if self.listaeliminados.__len__() > 0:
            for data in self.listaeliminados:
                self.minventario.eliminarDatosInventario(int(data))
                


    def eliminarRecepcion(self):
        fila = self.tableRecepcion.currentRow()
        if self.tableRecepcion.item(fila, 0).text() != "":
            self.listaeliminados.append(self.tableRecepcion.item(fila, 0).text())
        self.generales.eliminarFila(self.tableRecepcion)
        if self.tableRecepcion.rowCount() > 0:
            self.actionDelete.setEnabled(True)
            self.actionSave.setEnabled(True)
        else:
            self.actionDelete.setEnabled(False) 
            self.actionSave.setEnabled(False)
        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaRecepcion()
    ventana.show()
    sys.exit(app.exec())
