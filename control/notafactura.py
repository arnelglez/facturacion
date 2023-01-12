
import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_NotaFactura import *
from funciones.generales import FuncionesGenerales

class VentanaNotaFactura(QtWidgets.QMainWindow, Ui_VentanaNotaFactura):

    def __init__(self, nota ,parent = None):
        super(VentanaNotaFactura, self).__init__()

        self.parent = parent
        self.nota = nota
        self.generales = FuncionesGenerales()
        
        
        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaNotaFactura.__init__(self)
        self.setupUi(self)
        
        
    def inicializarVentana(self):
        self.textEditNota.setPlainText(self.nota)
        
    def guardarNota(self, ventana):
        self.parent.obtenerNotaFactura(self.textEditNota.toPlainText())  
        self.generales.cerrarVentana(ventana)

   
    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])  
    ventana = VentanaNotaFactura()
    ventana.show()
    sys.exit(app.exec())