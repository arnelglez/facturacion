# Form implementation generated from reading ui file 'servicio.ui'
#
# Created by: PyQt6 UI code generator 6.1.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_VentanaServicio(object):
    def setupUi(self, ventanaServicio):
        ventanaServicio.setObjectName("ventanaServicio")
        ventanaServicio.resize(433, 242)
        ventanaServicio.setMinimumSize(QtCore.QSize(433, 242))
        ventanaServicio.setMaximumSize(QtCore.QSize(433, 242))

        #########pocisionar ventana centrada#####
        qr = ventanaServicio.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        ventanaServicio.move(qr.topLeft())
        #######################################
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Shopping cart.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ventanaServicio.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(ventanaServicio)
        self.groupBox.setGeometry(QtCore.QRect(1, 1, 431, 240))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(59, 66, 92, 19))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(90, 26, 81, 19))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(17, 104, 131, 19))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(93, 143, 67, 19))
        self.label_4.setObjectName("label_4")
        self.editDescripcion = QtWidgets.QLineEdit(self.groupBox)
        self.editDescripcion.setGeometry(QtCore.QRect(151, 61, 247, 27))
        self.editDescripcion.setObjectName("editDescripcion")
        self.editPrecio = QtWidgets.QLineEdit(self.groupBox)
        self.editPrecio.setGeometry(QtCore.QRect(151, 140, 247, 27))
        self.editPrecio.setObjectName("editPrecio")
        self.editPrecio.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^[0-9]*\.?[0-9]{1,2}")))
        self.comboReparable = QtWidgets.QComboBox(self.groupBox)
        self.comboReparable.setGeometry(QtCore.QRect(151, 21, 247, 27))
        self.comboReparable.setEditable(True)
        self.comboReparable.setObjectName("comboReparable")
        self.comboUM = QtWidgets.QComboBox(self.groupBox)
        self.comboUM.setGeometry(QtCore.QRect(151, 100, 247, 27))
        self.comboUM.setObjectName("comboUM")
        self.buttonAceptar = QtWidgets.QPushButton(self.groupBox)
        self.buttonAceptar.setGeometry(QtCore.QRect(120, 192, 88, 27))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Ok.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonAceptar.setIcon(icon1)
        self.buttonAceptar.setObjectName("buttonAceptar")
        self.buttonAceptar.setEnabled(False)
        self.buttonCancelar = QtWidgets.QPushButton(self.groupBox)
        self.buttonCancelar.setGeometry(QtCore.QRect(260, 192, 88, 27))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Cancel.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonCancelar.setIcon(icon2)
        self.buttonCancelar.setObjectName("buttonCancelar")

        self.retranslateUi(ventanaServicio)
        QtCore.QMetaObject.connectSlotsByName(ventanaServicio)

        #eventos de la ventana
        self.buttonCancelar.clicked.connect(lambda:self.generales.cerrarVentana(ventanaServicio))
        self.buttonAceptar.clicked.connect(lambda:self.guardarServicio(ventanaServicio))
        self.editDescripcion.textChanged.connect(self.verificarCampos)
        self.editPrecio.textChanged.connect(self.verificarCampos)

    def retranslateUi(self, ventanaServicio):
        _translate = QtCore.QCoreApplication.translate
        ventanaServicio.setWindowTitle(_translate("ventanaServicio", "Insertar Servicio"))
        self.label.setText(_translate("ventanaServicio", "Descripción:"))
        self.label_2.setText(_translate("ventanaServicio", "Equipo:"))
        self.label_3.setText(_translate("ventanaServicio", "Unidad de Medida:"))
        self.label_4.setText(_translate("ventanaServicio", "Precio:"))
        self.buttonAceptar.setText(_translate("ventanaServicio", "Aceptar"))
        self.buttonCancelar.setText(_translate("ventanaServicio", "Cancelar"))

        self.inicializarVentana(ventanaServicio)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventanaServicio = QtWidgets.QDialog()
    ui = Ui_VentanaServicio()
    ui.setupUi(ventanaServicio)
    ventanaServicio.show()
    sys.exit(app.exec())