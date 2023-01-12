# Form implementation generated from reading ui file 'QtForm/liquidacion.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_VentanaLiquidacion(object):
    def setupUi(self, ventanaLiquidacion):
        ventanaLiquidacion.setObjectName("ventanaLiquidacion")
        ventanaLiquidacion.resize(555, 230)
        ventanaLiquidacion.setMinimumSize(QtCore.QSize(555, 230))
        ventanaLiquidacion.setMaximumSize(QtCore.QSize(555, 230))

        #########pocisionar ventana centrada#####
        qr = ventanaLiquidacion.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        ventanaLiquidacion.move(qr.topLeft())
        #######################################

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Dollar.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ventanaLiquidacion.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(ventanaLiquidacion)
        self.groupBox.setGeometry(QtCore.QRect(1, 1, 553, 228))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.labelCliente = QtWidgets.QLabel(self.groupBox)
        self.labelCliente.setGeometry(QtCore.QRect(20, 75, 531, 19))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelCliente.setFont(font)
        self.labelCliente.setObjectName("labelCliente")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(370, 24, 111, 19))
        self.label_2.setObjectName("label_2")
        self.editFecha = QtWidgets.QLineEdit(self.groupBox)
        self.editFecha.setEnabled(False)
        self.editFecha.setGeometry(QtCore.QRect(423, 22, 113, 27))
        self.editFecha.setObjectName("editFecha")
        self.editDocumento = QtWidgets.QLineEdit(self.groupBox)
        self.editDocumento.setEnabled(False)
        self.editDocumento.setGeometry(QtCore.QRect(137, 22, 113, 27))
        self.editDocumento.setObjectName("editDocumento")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 24, 130, 19))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 124, 91, 19))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(267, 123, 130, 19))
        self.label_6.setObjectName("label_6")
        self.editMonto = QtWidgets.QLineEdit(self.groupBox)
        self.editMonto.setGeometry(QtCore.QRect(387, 120, 150, 27))
        self.editMonto.setObjectName("editMonto")
        self.editMonto.setValidator(QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^[0-9]*\.?[0-9]{1,2}")))
        self.buttonAceptar = QtWidgets.QPushButton(self.groupBox)
        self.buttonAceptar.setGeometry(QtCore.QRect(150, 181, 88, 27))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Ok.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonAceptar.setIcon(icon1)
        self.buttonAceptar.setObjectName("buttonAceptar")
        self.buttonCancelar = QtWidgets.QPushButton(self.groupBox)
        self.buttonCancelar.setGeometry(QtCore.QRect(320, 181, 88, 27))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Cancel.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonCancelar.setIcon(icon2)
        self.buttonCancelar.setObjectName("buttonCancelar")
        self.editFactura = QtWidgets.QLineEdit(self.groupBox)
        self.editFactura.setGeometry(QtCore.QRect(84, 120, 170, 27))
        self.editFactura.setObjectName("editFactura")
        self.buttonFactura = QtWidgets.QToolButton(self.editFactura)
        self.buttonFactura.setGeometry(142,0,27,26)
        self.buttonFactura.setObjectName('buttonFactura')
        self.buttonFactura.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.buttonFactura.setToolTip('Buscar Facturas')

        self.retranslateUi(ventanaLiquidacion)
        QtCore.QMetaObject.connectSlotsByName(ventanaLiquidacion)

        self.buttonAceptar.clicked.connect(lambda:self.guardarLiquidacion(ventanaLiquidacion))
        self.buttonCancelar.clicked.connect(lambda:self.cerrarVentana(ventanaLiquidacion))
        self.buttonFactura.clicked.connect(self.verificarFactura)
        self.editFactura.returnPressed.connect(self.verificarFactura)

    def retranslateUi(self, ventanaLiquidacion):
        _translate = QtCore.QCoreApplication.translate
        ventanaLiquidacion.setWindowTitle(_translate("ventanaLiquidacion", "Liquidación"))
        self.labelCliente.setText(_translate("ventanaLiquidacion", "Nombre del cliente para hacer la recepcion"))
        self.label_2.setText(_translate("ventanaLiquidacion", "Fecha:"))
        self.label_3.setText(_translate("ventanaLiquidacion", "No. Documento:"))
        self.label_5.setText(_translate("ventanaLiquidacion", "Factura:"))
        self.label_6.setText(_translate("ventanaLiquidacion", "Monto a liquidar:"))
        self.buttonFactura.setText(_translate("ventanaLiquidacion", "..."))
        self.buttonAceptar.setText(_translate("ventanaLiquidacion", "Aceptar"))
        self.buttonCancelar.setText(_translate("ventanaLiquidacion", "Cancelar"))

        self.inicializarVentana(ventanaLiquidacion)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventanaLiquidacion = QtWidgets.QDialog()
    ui = Ui_VentanaLiquidacion()
    ui.setupUi(ventanaLiquidacion)
    ventanaLiquidacion.show()
    sys.exit(app.exec())
