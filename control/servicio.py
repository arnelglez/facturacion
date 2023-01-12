import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Servicio import *
from modelo.modServicio import mServicio, eServicio
from modelo.modUnidadMedida import mUnidadMedida, eUnidadMedida
from modelo.modEquipo import mEquipo, eEquipo
from funciones.generales import FuncionesGenerales


class VentanaServicio(QtWidgets.QMainWindow, Ui_VentanaServicio):

    def __init__(self, eservicio:eServicio , parent = None):
        super(VentanaServicio, self).__init__()

        self.parent = parent
        self.eservicio = eservicio
        self.mumedida = mUnidadMedida()
        self.mequipo = mEquipo()
        self.mservicio = mServicio()
        self.generales = FuncionesGenerales()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaServicio.__init__(self)
        self.setupUi(self)
    
    #inicializo la ventana con sus primeros valores
    def inicializarVentana(self, ventana):
        self.inicializarEquipo()
        self.inicializarUnidadMedida()

        if self.eservicio.getIdServicio() == "": # insertando nuevo servicio
            ventana.setWindowTitle("Insertar Servicio")
        else:
            self.editDescripcion.setText(self.eservicio.getDescripcion())
            self.editPrecio.setText(self.generales.floatToStr(self.eservicio.getPrecio()))
            equipo = self.mequipo.obtenerEquipoEspecifico(self.eservicio.getEquipo())
            um = self.mumedida.obtenerUnaUnidadMedidaEspecifica(self.eservicio.getUnidadMedida())
            self.generales.comboTextoAnterior(self.comboReparable, equipo.getDescripcion())
            self.generales.comboTextoAnterior(self.comboUM, um.getDescripcion())
            ventana.setWindowTitle("Modificar Servicio")

    #cargo el contenido del combo tipo de equipo
    def inicializarEquipo(self):
        equipos = self.mequipo.cargarDatosEquipo()
        self.comboReparable.clear()
        for equipo in equipos:
            if equipo.getActivo() == 1:
                self.comboReparable.addItem(str(equipo.getDescripcion()))

    #cargo el contenido del combo unidad de medida
    def inicializarUnidadMedida(self):
        unidadesmedida = self.mumedida.cargarDatosUnidadMedida()
        self.comboUM.clear()
        for umedida in unidadesmedida:
            if umedida.getActivo() == 1:
                self.comboUM.addItem(str(umedida.getDescripcion()))
    
    #verifico los campos que esten llenos antes de activar el boton de aceptar
    def verificarCampos(self):
        if self.editDescripcion.text() != "" and self.editPrecio.text() != "":
            self.buttonAceptar.setEnabled(True)
        else:
            self.buttonAceptar.setEnabled(False)

    #guardo el servicio
    def guardarServicio(self, ventana):
        eservicio = eServicio()
        eservicio.setIdServicio(self.eservicio.getIdServicio())
        eservicio.setDescripcion(self.editDescripcion.text())
        eservicio.setPrecio(self.editPrecio.text())
        um = self.verificarUnidadMedida()
        equipo = self.verificarEquipo()
        eservicio.setUnidadMedida(int(um))
        eservicio.setEquipo(int(equipo))
        eservicio.setActivo(1)
        if self.eservicio.getIdServicio() == "":
            self.mservicio.guardarDatosServicio(eservicio)        
        else:
            self.mservicio.editarDatosServicio(eservicio, 1)
        listaServicio = self.mservicio.cargarDatosServicio()
        self.parent.llenadoTablaServicio(listaServicio)
        self.generales.cerrarVentana(ventana)
 

    #convierto el texto a id para insertar el tipo de equipo 
    def verificarEquipo(self):
        selec = self.comboReparable.currentText()
        equipo = self.mequipo.obtenerEquipoEspecifico(selec)
        #si el cargo no esta en la tabla lo agrego
        if equipo.getIdEquipo() == '':
            eequipo = eEquipo()
            eequipo.setIdEquipo("")
            eequipo.setDescripcion(selec)
            self.mequipo.guardarDatosEquipo(eequipo)
            equipo = self.mequipo.obtenerEquipoEspecifico(selec)
        
        return equipo.getIdEquipo()

    def verificarUnidadMedida(self):
        selec = self.comboUM.currentText()
        umedida = self.mumedida.obtenerUnaUnidadMedidaEspecifica(selec)
        
        return umedida.getIdUnidadMedida()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaServicio()
    ventana.show()
    sys.exit(app.exec())
