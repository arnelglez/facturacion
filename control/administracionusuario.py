import sys
from PyQt6.QtCore import QByteArray, QSize, QStringListModel, Qt
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap, QScreen


from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QMessageBox, QTableView, QTableWidget, QTableWidgetItem, QToolBar
from PyQt6.QtPrintSupport import QPrintPreviewDialog, QPrinter
from vista.Ui_AdministracionUsuario import *
from control.usuario import *
from modelo.modUsuario import mUsuario, eUsuario
from funciones.generales import FuncionesGenerales
from funciones.visuales import Tablas
from funciones.reportes import Reporte


class VentanaAdministracionUsuario(QtWidgets.QMainWindow, Ui_VentanaAdministracionUsuario):

    def __init__(self, parent= None):
        super(VentanaAdministracionUsuario, self).__init__(parent)

        self.musuario = mUsuario()
        self.generales = FuncionesGenerales()
        self.tablas = Tablas()
        self.users = ""
        self.reporte = Reporte()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaAdministracionUsuario.__init__(self)
        self.setupUi(self)
    
    def contexMenuEvent(self, pos):    
        self.usuarioSeleccionado()
        menuTabla = QtWidgets.QMenu(self)
        menuTabla.addAction(self.actionAdd)
        menuTabla.addAction(self.actionDelete)
        menuTabla.addAction(self.actionEdit)
        menuTabla.addAction(self.actionPrint)

        menuTabla.exec(self.tableUsuario.mapToGlobal(pos))

    def inicializarVentana(self):
        self.tableUsuario.clear()
        self.tableUsuario.setRowCount(0)
        self.headerTablaUsuario()
        usuarios = self.musuario.cargarDatosUsuario()
        self.users = ""
        for fila, usuario in enumerate(usuarios):
            self.tableUsuario.insertRow(fila)
            self.tableUsuario.setItem(fila, 0, QTableWidgetItem(str(usuario.getIdUsuario())))
            self.tableUsuario.setItem(fila, 1, QTableWidgetItem(str(usuario.getUsername())))
            self.tableUsuario.setItem(fila, 2, QTableWidgetItem(str(usuario.getNombre() + ' ' + usuario.getApellidos())))
            self.tableUsuario.setItem(fila, 3, QTableWidgetItem(str(usuario.getCarnet())))
            self.tableUsuario.setItem(fila, 4, QTableWidgetItem(str(usuario.getActivo())))
            if usuario.getActivo() == 0:
                self.tableUsuario.setRowHidden(fila, True)
            else:
                self.users += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(usuario.getUsername(), usuario.getNombre() + ' ' + usuario.getApellidos(), usuario.getCarnet()) 

        self.actionEdit.setEnabled(False)
        self.actionDelete.setEnabled(False)

    def vistaPrevia(self):
        self.reporte.listasConfiguraciones('lista_usuarios.html', self.users, 'Lista de Usuarios', self)

    def headerTablaUsuario(self):
        self.tablas.headerListaUsuario(0, self.tableUsuario)    
        self.tablas.headerListaUsuario(1, self.tableUsuario)   
        self.tablas.headerListaUsuario(2, self.tableUsuario)   
        self.tablas.headerListaUsuario(3, self.tableUsuario)  
        self.tablas.headerListaUsuario(4, self.tableUsuario) 

    def usuarioSeleccionado(self):
        if self.tableUsuario.currentRow() != 0:
            self.actionDelete.setEnabled(True)
            self.actionEdit.setEnabled(True)
        else:
            self.actionDelete.setEnabled(False)
            self.actionEdit.setEnabled(False)
    
    ###funcion para crear nuevo usuario
    def nuevoUsuario(self):
        eusurio = eUsuario()
        self.ventanaUsuario = QtWidgets.QDialog()
        self.ui = VentanaUsuario(eusurio, self)
        self.ui.setupUi(self.ventanaUsuario) 
        self.ventanaUsuario.exec() 
    
    ###funcion para editar usuario
    def editarUsuario(self):
        fila = self.tableUsuario.currentRow()
        idusuario = self.tableUsuario.item(fila, 0).text()
        eusurio = self.musuario.obtenerUsuarioEspecifico(idusuario)
        self.ventanaUsuario = QtWidgets.QDialog()
        self.ui = VentanaUsuario(eusurio, self)
        self.ui.setupUi(self.ventanaUsuario) 
        self.ventanaUsuario.exec() 

    def eliminarUsuario(self):
        fila = self.tableUsuario.currentRow()
        idusuario = self.tableUsuario.item(fila,0).text()
        eusuario = self.musuario.obtenerUsuarioEspecifico(int(idusuario))
        if idusuario == 1:              
            self.generales.mensageInformacion("informacion",
                                "Error de usuario",
                                "El usuario seleccionado no puede ser eliminado.                ")
        else:
            resp = self.generales.mensageSiNo("Eliminar Usuario", "El usuario {} va a ser eliminado de la base de datos!".format(eusuario.getUsername()),
                                                    "Desea continuar con el proceso?")
            if resp == 1:
                self.musuario.editarDatosUsuario(eusuario, 0)
                self.generales.eliminarFila(self.tableUsuario)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaAdministracionUsuario()
    ventana.show()
    sys.exit(app.exec())
