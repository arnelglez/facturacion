# Form implementation generated from reading ui file 'QtForm/cargarfacturacobro.ui'
#
# Created by: PyQt6 UI code generator 6.1.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_VentanaCargarFacturaCobro(object):
    def setupUi(self, ventanaCargarFacturaCobro):
        ventanaCargarFacturaCobro.setObjectName("ventanaCargarFacturaCobro")
        ventanaCargarFacturaCobro.resize(442, 262)
        ventanaCargarFacturaCobro.setMinimumSize(QtCore.QSize(442, 262))
        ventanaCargarFacturaCobro.setMaximumSize(QtCore.QSize(442, 262))

        #########pocisionar ventana centrada#####
        qr = ventanaCargarFacturaCobro.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        ventanaCargarFacturaCobro.move(qr.topLeft())
        #######################################


        self.groupBox = QtWidgets.QGroupBox(ventanaCargarFacturaCobro)
        self.groupBox.setGeometry(QtCore.QRect(1, 1, 440, 260))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(70, 50, 67, 19))
        self.label.setObjectName("label")
        self.comboCliente = QtWidgets.QComboBox(self.groupBox)
        self.comboCliente.setGeometry(QtCore.QRect(130, 46, 270, 27))
        self.comboCliente.setObjectName("comboCliente")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 111, 19))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(34, 150, 101, 19))
        self.label_3.setObjectName("label_3")
        self.buttonAceptar = QtWidgets.QPushButton(self.groupBox)
        self.buttonAceptar.setGeometry(QtCore.QRect(110, 200, 88, 27))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Ok.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonAceptar.setIcon(icon)
        self.buttonAceptar.setObjectName("buttonAceptar")
        self.buttonCancelar = QtWidgets.QPushButton(self.groupBox)
        self.buttonCancelar.setGeometry(QtCore.QRect(250, 200, 88, 27))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Cancel.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonCancelar.setIcon(icon1)
        self.buttonCancelar.setObjectName("buttonCancelar")
                
        self.dateDesde = QtWidgets.QDateEdit(self.groupBox)
        self.dateDesde.setGeometry(QtCore.QRect(130, 95, 269, 28))
        self.dateDesde.setDisplayFormat('dd/MM/yyyy')
        self.dateDesde.setCalendarPopup(True)
        self.dateDesde.setObjectName("dateDesde")
        self.dateHasta = QtWidgets.QDateEdit(self.groupBox)
        self.dateHasta.setGeometry(QtCore.QRect(130, 146, 269, 28))
        self.dateHasta.setDisplayFormat('dd/MM/yyyy')
        self.dateHasta.setCalendarPopup(True)
        self.dateHasta.setObjectName("dateHasta")
        
        self.retranslateUi(ventanaCargarFacturaCobro)
        QtCore.QMetaObject.connectSlotsByName(ventanaCargarFacturaCobro)
        
        
        self.buttonAceptar.clicked.connect(self.imprimirReporte)
        self.buttonCancelar.clicked.connect(lambda:self.cerrarVentana(ventanaCargarFacturaCobro))

    def retranslateUi(self, ventanaCargarFacturaCobro):
        _translate = QtCore.QCoreApplication.translate
        ventanaCargarFacturaCobro.setWindowTitle(_translate("ventanaCargarFacturaCobro", "Factura"))
        self.label.setText(_translate("ventanaCargarFacturaCobro", "Cliente:"))
        self.label_2.setText(_translate("ventanaCargarFacturaCobro", "Fecha de Inicio:"))
        self.label_3.setText(_translate("ventanaCargarFacturaCobro", "Fecha de Fin:"))
        self.buttonAceptar.setText(_translate("ventanaCargarFacturaCobro", "Aceptar"))
        self.buttonCancelar.setText(_translate("ventanaCargarFacturaCobro", "Cancelar"))

        self.inicializarVentana(ventanaCargarFacturaCobro)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventanaCargarFacturaCobro = QtWidgets.QDialog()
    ui = Ui_VentanaCargarFacturaCobro()
    ui.setupUi(ventanaCargarFacturaCobro)
    ventanaCargarFacturaCobro.show()
    sys.exit(app.exec())
