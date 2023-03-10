# Form implementation generated from reading ui file 'QtForm/buscarinventario.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_VentanaBuscarInventario(object):
    def setupUi(self, ventanaBuscarInventario):
        ventanaBuscarInventario.setObjectName("ventanaBuscarInventario")
        ventanaBuscarInventario.resize(480, 480)
        ventanaBuscarInventario.setMinimumSize(QtCore.QSize(480, 480))
        ventanaBuscarInventario.setMaximumSize(QtCore.QSize(480, 480))

        #########pocisionar ventana centrada#####
        qr = ventanaBuscarInventario.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        ventanaBuscarInventario.move(qr.topLeft())
        #######################################

        ventanaBuscarInventario.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/User group.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ventanaBuscarInventario.setWindowIcon(icon)
        self.groupBox_3 = QtWidgets.QGroupBox(ventanaBuscarInventario) 
        self.groupBox_3.setGeometry(QtCore.QRect(1, 430, 478, 48))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.buttonAceptar = QtWidgets.QPushButton(self.groupBox_3)
        self.buttonAceptar.setGeometry(QtCore.QRect(130, 11, 88, 27))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Ok.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonAceptar.setIcon(icon1)
        self.buttonAceptar.setObjectName("buttonAceptar")
        self.buttonCancelar = QtWidgets.QPushButton(self.groupBox_3)
        self.buttonCancelar.setGeometry(QtCore.QRect(290, 11, 88, 27))
        self.buttonAceptar.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Cancel.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonCancelar.setIcon(icon2)
        self.buttonCancelar.setObjectName("buttonCancelar")
        self.groupBox = QtWidgets.QGroupBox(ventanaBuscarInventario)
        self.groupBox.setGeometry(QtCore.QRect(1, 1, 478, 50))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.editInventario = QtWidgets.QLineEdit(self.groupBox)
        self.editInventario.setGeometry(QtCore.QRect(10, 16, 460, 22))
        self.editInventario.setObjectName("editInventario")
        self.groupBox_2 = QtWidgets.QGroupBox(ventanaBuscarInventario)
        self.groupBox_2.setGeometry(QtCore.QRect(1, 50, 478, 380))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(1, 5, 476, 374))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableInventario = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableInventario.setColumnCount(3)
        self.tableInventario.setObjectName("tableInventario")
        self.tableInventario.setRowCount(0)
        self.tableInventario.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableInventario.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableInventario.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableInventario.verticalHeader().setVisible(False)
        #ancho de las columnas
        self.tableInventario.setColumnWidth(0,124)
        self.tableInventario.setColumnWidth(1,124)
        self.tableInventario.setColumnWidth(2,350)

        self.tableInventario.setColumnHidden(0, True)
        #cabecera de la tabla

        self.tablas.headerBuscarInventario(0, self.tableInventario)    
        self.tablas.headerBuscarInventario(1, self.tableInventario)    
        self.tablas.headerBuscarInventario(2, self.tableInventario)   

        self.gridLayout.addWidget(self.tableInventario, 0, 0, 1, 1)

        self.retranslateUi(ventanaBuscarInventario)
        QtCore.QMetaObject.connectSlotsByName(ventanaBuscarInventario)

        self.editInventario.textChanged.connect(self.filtroFilasTabla)
        self.tableInventario.clicked.connect(self.habilitarBoton)
        self.tableInventario.doubleClicked.connect(lambda:self.clienteSeleccionado(ventanaBuscarInventario))
        self.buttonAceptar.clicked.connect(lambda:self.clienteSeleccionado(ventanaBuscarInventario))
        self.buttonCancelar.clicked.connect(lambda:self.generales.cerrarVentana(ventanaBuscarInventario))

    def retranslateUi(self, ventanaBuscarInventario):
        _translate = QtCore.QCoreApplication.translate
        ventanaBuscarInventario.setWindowTitle(_translate("ventanaBuscarInventario", "Buscar Inventario"))
        self.buttonAceptar.setText(_translate("ventanaBuscarInventario", "Aceptar"))
        self.buttonCancelar.setText(_translate("ventanaBuscarInventario", "Cancelar"))

        self.llenadoTabla()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventanaBuscarInventario = QtWidgets.QDialog()
    ui = Ui_VentanaBuscarInventario()
    ui.setupUi(ventanaBuscarInventario)
    ventanaBuscarInventario.show()
    sys.exit(app.exec())
