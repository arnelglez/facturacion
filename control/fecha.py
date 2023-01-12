from sqlite3 import Date
import sys
from datetime import date, datetime
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Fecha import *
from modelo.modFecha import mFecha, eFecha
from funciones.generales import FuncionesGenerales


class VentanaFechaProcesamiento(QtWidgets.QMainWindow, Ui_ventanaFechaProcesamiento):

    def __init__(self, parent= None):
        super(VentanaFechaProcesamiento, self).__init__(parent)

        self.parent = parent
        self.generales = FuncionesGenerales()
        self.mfecha = mFecha()
        self.efecha = eFecha()

        QtWidgets.QMainWindow.__init__(self)
        Ui_ventanaFechaProcesamiento.__init__(self)
        self.setupUi(self)
  
  
    def inicializacionVentana(self):
        self.efecha.setIdFecha(self.mfecha.cargarValorFecha().getIdFecha())
        
        if self.generales.fechaDocumentos() == '//':
            self.dateProcesamiento.setDate(datetime.today())
        else:
            self.dateProcesamiento.setDate(datetime.strptime(self.generales.fechaDocumentos(), '%d/%m/%Y'))
            
    def guardarFechaProcesamiento(self, ventana):
        
        if ((datetime.strptime(self.generales.fechaDocumentos(), '%d/%m/%Y') < datetime.strptime(self.dateProcesamiento.text(), '%d/%m/%Y')) or self.generales.fechaDocumentos() == '//'):
            self.efecha.setIdFecha(self.efecha.getIdFecha())
            self.efecha.setFechaProcesamiento(self.dateProcesamiento.text())
            
            self.mfecha.guardarDatosFecha(self.efecha)   
            self.parent.permisosUsuarios()  
            self.generales.cerrarVentana(ventana)
                   
        else:
            self.generales.mensageInformacion("informacion", 
                                "Error de fecha",
                                "la fecha de procesamiento siempre tiene que ser posterior a la usada anteriormente.    ")
  
     
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaFechaProcesamiento()
    ventana.show()
    sys.exit(app.exec())
