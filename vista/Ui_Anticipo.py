# Form implementation generated from reading ui file 'QtForm/anticipo.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_VentanaAnticipo(object):
    def setupUi(self, ventanaAnticipo):
        ventanaAnticipo.setObjectName("ventanaAnticipo")
        ventanaAnticipo.resize(700, 450)
        ventanaAnticipo.setMinimumSize(QtCore.QSize(700, 450))
        ventanaAnticipo.setMaximumSize(QtCore.QSize(700, 450))

        #########pocisionar ventana centrada#####
        qr = ventanaAnticipo.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        ventanaAnticipo.move(qr.topLeft())
        #######################################

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Anticipo.jpg")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ventanaAnticipo.setWindowIcon(icon)
        self.tableAnticipo = QtWidgets.QTableWidget(ventanaAnticipo)
        self.tableAnticipo.setGeometry(QtCore.QRect(1, 39, 698, 410))
        self.tableAnticipo.setObjectName("tableAnticipo")
        self.tableAnticipo.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableAnticipo.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableAnticipo.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableAnticipo.verticalHeader().setVisible(False)
        self.tableAnticipo.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableAnticipo.customContextMenuRequested.connect(self.contexMenuEvent)

        self.groupBox = QtWidgets.QGroupBox(ventanaAnticipo)
        self.groupBox.setGeometry(QtCore.QRect(1, 1, 698, 37))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox_2")
        self.toolBar = QtWidgets.QToolBar(self.groupBox)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Dollar.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Devolver.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
       
        self.actionLiquidar = QtGui.QAction(ventanaAnticipo)
        self.actionLiquidar.setIcon(icon1)
        self.actionLiquidar.setObjectName("actionLiquidar")
        self.actionDevolver = QtGui.QAction(ventanaAnticipo)
        self.actionDevolver.setIcon(icon2)
        self.actionDevolver.setObjectName("actionDevolver")
        
        self.toolBar.addAction(self.actionLiquidar)
        self.toolBar.addAction(self.actionDevolver)

        self.retranslateUi(ventanaAnticipo)
        QtCore.QMetaObject.connectSlotsByName(ventanaAnticipo)

        self.tableAnticipo.clicked.connect(self.filaSeleccionada)
        self.actionDevolver.triggered.connect(lambda:self.devolucionAnticipo(ventanaAnticipo))
        self.actionLiquidar.triggered.connect(lambda:self.liquidacionAnticipo(ventanaAnticipo))


    def retranslateUi(self, ventanaAnticipo):
        _translate = QtCore.QCoreApplication.translate
        ventanaAnticipo.setWindowTitle(_translate("ventanaAnticipo", "Lista de Anticipos"))
        self.toolBar.setWindowTitle(_translate("ventanaAnticipo", "toolBar"))
        self.actionLiquidar.setText(_translate("ventanaAnticipo", "Liquidar Anticipo"))
        self.actionDevolver.setText(_translate("ventanaAnticipo", "Devolver Anticipo"))

        self.inicializarVentana()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventanaAnticipo = QtWidgets.QDialog()
    ui = Ui_VentanaAnticipo()
    ui.setupUi(ventanaAnticipo)
    ventanaAnticipo.show()
    sys.exit(app.exec())