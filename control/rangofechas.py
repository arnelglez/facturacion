import sys
from datetime import datetime
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_RangoFechas import *
from funciones.generales import FuncionesGenerales


class VentanaRangoFechas(QtWidgets.QMainWindow, Ui_VentanaRangoFechas):

    def __init__(self, parent= None):
        super(VentanaRangoFechas, self).__init__(parent)

        self.parent = parent
        self.generales = FuncionesGenerales()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaRangoFechas.__init__(self)
        self.setupUi(self)

    #mostrar ventana dependiendo si es edicion o nuevo
    def inicializarVentana(self, ventana):
      self.dateDesde.setDate(datetime.strptime(('1/1/2021'), '%d/%m/%Y'))
      self.dateHasta.setDate(datetime.strptime(self.generales.fechaDocumentos(), '%d/%m/%Y'))

    def rangoSeleccionado(self, ventana):
        if self.dateDesde.date() > self.dateHasta.date():
            self.generales.mensageInformacion('error', 'Error de selcción de fechas', 
                                            'La fecha de inicio no puede ser mayor que la fecha final de la busqueda...')
        else:
            inicio = self.dateDesde.date()
            fin = self.dateHasta.date()
            self.parent.rangoFechas(inicio, fin)
            self.generales.cerrarVentana(ventana)

    def cerrarVentana(self, ventana):
        self.parent.rangoCancelado()
        self.generales.cerrarVentana(ventana)

  
     
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaRangoFechas()
    ventana.show()
    sys.exit(app.exec())
