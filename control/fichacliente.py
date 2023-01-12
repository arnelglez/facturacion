import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_FichaCliente import *
from modelo.modCargo import mCargo, eCargo
from modelo.modFichaCliente import mFichaCliente, eFichaCliente
from funciones.generales import FuncionesGenerales


class VentanaFichaCliente(QtWidgets.QMainWindow, Ui_VentanaFichaCliente):

    def __init__(self, fichacliente:eFichaCliente, parent = None):
        super(VentanaFichaCliente, self).__init__()

        self.parent = parent
        self.fichacliente = fichacliente
        self.mcargo = mCargo()
        self.mfichacliente = mFichaCliente()
        self.listaCargos = list
        self.generales = FuncionesGenerales()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaFichaCliente.__init__(self)
        self.setupUi(self)
    
    def inicializarVentana(self, ventana):        
        self.llenadoComboCargos()
        if self.fichacliente.getIdFichaCliente() == "": # es porque vamos a insertar nuevo ficha cliente
            ventana.setWindowTitle("Insertar Ficha de Cliente")
        else:
            self.editNombre.setText(self.fichacliente.getNombre())
            self.editApellidos.setText(self.fichacliente.getApellidos())
            self.editCarnet.setText(self.fichacliente.getCarnet())
            cargo = self.fichacliente.getCargo()
            cargo = self.mcargo.obtenerCargoEspecifico(int(cargo))
            self.generales.comboTextoAnterior(self.comboCargo, cargo.getDescripcion())
            ventana.setWindowTitle("Modificar Ficha de Cliente")

    def verificarCampos(self):
        if self.editNombre.text() != "" and self.editApellidos.text() != "" and len(self.editCarnet.text()) == 11:
            self.buttonAceptar.setEnabled(True)
        else:
            self.buttonAceptar.setEnabled(False)

    def llenadoComboCargos(self):
        cargos = self.mcargo.cargarDatosCargo()
        self.comboCargo.clear()
        for cargo in cargos:
            self.comboCargo.addItem(str(cargo.getDescripcion()))

    def guardarFichaCliente(self, ventana):
        fcliente = eFichaCliente()
        fcliente.setIdFichaCliente(self.fichacliente.getIdFichaCliente())
        fcliente.setNombre(self.editNombre.text())
        fcliente.setApellidos(self.editApellidos.text())
        fcliente.setCarnet(self.editCarnet.text())
        fcliente.setCliente(self.fichacliente.getCliente())
        cargo = self.verificarCargo()
        fcliente.setCargo(int(cargo))
        fcliente.setActivo(1)
        if self.fichacliente.getIdFichaCliente() == "":
            self.mfichacliente.guardarDatosFichaCliente(fcliente)        
        else:
            self.mfichacliente.editarDatosFichaCliente(fcliente,1)
        listaFichaCliente = self.mfichacliente.cargarDatosFichaCliente()
        self.parent.llenadoTablaFichaCliente(listaFichaCliente)
        self.generales.cerrarVentana(ventana)
    
    def verificarCargo(self):
        selec = self.comboCargo.currentText()
        cargo = self.mcargo.obtenerCargoEspecifico(selec)
        #si el cargo no esta en la tabla lo agrego
        if cargo.getIdCargo() == '':
            ecargo = eCargo()
            ecargo.setIdCargo("")
            ecargo.setDescripcion(selec)
            self.mcargo.guardarDatosCargo(ecargo)
            cargo = self.mcargo.obtenerCargoEspecifico(selec)
        
        return cargo.getIdCargo()




if __name__ == "__main__":
    app = QtWidgets.QApplication([]) 
    ventana = VentanaFichaCliente()
    ventana.show()
    sys.exit(app.exec())