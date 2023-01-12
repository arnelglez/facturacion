# Form implementation generated from reading ui file 'tipopago.ui'
#
# Created by: PyQt6 UI code generator 6.1.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_VentanaTipoPago(object):
    def setupUi(self, ventanaTipoPago):
        ventanaTipoPago.setObjectName("ventanaTipoPago")
        ventanaTipoPago.resize(372, 152)
        ventanaTipoPago.setMinimumSize(QtCore.QSize(372, 152))
        ventanaTipoPago.setMaximumSize(QtCore.QSize(372, 152))

        #########pocisionar ventana centrada#####
        qr = ventanaTipoPago.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        ventanaTipoPago.move(qr.topLeft())
        #######################################
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Dollar.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ventanaTipoPago.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(ventanaTipoPago)
        self.groupBox.setGeometry(QtCore.QRect(1, 1, 370, 150))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(18, 38, 91, 19))
        self.label.setObjectName("label")
        self.editDescripcion = QtWidgets.QLineEdit(self.groupBox)
        self.editDescripcion.setGeometry(QtCore.QRect(105, 35, 240, 27))
        self.editDescripcion.setObjectName("editDescripcion")
        self.buttonAceptar = QtWidgets.QPushButton(self.groupBox)
        self.buttonAceptar.setGeometry(QtCore.QRect(97, 101, 88, 27))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Ok.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonAceptar.setIcon(icon1)
        self.buttonAceptar.setObjectName("buttonAceptar")
        self.buttonAceptar.setEnabled(False)
        self.buttonCancelar = QtWidgets.QPushButton(self.groupBox)
        self.buttonCancelar.setGeometry(QtCore.QRect(227, 101, 88, 27))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Cancel.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonCancelar.setIcon(icon2)
        self.buttonCancelar.setObjectName("buttonCancelar")

        self.retranslateUi(ventanaTipoPago)
        QtCore.QMetaObject.connectSlotsByName(ventanaTipoPago)

        #eventos de la ventana
        self.buttonCancelar.clicked.connect(lambda:self.generales.cerrarVentana(ventanaTipoPago))
        self.buttonAceptar.clicked.connect(lambda:self.guardarTipoPago(ventanaTipoPago))
        self.editDescripcion.textChanged.connect(self.verificarCampos)

    def retranslateUi(self, ventanaTipoPago):
        _translate = QtCore.QCoreApplication.translate
        ventanaTipoPago.setWindowTitle(_translate("ventanaTipoPago", "Insertar Tipo de Pago"))
        self.label.setText(_translate("ventanaTipoPago", "Descripción:"))
        self.buttonAceptar.setText(_translate("ventanaTipoPago", "Aceptar"))
        self.buttonCancelar.setText(_translate("ventanaTipoPago", "Cancelar"))


        self.inicializacionVentana(ventanaTipoPago)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventanaTipoPago = QtWidgets.QDialog()
    ui = Ui_VentanaTipoPago()
    ui.setupUi(ventanaTipoPago)
    ventanaTipoPago.show()
    sys.exit(app.exec())
