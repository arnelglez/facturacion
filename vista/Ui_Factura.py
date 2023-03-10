# Form implementation generated from reading ui file 'facturacion.ui'
#
# Created by: PyQt6 UI code generator 6.1.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from entidades.entFacturaDesglose import eFacturaDesglose
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_VentanaFactura(object):
    def setupUi(self, ventanaFactura):
        ventanaFactura.setObjectName("ventanaFactura")
        ventanaFactura.resize(845, 584)
        ventanaFactura.setMinimumSize(QtCore.QSize(845, 584))
        ventanaFactura.setMaximumSize(QtCore.QSize(845, 584))

        #########pocisionar ventana centrada#####
        qr = ventanaFactura.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        ventanaFactura.move(qr.topLeft())
        #######################################
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/Factura.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ventanaFactura.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(ventanaFactura)
        self.groupBox.setGeometry(QtCore.QRect(1, 1, 843, 582))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(40, 24, 67, 19))
        self.label.setObjectName("label")
        self.labelCliente = QtWidgets.QLabel(self.groupBox)
        self.labelCliente.setGeometry(QtCore.QRect(100, 60, 651, 19))
        self.labelCliente.setVisible(False)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelCliente.setFont(font)
        self.labelCliente.setObjectName("labelCliente")
        self.editCliente = QtWidgets.QLineEdit(self.groupBox)
        self.editCliente.setGeometry(QtCore.QRect(100, 22, 193, 27))
        self.editCliente.setObjectName("editCliente")
        self.buttonCliente = QtWidgets.QToolButton(self.editCliente)
        self.buttonCliente.setGeometry(QtCore.QRect(165, 0, 27, 26))
        self.buttonCliente.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.buttonCliente.setObjectName("buttonCliente")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(667, 24, 111, 19))
        self.label_2.setObjectName("label_2")
        self.editFecha = QtWidgets.QLineEdit(self.groupBox)
        self.editFecha.setEnabled(False)
        self.editFecha.setGeometry(QtCore.QRect(720, 22, 113, 27))
        self.editFecha.setObjectName("editFecha")
        self.editFactura = QtWidgets.QLineEdit(self.groupBox)
        self.editFactura.setEnabled(False)
        self.editFactura.setGeometry(QtCore.QRect(720, 58, 113, 27))
        self.editFactura.setObjectName("editFactura")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(629, 60, 111, 19))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(313, 24, 67, 19))
        self.label_4.setObjectName("label_4")
        self.comboFichaCliente = QtWidgets.QComboBox(self.groupBox)
        self.comboFichaCliente.setGeometry(QtCore.QRect(370, 22, 279, 27))
        self.comboFichaCliente.setObjectName("comboFichaCliente")
        
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(1, 95, 841, 37))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.toolBar = QtWidgets.QToolBar(self.groupBox_2)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/03.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/04.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/save.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/printer.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/nota.jpg")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.icon6 = QtGui.QIcon()
        self.icon6.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/cup.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.icon7 = QtGui.QIcon()
        self.icon7.addPixmap(QtGui.QPixmap(self.generales.resource_path("../img/mlc.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

        self.actionAdd = QtGui.QAction(self)
        self.actionAdd.setIcon(icon1)
        self.actionAdd.setObjectName("actionAdd")
        self.actionDelete = QtGui.QAction(self)
        self.actionDelete.setIcon(icon2)
        self.actionDelete.setObjectName("actionDelete")
        self.actionSave = QtGui.QAction(self)
        self.actionSave.setIcon(icon3)
        self.actionSave.setObjectName("actionSave")
        self.actionPrint = QtGui.QAction(self)
        self.actionPrint.setIcon(icon4)
        self.actionPrint.setObjectName("actionPrint")
        self.actionNota = QtGui.QAction(self)
        self.actionNota.setIcon(icon5)
        self.actionNota.setObjectName("actionNota")
        self.actionMoneda = QtGui.QAction(self)
        self.actionMoneda.setObjectName("actionMoneda")

        self.tableFactura = QtWidgets.QTableWidget(self.groupBox)
        self.tableFactura.setGeometry(QtCore.QRect(1, 132, 841, 430))
        self.tableFactura.setColumnCount(11)
        self.tableFactura.setObjectName("tableFactura")
        self.tableFactura.setRowCount(0)
        self.tableFactura.verticalHeader().setVisible(False)
        self.tableFactura.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableFactura.customContextMenuRequested.connect(self.contexMenuEvent)

        #ancho de las columnas
        self.tableFactura.setColumnWidth(0,10)
        self.tableFactura.setColumnWidth(1,140)
        self.tableFactura.setColumnWidth(2,140)
        self.tableFactura.setColumnWidth(3,150)
        self.tableFactura.setColumnWidth(4,50)
        self.tableFactura.setColumnWidth(5,118)
        self.tableFactura.setColumnWidth(6,120)
        self.tableFactura.setColumnWidth(7,120)
        self.tableFactura.setColumnWidth(8,130)

        self.tableFactura.setColumnHidden(0, True)
        self.tableFactura.setColumnHidden(8, True)
        self.tableFactura.setColumnHidden(9, True)
        self.tableFactura.setColumnHidden(10, True)
        #cabecera de la tabla
        self.headerTablaFactura()


        self.labelTotal = QtWidgets.QLabel(self.groupBox)
        self.labelTotal.setGeometry(QtCore.QRect(740, 562, 100, 19))
        self.labelTotal.setObjectName("labelTotal") 
        self.labelTotal.setVisible(False)
        self.labelReparado = QtWidgets.QLabel(self.groupBox)
        self.labelReparado.setGeometry(QtCore.QRect(8, 562, 541, 19))
        self.labelReparado.setVisible(False)
        self.labelReparado.setObjectName("labelReparado")


        self.toolBar.addAction(self.actionMoneda)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionPrint)        
        self.toolBar.addAction(self.actionNota)

        self.retranslateUi(ventanaFactura)
        QtCore.QMetaObject.connectSlotsByName(ventanaFactura)

        # Eventos de la ventana
        efacturadesglose = eFacturaDesglose()
        self.buttonCliente.clicked.connect(self.verificarCliente)
        self.editCliente.returnPressed.connect(self.verificarCliente) 
        self.actionMoneda.triggered.connect(self.cambioMoneda)
        self.actionAdd.triggered.connect(lambda:self.lineaTablaFactura(efacturadesglose))
        self.actionSave.triggered.connect(self.guardarFactura)
        self.actionDelete.triggered.connect(self.eliminarFactura)
        self.actionPrint.triggered.connect(self.vistaPrevia)
        self.actionNota.triggered.connect(self.notaFactura)

    def retranslateUi(self, ventanaFactura):
        _translate = QtCore.QCoreApplication.translate
        ventanaFactura.setWindowTitle(_translate("ventanaFactura", "Factura"))
        self.label.setText(_translate("ventanaFactura", "Cliente:"))
        self.labelCliente.setText(_translate("ventanaFactura", "Nombre del cliente para hacer la facturacion"))
        self.buttonCliente.setText(_translate("ventanaFactura", "..."))
        self.label_2.setText(_translate("ventanaFactura", "Fecha:"))
        self.label_3.setText(_translate("ventanaFactura", "No. Factura:"))
        self.label_4.setText(_translate("ventanaFactura", "Recibe:"))
        self.labelTotal.setText(_translate("ventanaFactura", "0.00"))
        self.labelReparado.setText(_translate("ventanaFactura", "TextLabel"))
        self.actionMoneda.setText(_translate("ventanaFactura", "Cambiar a MLC"))
        self.actionAdd.setText(_translate("ventanaFactura", "Adicionar Fila"))
        self.actionDelete.setText(_translate("ventanaFactura", "Eliminar Fila"))
        self.actionSave.setText(_translate("ventanaFactura", "Guardar Factura"))
        self.actionPrint.setText(_translate("ventanaFactura", "Imprimir Factura"))
        self.actionNota.setText(_translate("ventanaFactura", "Nota en la Factura"))

        self.inicializarVentana(ventanaFactura)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventanaFactura = QtWidgets.QDialog()
    ui = Ui_VentanaFactura()
    ui.setupUi(ventanaFactura)
    ventanaFactura.show()
    sys.exit(app.exec())
