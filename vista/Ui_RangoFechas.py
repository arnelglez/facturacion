# Form implementation generated from reading ui file 'QtForm/rangofechas.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_VentanaRangoFechas(object):
    def setupUi(self, ventanaRangoFechas):
        ventanaRangoFechas.setObjectName("ventanaRangoFechas")
        ventanaRangoFechas.resize(353, 233)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ventanaRangoFechas.sizePolicy().hasHeightForWidth())
        ventanaRangoFechas.setSizePolicy(sizePolicy)
        ventanaRangoFechas.setMinimumSize(QtCore.QSize(353, 233))
        ventanaRangoFechas.setMaximumSize(QtCore.QSize(353, 233))

        #########pocisionar ventana centrada#####
        qr = ventanaRangoFechas.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        ventanaRangoFechas.move(qr.topLeft())
        #######################################


        ventanaRangoFechas.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/rango.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ventanaRangoFechas.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(ventanaRangoFechas)
        self.groupBox.setGeometry(QtCore.QRect(1, 1, 351, 231))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.labelDesde = QtWidgets.QLabel(self.groupBox)
        self.labelDesde.setGeometry(QtCore.QRect(63, 60, 67, 19))
        self.labelDesde.setObjectName("labelDesde")
        self.labelHasta = QtWidgets.QLabel(self.groupBox)
        self.labelHasta.setGeometry(QtCore.QRect(69, 120, 91, 19))
        self.labelHasta.setObjectName("labelHasta")
        self.buttonAceptar = QtWidgets.QPushButton(self.groupBox)
        self.buttonAceptar.setGeometry(QtCore.QRect(80, 180, 88, 27))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Ok.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonAceptar.setIcon(icon1)
        self.buttonAceptar.setObjectName("buttonAceptar")
        self.buttonCancelar = QtWidgets.QPushButton(self.groupBox)
        self.buttonCancelar.setGeometry(QtCore.QRect(200, 180, 88, 27))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonCancelar.sizePolicy().hasHeightForWidth())
        self.buttonCancelar.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Cancel.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonCancelar.setIcon(icon2)
        self.buttonCancelar.setObjectName("buttonCancelar")
        self.dateDesde = QtWidgets.QDateEdit(self.groupBox)
        self.dateDesde.setGeometry(QtCore.QRect(120, 57, 200, 28))
        self.dateDesde.setDisplayFormat('dd/MM/yyyy')
        self.dateDesde.setCalendarPopup(True)
        self.dateDesde.setObjectName("dateDesde")
        self.dateHasta = QtWidgets.QDateEdit(self.groupBox)
        self.dateHasta.setGeometry(QtCore.QRect(120, 117, 200, 28))
        self.dateHasta.setDisplayFormat('dd/MM/yyyy')
        self.dateHasta.setCalendarPopup(True)
        self.dateHasta.setObjectName("dateHasta")

        self.retranslateUi(ventanaRangoFechas)
        QtCore.QMetaObject.connectSlotsByName(ventanaRangoFechas)


        self.buttonCancelar.clicked.connect(lambda:self.cerrarVentana(ventanaRangoFechas))
        self.buttonAceptar.clicked.connect(lambda:self.rangoSeleccionado(ventanaRangoFechas))

    def retranslateUi(self, ventanaRangoFechas):
        _translate = QtCore.QCoreApplication.translate
        ventanaRangoFechas.setWindowTitle(_translate("ventanaRangoFechas", "Rango de Fechas"))
        self.labelDesde.setText(_translate("ventanaRangoFechas", "Desde:"))
        self.labelHasta.setText(_translate("ventanaRangoFechas", "Hasta:"))
        self.buttonAceptar.setText(_translate("ventanaRangoFechas", "Aceptar"))
        self.buttonCancelar.setText(_translate("ventanaRangoFechas", "Cancelar"))

    
        self.inicializarVentana(ventanaRangoFechas)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventanaRangoFechas = QtWidgets.QDialog()
    ui = Ui_VentanaRangoFechas()
    ui.setupUi(ventanaRangoFechas)
    ventanaRangoFechas.show()
    sys.exit(app.exec())
