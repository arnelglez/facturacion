from funciones.generales import FuncionesGenerales
import sys
from PyQt6.QtCore import QSize, QStringListModel
from PyQt6.QtGui import QAbstractFileIconProvider, QIcon, QPixmap

from PyQt6.QtWidgets import QDialog, QFileDialog, QHeaderView, QTableView, QTableWidget, QTableWidgetItem
from vista.Ui_Usuario import *
from modelo.modUsuario import mUsuario, eUsuario
from funciones.generales import FuncionesGenerales


class VentanaUsuario(QtWidgets.QMainWindow, Ui_VentanaUsuario):

    def __init__(self, eusuario:eUsuario, parent = None):
        super(VentanaUsuario, self).__init__()

        self.parent = parent
        self.eusuario = eusuario
        self.musuario = mUsuario()
        self.generales = FuncionesGenerales()

        QtWidgets.QMainWindow.__init__(self)
        Ui_VentanaUsuario.__init__(self)
        self.setupUi(self)

    def inicializarVentana(self, ventana):
        if self.eusuario.getIdUsuario() == "": # es porque vamos a insertar nuevo Usuario
            ventana.setWindowTitle("Insertar Usuario")
        else:
            self.editUsername.setText(self.eusuario.getUsername())
            self.editPasswd.setText(self.eusuario.getPasswd())
            self.editReptPasswd.setText(self.eusuario.getPasswd())
            self.editCarnet.setText(self.eusuario.getCarnet())
            self.editNombre.setText(self.eusuario.getNombre())
            self.editApellidos.setText(self.eusuario.getApellidos())
            ventana.setWindowTitle("Modificar Usuario")

    def verificarUsuario(self):
        result = False
        eusuario = self.musuario.cargarDatosUsuario()
        for usuario in eusuario:
            if usuario.getUsername() == self.editUsername.text():
                result = True
        
        return result


    def guardarUsuario(self, ventana):

        if self.editUsername.text() == "" or self.editNombre.text() == "" or self.editApellidos.text() == "" or self.editCarnet.text() == "" or self.editPasswd.text() == "" or self.editReptPasswd.text() == "":
            self.generales.mensageInformacion('informacion',
                                                'Error de Usuario',
                                                'Debe llenar todos los campos para poder crear el usuario.                 ')

        elif self.editPasswd.text() != self.editReptPasswd.text(): 
            self.generales.mensageInformacion('informacion',
                                                'Error de Contraseña',
                                                'Las contraseñas no coinciden. Rectifíquelas antes de continuar.            ')

        elif len(self.editPasswd.text()) < 8: 
            self.generales.mensageInformacion('informacion',
                                                'Error de Contraseña',
                                                'La contraseña debe tener un mínimo de 8 caracteres.                        ')

        elif len(self.editCarnet.text()) < 11: 
            self.generales.mensageInformacion('informacion',
                                                'Error de Carnel',
                                                'El carnet de identidad es de 11 caracteres.                                ')
        
        else:
        
            usuario = eUsuario()
            usuario.setIdUsuario(self.eusuario.getIdUsuario())
            usuario.setUsername(self.editUsername.text().lower())
            usuario.setPasswd(self.editPasswd.text())
            usuario.setNombre(self.editNombre.text())
            usuario.setApellidos(self.editApellidos.text())
            usuario.setCarnet(self.editCarnet.text())
            usuario.setActivo(1)
            if self.eusuario.getIdUsuario() == "":
                if self.verificarUsuario():
                    self.generales.mensageInformacion('error',
                                                    'Error de Usuario',
                                                    'El usuario que intenta crear ya existe en la base de datos, cree uno nuevo.')
                
                else:
                    self.musuario.guardarDatosUsuario(usuario)
                    aux = self.musuario.cargarDatosUsuario()
                    self.eusuario = aux[-1]
                    self.generales.cerrarVentana(ventana)
                    
            else:
                self.musuario.editarDatosUsuario(usuario, 1)
                self.generales.cerrarVentana(ventana)
            self.parent.inicializarVentana()



if __name__ == "__main__": 
    app = QtWidgets.QApplication([])
    ventana = VentanaUsuario()
    ventana.show()
    sys.exit(app.exec())