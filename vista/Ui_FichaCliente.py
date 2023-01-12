# Form implementation generated from reading ui file 'fichacliente.ui'
#
# Created by: PyQt6 UI code generator 6.1.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_VentanaFichaCliente(object):
    def setupUi(self, ventanaFichaCliente):
        ventanaFichaCliente.setObjectName("ventanaFichaCliente")
        ventanaFichaCliente.resize(372, 252)
        ventanaFichaCliente.setMinimumSize(QtCore.QSize(372, 252))
        ventanaFichaCliente.setMaximumSize(QtCore.QSize(372, 252))

        #########pocisionar ventana centrada#####
        qr = ventanaFichaCliente.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        ventanaFichaCliente.move(qr.topLeft())
        #######################################

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/User group.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ventanaFichaCliente.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(ventanaFichaCliente)
        self.groupBox.setGeometry(QtCore.QRect(1, 1, 370, 250))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(31, 23, 67, 19))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(24, 64, 71, 19))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(42, 103, 131, 19))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(46, 144, 67, 19))
        self.label_4.setObjectName("label_4")
        self.editNombre = QtWidgets.QLineEdit(self.groupBox)
        self.editNombre.setGeometry(QtCore.QRect(105, 20, 240, 27))
        self.editNombre.setObjectName("editNombre")
        self.editApellidos = QtWidgets.QLineEdit(self.groupBox)
        self.editApellidos.setGeometry(QtCore.QRect(105, 60, 240, 27))
        self.editApellidos.setObjectName("editApellidos")
        self.editCarnet = QtWidgets.QLineEdit(self.groupBox)
        self.editCarnet.setGeometry(QtCore.QRect(105, 100, 240, 27))
        self.editCarnet.setObjectName("editCarnet")
        ###### Valido solo numeros y 11 digitos del carnet
        self.editCarnet.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[0-9]*")))
        self.editCarnet.setMaxLength(11)
        ###################################################
        self.buttonAceptar = QtWidgets.QPushButton(self.groupBox)
        self.buttonAceptar.setGeometry(QtCore.QRect(97, 199, 88, 27))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Ok.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonAceptar.setIcon(icon1)
        self.buttonAceptar.setObjectName("buttonAceptar")
        self.buttonAceptar.setEnabled(False)
        self.buttonCancelar = QtWidgets.QPushButton(self.groupBox)
        self.buttonCancelar.setGeometry(QtCore.QRect(227, 199, 88, 27))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Cancel.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonCancelar.setIcon(icon2)
        self.buttonCancelar.setObjectName("buttonCancelar")
        self.comboCargo = QtWidgets.QComboBox(self.groupBox)
        self.comboCargo.setGeometry(QtCore.QRect(105, 141, 240, 27))
        self.comboCargo.setEditable(True)
        self.comboCargo.setObjectName("comboCargo")

        self.retranslateUi(ventanaFichaCliente)
        QtCore.QMetaObject.connectSlotsByName(ventanaFichaCliente)
        
        #todos los eventos de la ventana
        self.buttonCancelar.clicked.connect(lambda:self.generales.cerrarVentana(ventanaFichaCliente))
        self.buttonAceptar.clicked.connect(lambda:self.guardarFichaCliente(ventanaFichaCliente))
        self.editNombre.textChanged.connect(self.verificarCampos)
        self.editApellidos.textChanged.connect(self.verificarCampos)
        self.editCarnet.textChanged.connect(self.verificarCampos)
        self.comboCargo.currentTextChanged.connect(self.verificarCampos)


    def retranslateUi(self, ventanaFichaCliente):
        _translate = QtCore.QCoreApplication.translate
        ventanaFichaCliente.setWindowTitle(_translate("ventanaFichaCliente", "Insertar Ficha de Cliente"))
        self.label.setText(_translate("ventanaFichaCliente", "Nombre:"))
        self.label_2.setText(_translate("ventanaFichaCliente", "Apellidos:"))
        self.label_3.setText(_translate("ventanaFichaCliente", "Carnet:"))
        self.label_4.setText(_translate("ventanaFichaCliente", "Cargo:"))
        self.buttonAceptar.setText(_translate("ventanaFichaCliente", "Aceptar"))
        self.buttonCancelar.setText(_translate("ventanaFichaCliente", "Cancelar"))

        self.inicializarVentana(ventanaFichaCliente)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventanaFichaCliente = QtWidgets.QDialog()
    ui = Ui_VentanaFichaCliente()
    ui.setupUi(ventanaFichaCliente)
    ventanaFichaCliente.show()
    sys.exit(app.exec())