import sys
from PyQt6 import QtWidgets
from vista.Ui_Inicio import Ui_ventanaInicioSession
from control.principal import *
from modelo.modUsuario import mUsuario
from funciones.tallerDB import BaseDatos

class VentanaInicio(QtWidgets.QMainWindow, Ui_ventanaInicioSession):


    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_ventanaInicioSession.__init__(self)
        self.muser = mUsuario()
        self.data = BaseDatos() 
        self.generales = FuncionesGenerales()
        self.data.__init__()
        self.data.__del__() 
        self.setupUi(self)

    def inicioSession(self,ventana):
        user = self.editUsuario.text().lower() 
        passwd = self.editPass.text()

        usuario = self.muser.verificarUsuario(user, passwd)   

        if usuario.getIdUsuario() == '':     
            self.generales.mensageInformacion("informacion", 
                                "Error de usuario",
                                "El usuario o contraseña no son correctos.                ")

            self.editUsuario.clear()
            self.editPass.clear()
        else:
    

            self.MainWindow = QtWidgets.QMainWindow()
            self.ui = VentanaPrincipal(usuario)
            self.ui.setupUi(self.MainWindow) 
            self.MainWindow.show()
            self.generales.cerrarVentana(ventana) 
                 

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ventana = VentanaInicio()
    ventana.show()
    sys.exit(app.exec())
